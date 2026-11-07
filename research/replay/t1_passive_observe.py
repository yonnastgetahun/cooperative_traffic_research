#!/usr/bin/env python3
"""T1 seed-2101 passive B/C observation ONLY; no new policy or seed generation.

Use original Actions artifact 13486493479 as input. Single-use CLI and
strict original vehicle parity before any physical interpretation.
"""
import argparse
import collections
import hashlib
import json
import math
import statistics
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

SEED = 2101
ORIGINAL_SHA = {
    "source/demand.json": "5e641331cfb4c58baa6decd5578325e24d55162da8e7299ef7729fbe704507d7",
    "source/network.net.xml": "e3ec1811290f39c1a8e6a2c81e24180c08c71e22e0fcdbeb14fcc740aa87d601",
    "source/trips.xml": "b7e1424a7c44e2d4a0c66098006e3c31579a9dcc074d2503b53687a14c223ce5",
    "feasibility_summary.json": "f3d27466b1075c9f6eee3ccc41a7690f3333a86f35624a89a5b0d8e7236ae788",
    "sumo_B/routes.rou.xml": "3d2984a4010445e8abe03d5855e796a3291b95ca2b0de763f05c0869a1f8a01e",
    "sumo_C/routes.rou.xml": "707b6c215b0792d4cf4d99c15e1a34670595e51995cd6814bc8ea8a7aa2d1718",
    "sumo_B/tripinfo.xml": "b1afa3b889602af2431a1cd7838da5e9f7d9ac8251d9df84aa937e6a6ddffb1a",
    "sumo_C/tripinfo.xml": "3a2c1d3873902f3f000819dd273cd2bce2428fc917312453184b350dde22b9a9",
    "sumo_B/statistics.xml": "9ba856b18803e86cde508682d683f42863301db209ad363c41159702239c6b0c",
    "sumo_C/statistics.xml": "7bf805d5ea36604f69693a0022b0a5edcf0ba8ea7b85a0fb57344fa203d4d5d0",
    "sumo_B/collisions.xml": "8066ad3d845cc9f268802c339b06f9b48ac70ed2da69904c01eefa46d70a7855",
    "sumo_C/collisions.xml": "01a6be79775f3b0c3bfe7acb7f95d719b52b93f134c3a338abbf12b97db00533",
}
FIELDS = ("depart", "departDelay", "arrival", "duration", "waitingTime", "timeLoss")
TOL = 0.01000001
STOP_SPEED = 0.1
SLOW_SPEED = 5.0

def fail(message):
    raise RuntimeError(message)

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def trips(root):
    rows = ET.parse(root / "source/trips.xml").getroot().findall("trip")
    result = {v.get("id"): float(v.get("depart")) for v in rows}
    if len(rows) != 1000 or len(result) != 1000:
        fail("Original preferred-departure identity mismatch")
    return result

def routes(path):
    entries = ET.parse(path).getroot().findall("vehicle")
    result = {}
    for v in entries:
        rt = v.find("route")
        if rt is None:
            fail("Expected original fixed route")
        result[v.get("id")] = (float(v.get("depart")), tuple(rt.get("edges").split()))
    if len(entries) != 1000 or len(result) != 1000:
        fail("Original requested route identity mismatch")
    if any(float(x.get("depart")) > float(y.get("depart")) for x, y in zip(entries, entries[1:])):
        fail("Original SUMO route input unsorted")
    return result

def infos(path):
    entries = ET.parse(path).getroot().findall("tripinfo")
    result = {v.get("id"): v.attrib for v in entries}
    if len(entries) != 1000 or len(result) != 1000:
        fail("Tripinfo lacks exactly 1000 matched IDs: " + str(path))
    return result

def stats(path):
    root = ET.parse(path).getroot()
    return {tag: dict(root.find(tag).attrib) for tag in ("vehicles", "teleports", "safety")}

def collisions(path):
    return len(ET.parse(path).getroot().findall("collision"))

def eligible_ids(preferred):
    return set(sorted(preferred, key=lambda v: (hashlib.sha256(
        ("T1:eligible:2101:" + v).encode()).hexdigest(), v))[:500])

def verify_inputs(root, require_binary=False):
    ledger = {}
    for file, expected in ORIGINAL_SHA.items():
        p = root / file
        if not p.is_file():
            fail("Missing original archived file: " + str(p))
        actual = digest(p)
        if actual != expected:
            fail("Original archive SHA256 mismatch: " + file)
        ledger[file] = actual
    b, c = routes(root/"sumo_B/routes.rou.xml"), routes(root/"sumo_C/routes.rou.xml")
    p = trips(root)
    if set(b) != set(c) or set(b) != set(p):
        fail("Original matched IDs differ between B, C and preferred departures")
    e = eligible_ids(p)
    changed = {}
    for vid in p:
        bd, br = b[vid]
        cd, cr = c[vid]
        if br != cr:
            fail("C changed original fixed route for " + vid)
        if abs(bd - p[vid]) > 0.0001:
            fail("B requested departure differs from original")
        shift = round(cd-bd, 6)
        if shift:
            if abs(shift-10) > .0001 or vid not in e:
                fail("Unexpected or nonparticipant C requested shift for " + vid)
            changed[vid] = shift
    if len(changed) != 12 or abs(sum(changed.values())-120) > .0001:
        fail("Not exactly 12 authorized original 10s shifts")
    original = json.loads((root/"feasibility_summary.json").read_text())
    if original.get("demand_seed") != 2101 or len(original.get("phase_results", [])) != 4:
        fail("Original T1 phase summary mismatched")
    env = {"archive_source": "GitHub Actions run 42183640504, artifact 13486493479",
           "artifact_sha256": "b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae",
           "original_member_sha256": ledger, "n": len(p),
           "eligible": len(e), "shifts": changed}
    if require_binary:
        version = subprocess.check_output(["sumo", "--version"], text=True).strip()
        help_text = subprocess.check_output(["sumo", "--help"], text=True)
        if "1.28.0" not in version:
            fail("SUMO executable not pinned 1.28.0: " + version)
        for flag in ("--fcd-output ", "--vehroute-output ", "--vehroute-output.exit-times"):
            if flag not in help_text:
                fail("Pinned SUMO does not support passive flag " + flag)
        env["sumo_version"] = version
    return env

def replay(root, arm, out):
    if arm not in ("B", "C"):
        fail("Only the two original B/C arms are authorized")
    verify_inputs(root, require_binary=True)
    if out.exists():
        fail("No reruns or overwrites: output directory already exists")
    out.mkdir(parents=True)
    # Original command behavior is preserved. ONLY output paths + two passive
    # output families have changed from original run_v01.simulate invocation.
    cmd = [
        "sumo", "-n", str(root/"source/network.net.xml"),
        "-r", str(root/("sumo_"+arm)/"routes.rou.xml"),
        "--tripinfo-output", str(out/"tripinfo.xml"),
        "--statistic-output", str(out/"statistics.xml"),
        "--collision-output", str(out/"collisions.xml"),
        "--seed", "2101", "--no-step-log", "true",
        "--log", str(out/"sumo.log"),
        "--fcd-output", str(out/"fcd.xml"),
        "--vehroute-output", str(out/"vehroute.xml"),
        "--vehroute-output.exit-times", "true"
    ]
    write_json(out/"command.json", {"command": cmd,
        "only_changed_original_options": ["output paths", "--fcd-output",
                                         "--vehroute-output", "--vehroute-output.exit-times"]})
    with (out/"runner.stdout.log").open("w") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
    for file in ("tripinfo.xml","statistics.xml","collisions.xml","fcd.xml","vehroute.xml"):
        if not (out/file).is_file():
            fail("Passive replay missing output " + file)

def audit_arm(root, arm, out):
    record = {"arm": arm, "status": "INVALID_REPLAY"}
    write_json(out/"parity.json", record)
    verify_inputs(root)
    old, new = infos(root/("sumo_"+arm)/"tripinfo.xml"), infos(out/"tripinfo.xml")
    if set(old) != set(new):
        fail("Matched tripinfo ID sets differ")
    worst = 0.
    for vid in old:
        for field in FIELDS:
            diff = abs(float(old[vid][field])-float(new[vid][field]))
            worst = max(worst, diff)
            if diff > TOL:
                fail("Original per-driver parity failed: %s %s %.8f" % (arm,vid,diff))
        for field in ("departLane", "rerouteNo", "speedFactor"):
            if old[vid].get(field) != new[vid].get(field):
                fail("Original vehicle field changed: %s %s %s" % (arm,vid,field))
    if stats(root/("sumo_"+arm)/"statistics.xml") != stats(out/"statistics.xml"):
        fail("Original safety/teleport/vehicle statistics changed")
    if collisions(root/("sumo_"+arm)/"collisions.xml") != collisions(out/"collisions.xml"):
        fail("Original structured collision count changed")
    preferred = trips(root)
    total = sum(float(v["arrival"])-preferred[k] for k,v in new.items())
    expected = {"B":211051., "C":211669.}[arm]
    if abs(total-expected) > .05:
        fail("Original network cost parity failed %s %.3f" % (arm,total))
    base_route = routes(root/("sumo_"+arm)/"routes.rou.xml")
    shift = sum(base_route[k][0]-preferred[k] for k in preferred)
    insert = sum(float(v["departDelay"]) for v in new.values())
    duration = sum(float(v["duration"]) for v in new.values())
    if abs(total-(shift+insert+duration)) > .05:
        fail("Trip clock decomposition failed")
    record = {"arm": arm, "status": "VALID_REPLAY",
              "matched_drivers":len(new), "max_numeric_tripinfo_difference_s":worst,
              "network_cost_s":total, "requested_wait_s":shift,
              "insertion_delay_s":insert, "duration_s":duration,
              "source_network_sha256":digest(root/"source/network.net.xml"),
              "route_sha256":digest(root/("sumo_"+arm)/"routes.rou.xml"),
              "trace_sha256":{n:digest(out/n) for n in ("fcd.xml","vehroute.xml")}}
    write_json(out/"parity.json", record)
    return record

def fcd_frames(path):
    frames = {}
    ids = set()
    for _, el in ET.iterparse(path, events=("end",)):
        if el.tag != "timestep":
            continue
        t = float(el.get("time"))
        snap = {}
        for v in el.findall("vehicle"):
            vid = v.get("id")
            lane = v.get("lane")
            pos = v.get("pos")
            speed = v.get("speed")
            if vid is None or lane is None or pos is None or speed is None:
                fail("Missing mandatory FCD lane/pos/speed or id")
            snap[vid] = (lane, float(pos), float(speed))
            ids.add(vid)
        if t in frames:
            fail("Duplicate FCD timestep")
        frames[t] = snap
        el.clear()
    if len(ids) != 1000 or not frames:
        fail("Incomplete FCD vehicle coverage")
    return frames

def vehicle_exits(path, original_routes):
    root = ET.parse(path).getroot()
    result = {}
    for vehicle in root.findall("vehicle"):
        vid = vehicle.get("id")
        if vid not in original_routes or vid in result:
            fail("Unexpected or duplicated vehicle in vehroute output")
        route = vehicle.find(".//route")
        if route is None:
            fail("Missing vehroute edge exit series")
        edges = tuple(route.get("edges","").split())
        exits = [float(x) for x in route.get("exitTimes","").split()]
        if edges != original_routes[vid][1] or len(edges)!=len(exits):
            fail("Vehroute path or exit count changed for " + vid)
        result[vid] = exits
    if len(result)!=1000:
        fail("Incomplete vehroute exit times")
    return result

def external_freeflow(netpath):
    root = ET.parse(netpath).getroot()
    ff = {}
    for e in root.findall("edge"):
        if e.get("function")=="internal" or e.get("id","").startswith(":"):
            continue
        lane = e.find("lane")
        if lane is not None:
            ff[e.get("id")] = float(lane.get("length")) / float(lane.get("speed"))
    return ff

def first_divergences(fb,fc, shifted, shared):
    first = {}
    for t in sorted(set(fb)|set(fc)):
        b, c = fb.get(t,{}), fc.get(t,{})
        for vid in (set(b)|set(c)) - set(first):
            x, y = b.get(vid), c.get(vid)
            kind = None
            if x is None or y is None:
                kind = "presence_or_insertion"
            elif x[0] != y[0]:
                kind = "lane"
            elif abs(x[1]-y[1]) > 0.020001:
                kind = "lane_position"
            elif abs(x[2]-y[2]) > 0.020001:
                kind = "speed"
            if kind:
                first[vid]={"time_s":t,"vid":vid,
                            "group":"shifted" if vid in shifted else "unshifted",
                            "route_overlap":vid in shared,
                            "kind":kind,
                            "B":x, "C":y}
    events = sorted(first.values(),key=lambda x:(x["time_s"],x["vid"]))
    return {"first_shifted":next((e for e in events if e["group"]=="shifted"),None),
            "first_unshifted":next((e for e in events if e["group"]=="unshifted"),None),
            "first_30_global":events[:30],
            "first_30_unshifted":[e for e in events if e["group"]=="unshifted"][:30],
            "n_divergent_vehicles":len(first),
            "n_unshifted_divergent":sum(e["group"]=="unshifted" for e in events)}

def lane_exposure(frames):
    stopped=collections.Counter()
    slow=collections.Counter()
    for _,snap in frames.items():
        for _,(lane,pos,speed) in snap.items():
            if speed <= STOP_SPEED:
                stopped[lane]+=1
            elif speed < SLOW_SPEED:
                slow[lane]+=1
    return stopped,slow

def arrival_clock_summary(root, out_b, out_c, shifted, shared):
    ff=external_freeflow(root/"source/network.net.xml")
    rb, rc = routes(root/"sumo_B/routes.rou.xml"),routes(root/"sumo_C/routes.rou.xml")
    eb,ec=vehicle_exits(out_b/"vehroute.xml",rb),vehicle_exits(out_c/"vehroute.xml",rc)
    ib,ic=infos(out_b/"tripinfo.xml"),infos(out_c/"tripinfo.xml")
    response={}
    for arm,rts,exits,observed in (("B",rb,eb,ib),("C",rc,ec,ic)):
        groups={"shifted":[],"unshifted_route_overlap":[],"unshifted_nonoverlap":[]}
        records=[]
        for vid,(requested,edges) in rts.items():
            nominal=requested
            actual=float(observed[vid]["depart"])
            key=("shifted" if vid in shifted else
                 "unshifted_route_overlap" if vid in shared else "unshifted_nonoverlap")
            for edge,exit_t in zip(edges, exits[vid]):
                diff=actual-nominal
                groups[key].append(diff)
                if vid in shifted:
                    records.append({"id":vid,"edge":edge,"nominal_entry_s":round(nominal,3),
                                    "observed_entry_s":round(actual,3),"entry_error_s":round(diff,3)})
                nominal+=ff[edge]
                actual=exit_t
        response[arm]={"clock_errors_by_group":{
            k:{"n":len(v),"mean_observed_minus_nominal_entry_s":statistics.mean(v) if v else None,
                "median_s":statistics.median(v) if v else None,
                "p95_s":sorted(v)[int(.95*(len(v)-1))] if v else None}
            for k,v in groups.items()},
            "shifted_driver_edge_entry_examples":records[:60]}
    return response

def analyze(root, obs):
    b, c=obs/"B",obs/"C"
    gates={a:json.loads((obs/a/"parity.json").read_text()) for a in ("B","C")}
    if any(g["status"]!="VALID_REPLAY" for g in gates.values()):
        fail("Never analyze physical trace without strict original parity")
    preferred=trips(root)
    rb,rc=routes(root/"sumo_B/routes.rou.xml"),routes(root/"sumo_C/routes.rou.xml")
    shifted={v for v in preferred if rc[v][0] != rb[v][0]}
    shift_edges=set(e for vid in shifted for e in rb[vid][1])
    shared={v for v in preferred if v not in shifted and
            (shift_edges & set(rb[v][1]))}
    fb,fc=fcd_frames(b/"fcd.xml"),fcd_frames(c/"fcd.xml")
    d=first_divergences(fb,fc,shifted,shared)
    bs,bm=lane_exposure(fb)
    cs,cm=lane_exposure(fc)
    lane_deltas=[]
    for lane in set(bs)|set(cs)|set(bm)|set(cm):
        lane_deltas.append({"lane":lane,"B_stopped_samples":bs[lane],
                            "C_stopped_samples":cs[lane],
                            "delta_stopped_samples":cs[lane]-bs[lane],
                            "delta_slow_moving_samples":cm[lane]-bm[lane]})
    lane_deltas.sort(key=lambda x:-abs(x["delta_stopped_samples"]))
    ib,ic=infos(b/"tripinfo.xml"),infos(c/"tripinfo.xml")
    eligible=eligible_ids(preferred)
    harms={}
    for name, ids in (("all",set(preferred)),("shifted",shifted),
                     ("unshifted",set(preferred)-shifted),
                     ("eligible",eligible),("nonparticipants",set(preferred)-eligible),
                     ("unshifted_route_overlap",shared),
                     ("unshifted_no_route_overlap",set(preferred)-shifted-shared)):
        v=sorted(float(ic[k]["arrival"])-float(ib[k]["arrival"]) for k in ids)
        harms[name]={"n":len(v),"sum_C_minus_B_s":round(sum(v),6),
                     "mean_C_minus_B_s":round(statistics.mean(v),6) if v else None,
                     "median_s":statistics.median(v) if v else None,
                     "helped":sum(x<0 for x in v),"harmed":sum(x>0 for x in v),
                     "unchanged":sum(x==0 for x in v),
                     "harm_gt30_s":sum(x>30 for x in v)}
    if (harms["all"]["sum_C_minus_B_s"]!=618 or
        harms["unshifted"]["sum_C_minus_B_s"]!=614 or
        harms["nonparticipants"]["sum_C_minus_B_s"]!=543 or
        harms["all"]["harm_gt30_s"]!=205):
        fail("Original B/C fairness and network bridge did not reproduce")
    ordered=sorted((rc[k][0],k) for k in shifted)
    source_divergences=sorted(
        (float(ic[k]["depart"])-float(ib[k]["depart"]),k,
         float(ib[k]["depart"]),float(ic[k]["depart"]))
        for k in preferred if k not in shifted and
        float(ic[k]["depart"]) != float(ib[k]["depart"]))
    clock=arrival_clock_summary(root,b,c,shifted,shared)
    result={"status":"VALID_REPLAY_DESCRIPTIVE_ONLY",
            "research_question":"Can earliest B/C effects on unshifted traffic be observed and localized?",
            "first_requested_C_shift":{"time_s":ordered[0][0],"vehicle":ordered[0][1]},
            "first_unshifted_insertion_change":(
                {"vehicle":source_divergences[0][1],
                 "B_actual_depart_s":source_divergences[0][2],
                 "C_actual_depart_s":source_divergences[0][3]}
                if source_divergences else None),
            "n_unshifted_insertion_changed":len(source_divergences),
            "fcd_first_differences":d,
            "lane_stopped_speed_threshold_mps":STOP_SPEED,
            "lane_slow_moving_upper_threshold_mps":SLOW_SPEED,
            "fcd_sample_count_B":sum(len(f) for f in fb.values()),
            "fcd_sample_count_C":sum(len(f) for f in fc.values()),
            "total_stopped_samples_B":sum(bs.values()),
            "total_stopped_samples_C":sum(cs.values()),
            "total_slow_moving_samples_B":sum(bm.values()),
            "total_slow_moving_samples_C":sum(cm.values()),
            "top_25_lane_stopped_sample_deltas":lane_deltas[:25],
            "physical_clock_comparison":clock,
            "matched_driver_harms":harms,
            "historical_parity":gates,
            "caveat":"Timing/overlap/queuing associations are descriptive, not unique causal mediation; one inspected seed; sample-time limited."}
    write_json(obs/"t1_passive_physical_diagnostic.json",result)
    rows=[
      "# T1 authorized passive B/C replay — machine-derived descriptive checkpoint",
      "",
      "**Status:** Strict original tripinfo/exception parity PASS for both B and C.",
      "**Scientific interpretation:** Earliest observed physical differences, NOT proof of a unique causal bottleneck.",
      "",
      "## First observed events",
      "",
      "- First requested C delay: "+str(result["first_requested_C_shift"]),
      "- Earliest matched unshifted actual insertion change: "+str(result["first_unshifted_insertion_change"]),
      "- First FCD difference in shifted drivers: "+str(d["first_shifted"]),
      "- First FCD difference in unshifted drivers: "+str(d["first_unshifted"]),
      "- Total vehicles with differing FCD samples: "+str(d["n_divergent_vehicles"]),
      "",
      "## Primary network and fairness",
      "",
      "| Cohort | n | C−B network-s | Harm >30s |",
      "|---|---:|---:|---:|"
    ]
    for k in ("all","shifted","unshifted","eligible","nonparticipants",
              "unshifted_route_overlap","unshifted_no_route_overlap"):
        v=harms[k]
        rows.append("|%s|%s|%s|%s|"%(k,v["n"],v["sum_C_minus_B_s"],v["harm_gt30_s"]))
    rows.extend(["","## Stationary FCD lane-sample changes (descriptive, step-aligned)",
                 "","| Lane | B samples | C samples | Δ samples |","|---|---:|---:|---:|"])
    for v in lane_deltas[:15]:
        rows.append("|%s|%d|%d|%d|"%(v["lane"],v["B_stopped_samples"],
                   v["C_stopped_samples"],v["delta_stopped_samples"]))
    rows.extend(["","## Interpretation limits",
       "- Per-driver FCD differences can precede a downstream traffic effect; do not infer specific causal bottleneck from chronology alone.",
       "- FCD speed samples and vehroute edge exits do not measure exact substep turn priority or causal gap acceptance.",
       "- The originally frozen forecast and B/C schedule remain failed development evidence; no policy reoptimization or new model.",
       "- Details, first-30 chronology, downstream clock errors, full fairness and hashes are in t1_passive_physical_diagnostic.json.",
       ""])
    (obs/"t1_passive_checkpoint.md").write_text("\n".join(rows))
    print(json.dumps({"status":result["status"],
          "first_shifted":d["first_shifted"],"first_unshifted":d["first_unshifted"],
          "harms":harms["all"]},sort_keys=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=("preflight","run","parity","analyze"))
    ap.add_argument("--root",default="t1-development")
    ap.add_argument("--out",default="observed")
    ap.add_argument("--arm",choices=("B","C"))
    a=ap.parse_args()
    root=Path(a.root)
    out=Path(a.out)
    if a.mode=="preflight":
        x=verify_inputs(root,require_binary=True)
        write_json(out/"source_preflight.json",x)
        print(json.dumps({"status":"SOURCE_AND_PINNED_BINARY_PASS","n":x["n"],
                          "shifted":len(x["shifts"]),"sumo":x["sumo_version"]}))
    elif a.mode=="run":
        if not a.arm:
            fail("Replay requires --arm B or C")
        replay(root,a.arm,out/a.arm)
    elif a.mode=="parity":
        if not a.arm:
            fail("Parity requires --arm")
        print(json.dumps(audit_arm(root,a.arm,out/a.arm),sort_keys=True))
    else:
        analyze(root,out)
if __name__=="__main__":
    main()
