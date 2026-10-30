#!/usr/bin/env python3
"""Compare zero-correction adapter with original on frozen Experiment 001 decisions.

Uses original time_aware.main routing and a patched search delegate; outputs
route-file equality and audit hashes, without running new SUMO traffic.
"""
import argparse,hashlib,json,os,sys,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"experiment_002"))
import time_aware as policy
from prospective_search_adapter_v01 import search as adapter
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(net,trips,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    original=policy.search
    def patched(*args):return original(*args)  # Zero correction must delegate to captured unpatched search.
    def one(label,search):
        policy.search=search
        saved=sys.argv
        sys.argv=["time_aware.py","--net",str(net),"--trips",str(trips),
            "--out",str(out/f"{label}.rou.xml"),"--audit",str(out/f"{label}.csv"),
            "--manifest",str(out/f"{label}.json")]
        try:policy.main()
        finally:sys.argv=saved;policy.search=original
    one("original",original)
    one("adapter-zero",patched)
    eq_routes=(out/"original.rou.xml").read_bytes()==(out/"adapter-zero.rou.xml").read_bytes()
    eq_audit=(out/"original.csv").read_bytes()==(out/"adapter-zero.csv").read_bytes()
    result=dict(zero_correction_route_bytes_equal=eq_routes,zero_correction_audit_bytes_equal=eq_audit,
        original_route_sha256=digest(out/"original.rou.xml"),
        adapter_route_sha256=digest(out/"adapter-zero.rou.xml"))
    (out/"equivalence.json").write_text(json.dumps(result,indent=2)+"\n")
    if not eq_routes or not eq_audit:raise SystemExit("Adapter-only control required: zero-correction differs")
    print(json.dumps(result))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--net",required=True);p.add_argument("--trips",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();run(a.net,a.trips,a.out)
