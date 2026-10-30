#!/usr/bin/env python3
"""Prospective Experiment 004 search adapter; no future SUMO observations.

Zero correction delegates exactly to the frozen original search. Nonzero
correction carries route ordinal as state, retaining multiple path labels.
"""
import heapq
from dataclasses import dataclass
@dataclass(frozen=True)
class Label:
    cost:float
    edge:str
    ordinal:int
    path:tuple

def search(origin,dest,departure,edges,adj,occupancy,bin_s,pressure,offset_s=0.0,per_edge_s=0.0):
    from time_aware import search as original,freeflow
    if offset_s==0.0 and per_edge_s==0.0:
        return original(origin,dest,departure,edges,adj,occupancy,bin_s,pressure)
    if bin_s<=0 or offset_s<0 or per_edge_s<0:raise ValueError("Invalid prospective calibration parameters")
    first=freeflow(edges[origin])
    queue=[(first,0,(origin,))]
    # Explicit (edge, ordinal, lookup-bin) states; no single-best-edge pruning.
    best={}
    while queue:
        cost,k,path=heapq.heappop(queue)
        u=path[-1]
        state=(u,k,int((departure+cost+offset_s+per_edge_s*k)//bin_s))
        if cost>best.get(state,float("inf"))+1e-9:continue
        if u==dest:return list(path),cost
        for v in adj[u]:
            if v in path:continue
            next_ordinal=k+1
            entry=departure+cost+offset_s+per_edge_s*next_ordinal
            time_bin=int(entry//bin_s)
            e=edges[v]
            ff=freeflow(e)
            cap=max(1.0,e.getLength()*max(e.getLaneNumber(),1)/7.5)
            surcharge=ff*pressure*(occupancy[(v,time_bin)]/cap)
            turn=1.0 if len(adj[u])>1 else 0.0
            new=cost+ff+surcharge+turn
            next_state=(v,next_ordinal,int((departure+new+offset_s+per_edge_s*next_ordinal)//bin_s))
            if new<best.get(next_state,float("inf"))-1e-9:
                best[next_state]=new
                heapq.heappush(queue,(new,next_ordinal,path+(v,)))
    raise RuntimeError("No legal prospective route")
