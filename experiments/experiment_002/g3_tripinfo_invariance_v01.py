#!/usr/bin/env python3
"""Strict comparison of original and observation-augmented SUMO tripinfo."""
import argparse,json,xml.etree.ElementTree as ET
FIELDS=("depart","arrival","duration","waitingTime","timeLoss","departDelay")

def read(path):
    root=ET.parse(path).getroot()
    ans={}
    for t in root.findall("tripinfo"):
        vid=t.get("id")
        if not vid or vid in ans:raise RuntimeError("Missing/duplicate tripinfo ID")
        ans[vid]=t.attrib
    return ans

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--baseline",required=True);p.add_argument("--observed",required=True)
    p.add_argument("--report",required=True);a=p.parse_args()
    baseline=read(a.baseline);observed=read(a.observed)
    mismatch=[]
    for vid in sorted(set(baseline)|set(observed)):
        if vid not in baseline or vid not in observed:
            mismatch.append({"vehicle":vid,"field":"missing_tripinfo"});continue
        for field in FIELDS:
            first=baseline[vid].get(field);second=observed[vid].get(field)
            if (first is None)!=(second is None):
                mismatch.append({"vehicle":vid,"field":field,"baseline":first,"observed":second})
            elif first is not None and abs(float(first)-float(second))>1e-6:
                mismatch.append({"vehicle":vid,"field":field,"baseline":first,"observed":second})
    summary={"status":"PASS" if not mismatch and len(baseline)==1000 else "FAIL",
             "baseline_trips":len(baseline),"observed_trips":len(observed),
             "checked_fields":FIELDS,"differing_vehicle_field_count":len(mismatch),
             "first20_mismatches":mismatch[:20]}
    with open(a.report,"w") as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
    if summary["status"]!="PASS":raise RuntimeError("Observation changed simulated trip outcomes")

if __name__=="__main__":main()
