#!/usr/bin/env python3
"""Independently replay original search-time counter reads from gzip event stream."""
import argparse,collections,csv,gzip,json,math,xml.etree.ElementTree as ET

def verify(events_path,routes_path,audit_report):
    counter=collections.Counter()
    totals=collections.Counter()
    decisions={}
    current_ordinal=-1
    revisions=0
    pressure=None
    errors=[]
    def bad(msg):
        if len(errors)<25:errors.append(msg)
    with gzip.open(events_path,"rt",encoding="utf8") as f:
        for line in f:
            event=json.loads(line)
            typ=event["event_type"]
            totals[typ]+=1
            ordinal=event["decision_ordinal"]
            vid=event["vehicle"]
            if typ=="decision_start":
                if ordinal!=current_ordinal+1:bad("Nonsequential decision ordinal: "+str(ordinal))
                current_ordinal=ordinal
                if vid in decisions:bad("Repeated vehicle: "+str(vid))
                decisions[vid]={"ordinal":ordinal,"lookup_n":0,"updated_n":0}
            if ordinal!=current_ordinal or vid not in decisions:
                bad("Event attributed outside current decision "+str(typ))
                continue
            if typ=="search_start":
                pressure=event["pressure"]
            if typ=="edge_lookup":
                key=(event["to_edge"],int(event["lookup_bin"]))
                expected=counter[key]
                if event["assignment_revision"]!=revisions:bad("Wrong counter revision at lookup")
                if event["prior_assigned_count"]!=expected:
                    bad("Counter lookup diverged: "+str((vid,key,expected,event["prior_assigned_count"])))
                ff=event["freeflow_edge_s"];cap=event["capacity_proxy"]
                if cap<=0 or pressure is None:bad("Uninitialized pressure or nonpositive capacity")
                else:
                    calc=ff*(1+pressure*expected/cap)+event["junction_proxy_s"]
                    if abs(calc+event["heap_cost_s"]-event["new_label_cost_s"])>1e-7:
                        bad("Original search cost identity not satisfied")
                    if abs(event["congestion_surcharge_s"]-ff*pressure*expected/cap)>1e-8:
                        bad("Inconsistent congestion surcharge")
                prev=event["previous_best_s"]
                accepted=(prev is None or event["new_label_cost_s"]<prev-1e-8)
                if event["accepted_for_heap"]!=accepted:bad("Heap relax bool mismatch")
                decisions[vid]["lookup_n"]+=1
            if typ=="assignment_update":
                key=(event["edge"],int(event["lookup_bin"]))
                prev=counter[key]
                if event["prior_assigned_count"]!=prev:
                    bad("Counter changed before assignment "+str((vid,key,prev)))
                if event["new_assigned_count"]!=prev+1:
                    bad("Counter update changed policy "+str((vid,key)))
                revisions+=1
                if event["assignment_revision"]!=revisions:
                    bad("Assignment revision not increasing")
                counter[key]+=1
                decisions[vid]["updated_n"]+=1
            if typ=="decision_end" and decisions[vid]["updated_n"]!=event["updated_edges"]:
                bad("Decision assignment updates mismatch route length")
    route_vehicles={}
    root=ET.parse(routes_path).getroot()
    for v in root.findall("vehicle"):
        route_vehicles[v.get("id")]=v.find("route").get("edges").split()
    if len(route_vehicles)!=1000 or len(decisions)!=1000:bad("Wrong vehicle count")
    for vid,route in route_vehicles.items():
        if vid not in decisions or decisions[vid]["updated_n"]!=len(route):
            bad("Assigned route length does not match emitted counter updates "+vid)
    if totals["decision_start"]!=1000 or totals["decision_end"]!=1000:
        bad("Missing decision events")
    if totals["search_start"]!=1000 or totals["search_end"]!=1000:
        bad("Missing search events")
    if totals["assignment_update"]!=sum(map(len,route_vehicles.values())):
        bad("Unexpected total counter assignments")
    report={"status":"PASS" if not errors else "FAIL",
            "event_counts":dict(totals),"vehicles":len(decisions),
            "assigned_edges":revisions,"distinct_occupied_edge_time_bins":len(counter),
            "edge_cost_reads_observed":totals["edge_lookup"],
            "first_errors":errors,"limits":[
               "Original search-time prior assignment counts are not measured physical occupancy.",
               "This checks counter values and unchanged route assignment, not learned traffic forecast accuracy.",
               "Unchosen candidate routes have no simulated counterfactual travel outcomes."]}
    with open(audit_report,"w") as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!="limits"},indent=2))
    if errors:raise RuntimeError("G3 search event audit failed: "+str(errors[:3]))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--events",required=True);p.add_argument("--routes",required=True)
    p.add_argument("--report",required=True)
    a=p.parse_args()
    verify(a.events,a.routes,a.report)
