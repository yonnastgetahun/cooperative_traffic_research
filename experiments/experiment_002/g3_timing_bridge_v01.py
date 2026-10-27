#!/usr/bin/env python3
"""Compare native SUMO exit-step entry times with FCD first-observed entries."""
import argparse,csv,json,collections,xml.etree.ElementTree as ET,statistics

def csv_data(path):
    with open(path) as f:return list(csv.DictReader(f))

def main():
    p=argparse.ArgumentParser()
    for field in ["trace","events","fcd","report","out"]:
        p.add_argument("--"+field,required=True)
    a=p.parse_args()
    traces=collections.defaultdict(list);native=collections.defaultdict(list)
    for r in csv_data(a.trace):traces[r["vehicle"]].append(r)
    for r in csv_data(a.events):
        if r["kind"]=="external":native[r["vehicle"]].append(r)
    front=collections.defaultdict(list)
    for _,node in ET.iterparse(a.fcd,events=("end",)):
        if node.tag!="timestep":continue
        t=float(node.get("time"))
        for v in node.findall("vehicle"):
            lane=v.get("lane","")
            if not lane:raise RuntimeError("Missing FCD lane")
            front[v.get("id")].append((t,lane.rsplit("_",1)[0],lane.startswith(":")))
        node.clear()
    output=[];miss=[];changes=collections.Counter()
    for vid,rs in sorted(traces.items()):
        rs.sort(key=lambda x:int(x["route_index"]))
        f=[];internal=False
        for t,e,k in front[vid]:
            if k:internal=True;continue
            if not f or f[-1][1]!=e or internal:f.append((t,e))
            internal=False
        n=native[vid]
        if [x["edge"] for x in rs]!=[x["edge"] for x in n] or [x["edge"] for x in rs]!=[x[1] for x in f]:
            miss.append(vid);continue
        for i,(r,event,sample) in enumerate(zip(rs,n,f)):
            native_t=float(event["enter_at_prior_exit_s"]);front_t=sample[0]
            d=round(front_t-native_t,6)
            changes[str(d)]+=1
            output.append((vid,i,r["edge"],native_t,front_t,d,float(r["predicted_entry_s"]),float(r["freeflow_entry_s"])))
    with open(a.out,"w",newline="") as f:
        w=csv.writer(f);w.writerow(["vehicle","route_index","edge","native_entry_s","FCD_entry_s","FCD_minus_native_s","timeaware_predicted_s","freeflow_predicted_s"]);w.writerows(output)
    def errors(j):
        values=[row[3]-row[j] for row in output]
        return dict(n=len(values),bias_s=statistics.mean(values),mae_s=statistics.mean(abs(x) for x in values))
    def fcd_errors(j):
        values=[row[4]-row[j] for row in output]
        return dict(n=len(values),bias_s=statistics.mean(values),mae_s=statistics.mean(abs(x) for x in values))
    report=dict(planned_edges=sum(len(x) for x in traces.values()),matched=len(output),missing_vehicle_ids=miss,
                observed_delta_counts=dict(changes),native_timeaware=errors(6),native_freeflow=errors(7),
                FCD_timeaware=fcd_errors(6),FCD_freeflow=fcd_errors(7),
                first_edge_count=sum(row[1]==0 for row in output),
                FCD_later_over_one_step=sum(row[5]>1.0 for row in output),
                FCD_earlier_over_one_step=sum(row[5]<-1.0 for row in output),
                provenance="simulation-step native predecessor exit; first FCD front sample; development only",
                interpretation="two observation conventions on same realized chosen route; not occupancy calibration")
    with open(a.report,"w") as f:json.dump(report,f,indent=2)
    if miss or report["matched"]!=report["planned_edges"]:raise RuntimeError("Unmatched ordered route visits")
if __name__=="__main__":main()
