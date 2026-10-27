#!/usr/bin/env python3
"""Stream every actual time_aware search event from the default-off observation hook.

Do not use this output as measured physical occupancy. The emitted search
events record prior route ASSIGNMENT counts and heap candidate evaluation.
"""
import argparse, collections, gzip, json, math, os, sys
import time_aware as policy

def valid_json(x):
    if isinstance(x,dict):
        return {k:valid_json(v) for k,v in x.items()}
    if isinstance(x,float) and not math.isfinite(x):return None
    return x

def main():
    p=argparse.ArgumentParser()
    for name in ("net","trips","out","audit","manifest","events","summary"):
        p.add_argument("--"+name,required=True)
    p.add_argument("--bin-seconds",type=int,default=30)
    p.add_argument("--pressure",type=float,default=1.)
    p.add_argument("--detour-percent",type=float,default=.10)
    p.add_argument("--detour-seconds",type=float,default=30.)
    p.add_argument("--distance-percent",type=float,default=.15)
    a=p.parse_args()
    counts=collections.Counter()
    old_sink=policy.G3_SEARCH_TRACE_SINK
    old_argv=sys.argv
    if old_sink is not None:raise RuntimeError("Search event sink already active")
    with gzip.open(a.events,"wt",encoding="utf8",compresslevel=3) as stream:
        def sink(event):
            counts[event["event_type"]]+=1
            stream.write(json.dumps(valid_json(event),sort_keys=True,allow_nan=False)+"\n")
        policy.G3_SEARCH_TRACE_SINK=sink
        sys.argv=["time_aware.py","--net",a.net,"--trips",a.trips,
                  "--out",a.out,"--audit",a.audit,"--manifest",a.manifest,
                  "--bin-seconds",str(a.bin_seconds),"--pressure",str(a.pressure),
                  "--detour-percent",str(a.detour_percent),
                  "--detour-seconds",str(a.detour_seconds),
                  "--distance-percent",str(a.distance_percent)]
        try:policy.main()
        finally:
            policy.G3_SEARCH_TRACE_SINK=old_sink
            sys.argv=old_argv
    summary={"status":"development_only_search_trace",
             "search_events":dict(counts),
             "total_events":sum(counts.values()),
             "exact_event_source":"original_time_aware_search_default_off_sink_enabled",
             "observed_quantity":"prior route assignment count, not physical occupancy"}
    with open(a.summary,"w") as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
    for t in ("search_start","search_end","decision_start","decision_end","guardrail_decision"):
        if counts[t]!=1000:raise RuntimeError(f"Expected 1000 {t}, got {counts[t]}")
    if counts["edge_lookup"]<1000 or counts["assignment_update"]<1000:
        raise RuntimeError("Search instrumentation has insufficient events")

if __name__=="__main__":main()
