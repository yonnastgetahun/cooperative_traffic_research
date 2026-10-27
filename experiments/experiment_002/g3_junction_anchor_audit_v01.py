#!/usr/bin/env python3
"""Targeted preselected junction case, seed2103/window200/veh0213/C6C7.

This is NOT an exact native vehicle-length occupancy reconstruction.
"""
import argparse,csv,json,statistics
import xml.etree.ElementTree as ET

SEED=2103
WINDOW=200
VEHICLE="veh0213"
UPSTREAM="C6C7"
INTERNAL_LANE=":C7_11_0"
BEGIN,END=60.,90.

def main():
    p=argparse.ArgumentParser()
    for name in ("events","fcd","native-edge-data","observed-bins","report"):
        p.add_argument("--"+name,required=True)
    a=p.parse_args()
    native=[r for r in csv.DictReader(open(a.events)) if r["vehicle"]==VEHICLE]
    idx=[i for i,r in enumerate(native) if r["edge"]==UPSTREAM and r["kind"]=="external"]
    if len(idx)!=1:raise RuntimeError("Expected one upstream C6C7 visit on anchor route")
    from_edge=native[idx[0]]
    following=[]
    for e in native[idx[0]+1:]:
        if e["kind"]=="external":break
        following.append(e)
    if not following:raise RuntimeError("Native vehroute internal junction events missing")
    end_internal=float(following[-1]["exit_s"])
    external_exit=float(from_edge["exit_s"])
    if end_internal<external_exit:
        raise RuntimeError("Internal movement precedes road exit")
    # Full 1-second simulation timestamps: FRONT lane membership, not physical extent.
    snapshots=[]
    for _,node in ET.iterparse(a.fcd,events=("end",)):
        if node.tag!="timestep":continue
        t=float(node.get("time"))
        if BEGIN<=t<END:
            for v in node.findall("vehicle"):
                if v.get("id")==VEHICLE:
                    snapshots.append(dict(time=t,lane=v.get("lane",""),
                                          position_m=float(v.get("pos","nan")),
                                          speed_mps=float(v.get("speed","nan"))))
        node.clear()
    bins=[r for r in csv.DictReader(open(a.observed_bins))
          if r["edge"]==UPSTREAM and
             float(r["interval_begin_s"])==BEGIN and
             float(r["interval_end_s"])==END and r["edge_type"]=="external"]
    if len(bins)!=1:raise RuntimeError("Native road bin unavailable")
    b=bins[0]
    raw=ET.parse(a.native_edge_data).getroot()
    native_vals=[float(e.get("sampledSeconds")) for interval in raw.findall("interval")
                 if float(interval.get("begin"))==BEGIN and float(interval.get("end"))==END
                 for e in interval.findall("edge") if e.get("id")==UPSTREAM]
    if len(native_vals)!=1 or abs(native_vals[0]-float(b["native_sampledSeconds"]))>1e-6:
        raise RuntimeError("Native cross-source road sampledSeconds mismatch")
    actual= [r for r in snapshots if r["lane"]==INTERNAL_LANE]
    report={
      "status":"targeted_case_reproduced_at_native_step_resolution_not_causal_junction_delay",
      "seed":SEED,"window_s":WINDOW,"vehicle":VEHICLE,
      "source_external_edge":UPSTREAM,"native_external_exit_step_s":external_exit,
      "native_internal_edges":[x["edge"] for x in following],
      "native_internal_exit_steps_s":[float(x["exit_s"]) for x in following],
      "internal_dwell_from_exit_steps_s":round(end_internal-external_exit,5),
      "target_bin":[BEGIN,END],
      "native_external_road_sampledSeconds":native_vals[0],
      "FCD_external_front_vehicle_seconds":float(b["fcd_vehicle_sample_seconds"]),
      "anchor_FCD_samples":len(snapshots),
      "internal_front_samples_target_lane":len(actual),
      "internal_front_stopped_under_0_1mps":sum(x["speed_mps"]<0.1 for x in actual),
      "internal_front_positions_m_first_last":([actual[0]["position_m"],actual[-1]["position_m"]] if actual else []),
      "measured_at":"original 1.0 second SUMO solver steps",
      "limitations":[
        "Native vehroute exit times are step-resolution edge events, not continuous physical crossing times.",
        "Native SUMO edge sampledSeconds can include vehicle physical extent overlapping prior edge while front is downstream.",
        "The native road sampledSeconds field is not attributed to this one vehicle by SUMO output.",
        "FCD position is a front coordinate; no physically exact rear bumper occupancy integration was performed.",
        "Internal junction dwell is not equivalent to causal congestion or signal delay."],
      "source":"preselected M2 development seed2103 high congestion + standalone pinned digest native event replay"
    }
    with open(a.report,"w") as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    if (len(snapshots)!=30 or len(actual)<28 or
        native_vals[0]<29 or float(b["fcd_vehicle_sample_seconds"])>1 or
        not report["native_internal_edges"]):
        raise RuntimeError("Expected preselected anchor evidence not observed")

if __name__=="__main__":main()
