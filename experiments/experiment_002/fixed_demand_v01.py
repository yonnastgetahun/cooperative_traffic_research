#!/usr/bin/env python3
"""Same seeded SUMO OD pairs across 200/600/1200s demand windows."""
import argparse, json, os, random, sys, xml.etree.ElementTree as ET
sys.path.insert(0,os.path.join(os.environ.get("SUMO_HOME","/usr/share/sumo"),"tools"))
import sumolib

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--net",required=True);p.add_argument("--out",required=True)
    p.add_argument("--manifest",required=True)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    p.add_argument("--vehicles",type=int,default=1000)
    a=p.parse_args()
    if a.window not in (200,600,1200) or a.vehicles!=1000:
        raise ValueError("Only prespecified 1000-trip congestion regimes are supported")
    random.seed(a.seed)
    net=sumolib.net.readNet(a.net)
    edges=[e for e in net.getEdges() if not e.isSpecial() and e.allows("passenger")]
    root=ET.Element("trips")
    for i in range(a.vehicles):
        for _ in range(1000):
            origin,dest=random.sample(edges,2)
            path,_=net.getShortestPath(origin,dest,vClass="passenger")
            if path and len(path)>=2:break
        else:raise RuntimeError("Cannot find legal origin/destination")
        ET.SubElement(root,"trip",id=f"veh{i:04d}",
            depart=f"{i*a.window/a.vehicles:.3f}",
            **{"from":origin.getID(),"to":dest.getID()})
    ET.ElementTree(root).write(a.out,encoding="utf-8",xml_declaration=True)
    with open(a.manifest,"w") as f:
        json.dump({"seed":a.seed,"window_seconds":a.window,"vehicles":a.vehicles,
                   "purpose":"physical occupancy and junction measurement development",
                   "no_holdout":True,"route_policy":"original_time_aware_v0.1",
                   "bin_seconds":30,"fcd_step_seconds":1},f,indent=2)

if __name__=="__main__":main()
