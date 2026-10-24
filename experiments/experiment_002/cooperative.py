#!/usr/bin/env python3
"""Experimental advance-demand cooperative routing, not real-time rerouting."""
import argparse, collections, heapq, json, math, xml.etree.ElementTree as ET
import sumolib

def path_for(net, origin, dest, load, penalty):
    # Edge graph: successors are connected passenger-legal edges.
    edges={e.getID():e for e in net.getEdges() if not e.isSpecial() and e.allows("passenger")}
    q=[(0.0,origin)]; dist={origin:0.0}; prev={}
    while q:
        cost,u=heapq.heappop(q)
        if cost>dist[u]+1e-9: continue
        if u==dest: break
        for v in sorted(e.getID() for e in edges[u].getOutgoing() if e.getID() in edges):
            e=edges[v]
            base=e.getLength()/max(e.getSpeed(),0.1)
            # Penalize anticipated occupancy; no observed/future simulation data.
            weight=base*(1.0+penalty*load[v])
            nd=cost+weight
            if nd<dist.get(v,float("inf"))-1e-9:
                dist[v]=nd;prev[v]=u;heapq.heappush(q,(nd,v))
    if dest not in dist: raise ValueError(f"No legal route {origin} -> {dest}")
    result=[dest]
    while result[-1]!=origin: result.append(prev[result[-1]])
    return list(reversed(result))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--net",required=True);p.add_argument("--trips",required=True)
    p.add_argument("--out",required=True);p.add_argument("--metrics",required=True)
    p.add_argument("--penalty",type=float,default=0.08)
    a=p.parse_args()
    net=sumolib.net.readNet(a.net)
    trips=ET.parse(a.trips).getroot().findall("trip")
    root=ET.Element("routes")
    ET.SubElement(root,"vType",id="passenger",vClass="passenger")
    load=collections.Counter();route_counts=collections.Counter()
    for t in sorted(trips,key=lambda x:(float(x.get("depart")),x.get("id"))):
        route=path_for(net,t.get("from"),t.get("to"),load,a.penalty)
        vehicle=ET.SubElement(root,"vehicle",id=t.get("id"),type="passenger",depart=t.get("depart"))
        ET.SubElement(vehicle,"route",edges=" ".join(route))
        route_counts[len(route)]+=1
        for edge in route:load[edge]+=1
    ET.ElementTree(root).write(a.out,encoding="utf-8",xml_declaration=True)
    with open(a.metrics,"w") as f:
        json.dump({"algorithm":"sequential announced-trip edge-load penalty","penalty":a.penalty,"vehicles":len(trips),"route_length_histogram":dict(route_counts),"advance_trip_knowledge":True},f,indent=2)
    if len(trips)!=1000:raise RuntimeError("Expected 1000 trips")

if __name__=="__main__":main()
