#!/usr/bin/env python3
"""G3 J0/J1: parse SUMO native vehicle exitTimes, preserving internal links.

These are SUMO step-resolution events; do not claim continuous crossing times.
Never reuse a vehroute-output.internal route as input to SUMO.
"""
import argparse, collections, csv, json
import xml.etree.ElementTree as ET


def extract_events(root):
    events, vehicles, issues = [], {}, []
    for v in root.findall("vehicle"):
        vid = v.get("id")
        choices = v.findall("./route") or v.findall("./routeDistribution/route")
        if not vid or not choices or len(choices) != 1:
            issues.append({"vehicle":vid, "issue":"missing_or_multiple_route_elements"})
            continue
        route = choices[0]
        edges = route.get("edges","").split()
        raw_times = route.get("exitTimes","").split()
        if not edges or len(edges)!=len(raw_times):
            issues.append({"vehicle":vid, "issue":"edge_exittime_count_mismatch",
                           "edges":len(edges),"exit_times":len(raw_times)})
            continue
        depart = float(v.get("depart"))
        arrive = float(v.get("arrival"))
        previous=depart
        external=[]
        internal_n=0
        for ordinal,(edge,raw) in enumerate(zip(edges,raw_times)):
            t=float(raw)
            if t<previous-1e-8:
                issues.append({"vehicle":vid,"issue":"nonmonotone_exit_times","ordinal":ordinal})
                break
            kind="internal" if edge.startswith(":") else "external"
            if kind=="external": external.append(edge)
            else:internal_n+=1
            events.append(dict(vehicle=vid,ordinal=ordinal,edge=edge,kind=kind,
                               enter_at_prior_exit_s=previous,exit_s=t,
                               interval_s=round(t-previous,6),
                               status="native_step_resolution_not_continuous_crossing"))
            previous=t
        else:
            vehicles[vid]={"departure_s":depart,"arrival_s":arrive,
                           "last_exit_s":previous,"external_route":external,
                           "internal_links":internal_n}
    return events, vehicles, issues


def summarize(vehroute,planned,tripinfo,events_out,report_out):
    root=ET.parse(vehroute).getroot()
    events,vehicles,issues=extract_events(root)
    original_routes={}
    for v in ET.parse(planned).getroot().findall("vehicle"):
        original_routes[v.get("id")]=v.find("route").get("edges").split()
    baseline={}
    for v in ET.parse(tripinfo).getroot().findall("tripinfo"):
        vid=v.get("id")
        baseline[vid]={k:float(v.get(k)) for k in ("depart","arrival","duration","waitingTime")}
    missing=set(original_routes)-set(vehicles)
    unknown=set(vehicles)-set(original_routes)
    route_mismatch=[]
    value_mismatch=[]
    for vid,row in vehicles.items():
        if vid in original_routes and row["external_route"]!=original_routes[vid]:
            route_mismatch.append(vid)
        if vid in baseline:
            for kind,v in (("depart",row["departure_s"]),("arrival",row["arrival_s"])):
                if abs(v-baseline[vid][kind])>1e-6:
                    value_mismatch.append((vid,kind,v,baseline[vid][kind]))
        else:value_mismatch.append((vid,"missing_tripinfo",None,None))
    fields=["vehicle","ordinal","edge","kind","enter_at_prior_exit_s","exit_s","interval_s","status"]
    with open(events_out,"w",newline="") as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(events)
    report={
        "vehicles_with_parsed_events":len(vehicles),
        "planned_vehicles":len(original_routes),
        "tripinfo_vehicles":len(baseline),
        "native_event_rows":len(events),
        "internal_event_rows":sum(e["kind"]=="internal" for e in events),
        "missing_vehicles":sorted(missing)[:30],
        "unexpected_vehicles":sorted(unknown)[:30],
        "external_route_mismatch":route_mismatch[:30],
        "depart_arrival_mismatch":value_mismatch[:30],
        "parse_issues":issues[:30],
        "event_time_semantics":"SUMO simulation-step exit time; entering next link is inferred from prior exit, not an independent crossing measurement",
        "source":"vehroute-output.exit-times + vehroute-output.internal",
        "status":"diagnostic_not_holdout"
    }
    with open(report_out,"w") as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    if (len(vehicles)!=1000 or len(original_routes)!=1000 or
          len(baseline)!=1000 or issues or missing or unknown or
          route_mismatch or value_mismatch or report["internal_event_rows"]==0):
        raise RuntimeError("Native route-timing integrity gate failed")


def main():
    p=argparse.ArgumentParser()
    for x in ("vehroute","planned-routes","tripinfo","events","report"):
        p.add_argument("--"+x,required=True)
    a=p.parse_args()
    summarize(a.vehroute,a.planned_routes,a.tripinfo,a.events,a.report)

if __name__=="__main__":main()
