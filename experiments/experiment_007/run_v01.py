#!/usr/bin/env python3
"""Experiment 007 frozen-objective two-test implementation.
All future realized SUMO outcomes are evaluation-only, never inputs to routing.
The static time-bin externality proxy is not actual physical queue measurement.
"""
import argparse
import collections
import csv
import hashlib
import heapq
import json
import math
import os
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, os.path.join(os.environ.get("SUMO_HOME", "/usr/share/sumo"), "tools"))
import sumolib
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiment_002"))
import time_aware

PROBE_SEEDS = tuple(range(4101, 4106))
POLICY_SEEDS = tuple(range(4201, 4211))
DEV_SEED = 2101
BIN = 30
OFFSET = 4.053135104279146
PER_EDGE = 11.524898884412591
N = 1000
WINDOW = 200
T9 = 2.2621571627409915


def invoke(cmd, logfile=None):
    if logfile:
        with Path(logfile).open("w") as f:
            result = subprocess.run([str(x) for x in cmd], stdout=f, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError("Command failed (%s), see %s" % (result.returncode, logfile))
    else:
        subprocess.run([str(x) for x in cmd], check=True)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(seed, out, scientific):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    net = out / "network.net.xml"
    trips = out / "trips.xml"
    invoke(["netgenerate", "--grid", "--grid.number", "10", "--grid.length", "200",
            "--output-file", net], out / "netgenerate.log")
    invoke([sys.executable, Path(scientific) / "experiments/experiment_002/fixed_demand_v01.py",
            "--net", net, "--out", trips, "--manifest", out / "demand.json",
            "--seed", seed, "--window", WINDOW], out / "demand-stage.log")
    return net, trips


def scheduled(trips):
    xs = sorted(ET.parse(trips).getroot().findall("trip"),
                key=lambda t: (float(t.get("depart")), t.get("id")))
    assert len(xs) == N and len({t.get("id") for t in xs}) == N
    return [{"id": t.get("id"), "depart": float(t.get("depart")),
             "origin": t.get("from"), "dest": t.get("to")} for t in xs]


def noise(vehicle, variant, eid):
    h = hashlib.blake2b(("%s:%s:%s" % (vehicle, variant, eid)).encode(), digest_size=8).digest()
    return int.from_bytes(h, "big") / (2**64 - 1)


def dijkstra(origin, dest, edges, adj, vehicle, variant):
    costs = {origin: time_aware.freeflow(edges[origin])}
    q = [(costs[origin], origin)]
    previous = {}
    while q:
        cost, u = heapq.heappop(q)
        if cost > costs[u] + 1e-9:
            continue
        if u == dest:
            break
        for v in adj[u]:
            ff = time_aware.freeflow(edges[v])
            w = ff if variant == 0 else ff * (1 + 0.25 * noise(vehicle, variant, v))
            value = cost + w
            if value < costs.get(v, float("inf")) - 1e-9:
                costs[v] = value
                previous[v] = u
                heapq.heappush(q, (value, v))
    if dest not in costs:
        raise ValueError("No route from %s to %s" % (origin, dest))
    path = [dest]
    while path[-1] != origin:
        path.append(previous[path[-1]])
    return tuple(reversed(path))


def candidates(trips, edges, adj):
    result = {}
    for t in trips:
        paths = []
        for variant in (0, 1, 2, 3):
            p = dijkstra(t["origin"], t["dest"], edges, adj, t["id"], variant)
            if p not in paths:
                paths.append(p)
        base = paths[0]
        btime = sum(time_aware.freeflow(edges[e]) for e in base)
        bdist = sum(edges[e].getLength() for e in base)
        maxextra = min(30.0, .1 * btime)
        allowed = [p for p in paths
                   if sum(time_aware.freeflow(edges[e]) for e in p) <= btime + maxextra + 1e-9
                   and sum(edges[e].getLength() for e in p) <= 1.15 * bdist + 1e-9]
        assert allowed and allowed[0] == base
        result[t["id"]] = allowed
    return result


def footprint(path, depart, edges):
    clock = depart
    out = collections.Counter()
    for k, eid in enumerate(path):
        b = int((clock + OFFSET + PER_EDGE * k) // BIN)
        out[(eid, b)] += 1
        clock += time_aware.freeflow(edges[eid])
    return out


def cap(edge):
    return max(1., edge.getLength() * max(edge.getLaneNumber(), 1) / 7.5)


def edge_total(q, eid, edges):
    ff = time_aware.freeflow(edges[eid])
    return ff * (q + q * q / cap(edges[eid]))


def own_time(path, profile, occupancy, edges):
    return sum(n * time_aware.freeflow(edges[eid]) * (1 + occupancy[(eid, b)] / cap(edges[eid]))
               for (eid, b), n in profile.items())


def delta(old, new, depart, q, edges):
    if old == new:
        return {"total": 0., "self": 0., "external": 0.}
    a = footprint(old, depart, edges)
    b = footprint(new, depart, edges)
    changed = b - a
    changed.subtract(a - b)
    # Counter subtraction above is arithmetic; retain signed values.
    dq = {key: b.get(key, 0) - a.get(key, 0) for key in set(a) | set(b)}
    dc = 0.
    for (eid, bin_), diff in dq.items():
        before = q[(eid, bin_)]
        after = before + diff
        if after < 0:
            raise RuntimeError("Negative forecast occupancy")
        dc += edge_total(after, eid, edges) - edge_total(before, eid, edges)
    before_own = own_time(old, a, q, edges)
    modified = collections.Counter(q)
    for key, diff in dq.items():
        modified[key] += diff
    after_own = own_time(new, b, modified, edges)
    ds = after_own - before_own
    return {"total": dc, "self": ds, "external": dc - ds}


def replace(q, old, new, depart, edges):
    if old == new:
        return
    for key, n in footprint(old, depart, edges).items():
        q[key] -= n
        if q[key] < 0:
            raise RuntimeError("Negative occupancy after replacement")
    q.update(footprint(new, depart, edges))


def count_assignments(routes, byid, edges):
    q = collections.Counter()
    for vid, route in routes.items():
        q.update(footprint(route, byid[vid]["depart"], edges))
    return q


def generate_routes(data, candidate, edges):
    byid = {t["id"]: t for t in data}
    # Fully announced independent initial assignment with common forecast.
    route = {t["id"]: candidate[t["id"]][0] for t in data}
    q = count_assignments(route, byid, edges)
    for t in data:
        vid = t["id"]
        current = route[vid]
        scored = [(delta(current, p, t["depart"], q, edges)["self"], p) for p in candidate[vid]]
        bestval, best = min(scored, key=lambda x: (x[0], x[1]))
        if bestval < -1e-8:
            replace(q, current, best, t["depart"], edges)
            route[vid] = best
    return route


def policy_routes(base, data, candidate, edges, kind):
    if kind not in ("I", "S"):
        raise ValueError("Invalid policy")
    byid = {t["id"]: t for t in data}
    routes = dict(base)
    occupancy = count_assignments(routes, byid, edges)
    changed = []
    for t in data:
        vid = t["id"]
        if int(vid[-4:]) % 2:  # odd indices are nonparticipants
            continue
        cur = routes[vid]
        options = []
        for p in candidate[vid]:
            d = delta(cur, p, t["depart"], occupancy, edges)
            if d["self"] <= 30. + 1e-8:
                options.append((d[kind == "S" and "total" or "self"], p, d))
        if not options:
            raise ValueError("Missing baseline route candidate")
        score, picked, impact = min(options, key=lambda x: (x[0], x[1]))
        if picked != cur and score < -1e-8:
            replace(occupancy, cur, picked, t["depart"], edges)
            routes[vid] = picked
            changed.append({"vehicle": vid, "predicted": impact})
    return routes, changed


def write_routes(routes, trips, out):
    root = ET.Element("routes")
    ET.SubElement(root, "vType", id="passenger", vClass="passenger")
    for t in trips:
        vid = t["id"]
        v = ET.SubElement(root, "vehicle", id=vid, type="passenger",
                          depart=f'{t["depart"]:.3f}')
        ET.SubElement(v, "route", edges=" ".join(routes[vid]))
    ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=True)


def verify_routes(routes, data, adj):
    if len(routes) != N or set(routes) != {x["id"] for x in data}:
        raise RuntimeError("Missing/extra assignments")
    for t in data:
        path = routes[t["id"]]
        if not path or path[0] != t["origin"] or path[-1] != t["dest"] or len(set(path)) != len(path):
            raise RuntimeError("Invalid origin, destination or loop for " + t["id"])
        if any(v not in adj[u] for u, v in zip(path, path[1:])):
            raise RuntimeError("Disconnected assigned route")


def simulate(root, name, routes, data, net, seed, adj):
    output = Path(root) / name
    output.mkdir(parents=True)
    verify_routes(routes, data, adj)
    xml = output / "routes.rou.xml"
    write_routes(routes, data, xml)
    invoke(["sumo", "-n", net, "-r", xml,
            "--tripinfo-output", output / "tripinfo.xml",
            "--statistic-output", output / "statistics.xml",
            "--collision-output", output / "collisions.xml",
            "--seed", seed, "--no-step-log", "true", "--log", output / "sumo.log"],
           output / "sumo-stage.log")
    return tripinfo(output / "tripinfo.xml", data)


def tripinfo(path, data):
    planned = {t["id"]: t["depart"] for t in data}
    rows = ET.parse(path).getroot().findall("tripinfo")
    if len(rows) != N or len({v.get("id") for v in rows}) != N:
        raise RuntimeError("Incomplete or duplicate tripinfo; reject completed-only means")
    r = {}
    for t in rows:
        vid = t.get("id")
        if vid not in planned:
            raise RuntimeError("Unrecognized completed ID")
        actual_depart = float(t.get("depart"))
        duration = float(t.get("duration"))
        arrival = float(t.get("arrival", actual_depart + duration))
        if abs(arrival - (actual_depart + duration)) > .03:
            raise RuntimeError("SUMO arrival/depart/duration inconsistency")
        delay = actual_depart - planned[vid]
        if delay < -0.03:
            raise RuntimeError("Vehicle departed before its scheduled departure")
        r[vid] = {"total": arrival-planned[vid], "duration": duration,
                  "depart_delay": delay, "waiting": float(t.get("waitingTime", "0")),
                  "time_loss": float(t.get("timeLoss", "0"))}
    if set(r) != set(planned):
        raise RuntimeError("Trip identities mismatch")
    return r


def setup(seed, out, scientific):
    out = Path(out)
    netpath, tripspath = prepare(seed, out, scientific)
    net = sumolib.net.readNet(str(netpath))
    edges, adj = time_aware.build_graph(net)
    data = scheduled(tripspath)
    candidate = candidates(data, edges, adj)
    base = generate_routes(data, candidate, edges)
    i, changes_i = policy_routes(base, data, candidate, edges, "I")
    verify_routes(i, data, adj)
    return netpath, data, edges, adj, candidate, base, i, changes_i


def select_probes(routes, data, candidate, edges):
    byid = {t["id"]: t for t in data}
    q = count_assignments(routes, byid, edges)
    options = []
    for t in data:
        vid = t["id"]
        if int(vid[-4:]) % 2:
            continue
        cur = routes[vid]
        for alt in candidate[vid]:
            if alt == cur:
                continue
            d = delta(cur, alt, t["depart"], q, edges)
            if d["self"] <= 30.:
                options.append((d["external"], vid, alt, d))
    if len({x[1] for x in options}) < 4:
        raise RuntimeError("Cannot find four distinct eligible probes")
    sorted_opts = sorted(options, key=lambda x: (x[0], x[1], x[2]))
    targets = [sorted_opts[0], sorted_opts[-1],
               min(options, key=lambda x: (abs(x[0]), x[1], x[2])),
               sorted_opts[len(sorted_opts)//2]]
    selected = []
    used = set()
    for target in targets:
        possible = sorted(options, key=lambda x: (abs(x[0]-target[0]), x[1], x[2]))
        chosen = next((x for x in possible if x[1] not in used), None)
        if chosen is None:
            raise RuntimeError("Probe distinctness failure")
        selected.append(chosen)
        used.add(chosen[1])
    return selected


def probe(seed, out, scientific):
    if seed not in PROBE_SEEDS:
        raise ValueError("Not a frozen Test A seed")
    out = Path(out)
    attempt = {"experiment": "007", "test": "A", "seed": seed, "status": "FAILED"}
    try:
        net, data, edges, adj, cand, base, i, _ = setup(seed, out, scientific)
        picks = select_probes(i, data, cand, edges)
        baseline_obs = simulate(out, "I", i, data, net, seed, adj)
        probe_records = []
        for idx, (ext, vid, alt, d) in enumerate(picks):
            new = dict(i)
            new[vid] = alt
            obs = simulate(out, "probe%d"%idx, new, data, net, seed, adj)
            diffs = {v: obs[v]["total"]-baseline_obs[v]["total"] for v in baseline_obs}
            observed_total = sum(diffs.values())
            observed_self = diffs[vid]
            probe_records.append({"id": idx, "vehicle": vid, "predicted": d,
                "realized": {"total": observed_total, "self": observed_self,
                             "external": observed_total-observed_self}})
        # Joint bundle is the first two singleton probes, preselected without SUMO outcomes.
        bundle = dict(i)
        q = count_assignments(bundle, {t["id"]:t for t in data}, edges)
        bundle_pred_total = 0.
        for _,vid,alt,_ in picks[:2]:
            t = next(t for t in data if t["id"] == vid)
            move = delta(bundle[vid], alt, t["depart"], q, edges)
            bundle_pred_total += move["total"]
            replace(q, bundle[vid], alt, t["depart"], edges)
            bundle[vid] = alt
        bobs = simulate(out, "bundle", bundle, data, net, seed, adj)
        realized_bundle = sum(bobs[v]["total"]-baseline_obs[v]["total"] for v in baseline_obs)
        (out/"probe-results.json").write_text(json.dumps({
            "seed": seed, "records":probe_records, "bundle":{
                "predicted_total":bundle_pred_total, "realized_total":realized_bundle,
                "isolated_predicted_total_sum":sum(p["predicted"]["total"] for p in probe_records[:2]),
                "isolated_realized_total_sum":sum(p["realized"]["total"] for p in probe_records[:2])
            }}, indent=2)+"\n")
        attempt.update(status="COMPLETE", n_probes=len(picks), n_runs=6,
                       tripinfo_all_complete=True, demand_sha256=digest(out/"trips.xml"))
    except Exception as ex:
        attempt["error"] = repr(ex)
    (out/"attempt.json").write_text(json.dumps(attempt, indent=2)+"\n")
    if attempt["status"] != "COMPLETE":
        raise RuntimeError(attempt["error"])
    print(json.dumps(attempt))


def policy(seed, out, scientific):
    if seed not in POLICY_SEEDS:
        raise ValueError("Not a frozen Test B seed")
    out=Path(out)
    attempt={"experiment":"007","test":"B","seed":seed,"status":"FAILED"}
    try:
        net, data, edges, adj, cand, base, i, changes_i = setup(seed, out, scientific)
        s, changes_s = policy_routes(base, data, cand, edges, "S")
        for vid in i:
            if int(vid[-4:])%2 and i[vid]!=s[vid]:
                raise RuntimeError("Nonparticipant route is not invariant")
        ii=simulate(out, "I", i, data, net, seed, adj)
        ss=simulate(out, "S", s, data, net, seed, adj)
        def mean(vals, metric):
            return statistics.mean(x[metric] for x in vals.values())
        match={v: ss[v]["total"]-ii[v]["total"] for v in ii}
        groups={name:[val for vid,val in match.items() if
                  (name=="all" or ((int(vid[-4:])%2==0)==(name=="participants")))]
                 for name in ("all","participants","nonparticipants")}
        group_metrics={name:{"count":len(arr),"harmed":sum(x>0 for x in arr),
                             "severe_gt30":sum(x>30 for x in arr),
                             "p95_harm":quantile(arr,.95),
                             "mean_S_minus_I":statistics.mean(arr)}
                       for name,arr in groups.items()}
        (out/"policy-results.json").write_text(json.dumps({
            "seed":seed,"I_mean_total":mean(ii,"total"),"S_mean_total":mean(ss,"total"),
            "I_mean_duration":mean(ii,"duration"),"S_mean_duration":mean(ss,"duration"),
            "I_mean_depart_delay":mean(ii,"depart_delay"),
            "S_mean_depart_delay":mean(ss,"depart_delay"),
            "I_mean_waiting":mean(ii,"waiting"),"S_mean_waiting":mean(ss,"waiting"),
            "changed_routes":sum(i[v]!=s[v] for v in i),
            "groups":group_metrics},indent=2)+"\n")
        attempt.update(status="COMPLETE", n_runs=2, demand_sha256=digest(out/"trips.xml"))
    except Exception as ex:
        attempt["error"]=repr(ex)
    (out/"attempt.json").write_text(json.dumps(attempt,indent=2)+"\n")
    if attempt["status"]!="COMPLETE":
        raise RuntimeError(attempt["error"])
    print(json.dumps(attempt))


def quantile(x,p):
    a=sorted(x)
    return a[max(0, math.ceil(len(a)*p)-1)]


def interval(vals):
    assert len(vals)==10
    m=statistics.mean(vals)
    h=T9*statistics.stdev(vals)/math.sqrt(10)
    return {"mean":m,"ci95":[m-h,m+h],"seeds":10}


def aggregate_a(root, out, gate_path):
    records=[]
    for seed in PROBE_SEEDS:
        directory=Path(root)/("exp007-probe-%s"%seed)
        status=json.loads((directory/"attempt.json").read_text())
        if status["status"]!="COMPLETE" or status["seed"]!=seed:
            raise RuntimeError("Missing/incomplete Test A seed %s"%seed)
        records.append(json.loads((directory/"probe-results.json").read_text()))
    material=[]
    for seed in records:
        for p in seed["records"]:
            actual=p["realized"]["external"]
            if abs(actual)>=10:
                material.append({"seed":seed["seed"],"predicted":p["predicted"]["external"],
                                 "realized":actual,"correct":(p["predicted"]["external"]*actual>0)})
    concordance=sum(x["correct"] for x in material)/len(material) if material else None
    gate=(len(material)>=10 and concordance is not None and concordance>=.6)
    output={"experiment":"007","test":"A","seed_records":records,"material_count":len(material),
            "sign_concordance":concordance,"material_probes":material,
            "independent_unit":"seed","gate_pass":gate,
            "gate_criteria":"at least 10 |realized externality|>=10 network seconds; >=60% sign concordance; all 5 complete; bundles measured"}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(output,indent=2)+"\n")
    Path(gate_path).write_text("true" if gate else "false")
    print(json.dumps({"gate_pass":gate,"material_n":len(material),"concordance":concordance}))


def aggregate_b(root,out):
    rows=[]
    for seed in POLICY_SEEDS:
        folder=Path(root)/("exp007-policy-%s"%seed)
        status=json.loads((folder/"attempt.json").read_text())
        if status["status"]!="COMPLETE" or status["seed"]!=seed:
            raise RuntimeError("Missing or invalid Test B seed %s"%seed)
        rows.append(json.loads((folder/"policy-results.json").read_text()))
    diffs=[r["I_mean_total"]-r["S_mean_total"] for r in rows]
    ci=interval(diffs)
    n=sum(r["groups"]["all"]["count"] for r in rows)
    harmed=sum(r["groups"]["all"]["harmed"] for r in rows)
    severe=sum(r["groups"]["all"]["severe_gt30"] for r in rows)
    nnon=sum(r["groups"]["nonparticipants"]["count"] for r in rows)
    snon=sum(r["groups"]["nonparticipants"]["severe_gt30"] for r in rows)
    flags={"lower_ci_gt_zero":ci["ci95"][0]>0,"mean_at_least_2_seconds":ci["mean"]>=2.,
           "severe_fraction_at_most_10pct":severe/n<=.1,
           "nonparticipant_severe_at_most_10pct":snon/nnon<=.1,
           "harmed_fraction_at_most_50pct":harmed/n<=.5}
    decision=("GO: conditional synthetic network improvement and fairness criteria met"
              if all(flags.values()) else
              "NO-GO: demonstrated slower-than-I" if ci["ci95"][1]<0 else
              "INCONCLUSIVE efficacy or JOINT FAIRNESS/UTILITY GO NOT MET")
    output={"experiment":"007","test":"B","primary_I_minus_S_total_s":ci,
            "fairness":{"matched":n,"harmed":harmed,"harmed_fraction":harmed/n,
                        "severe_gt30":severe,"severe_fraction":severe/n,
                        "nonparticipant_count":nnon,"nonparticipant_severe":snon,
                        "nonparticipant_severe_fraction":snon/nnon},
            "flags":flags,"decision":decision,"seed_pairs":rows,
            "unit":"independent demand seed; driver IDs for matching only"}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(output,indent=2)+"\n")
    with (Path(out).parent/"exp007-policy-seed-summary.csv").open("w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["seed","I_mean_total_s","S_mean_total_s","I_minus_S_s","changed_routes",
                    "severe_all","severe_nonparticipants"])
        for r in rows:
            w.writerow([r["seed"],r["I_mean_total"],r["S_mean_total"],
                        r["I_mean_total"]-r["S_mean_total"],r["changed_routes"],
                        r["groups"]["all"]["severe_gt30"],
                        r["groups"]["nonparticipants"]["severe_gt30"]])
    print(json.dumps({"decision":decision,"effect":ci,"flags":flags}))


def development(out,scientific):
    out=Path(out)
    net, data, edges, adj, candidate, base, i, _=setup(DEV_SEED,out,scientific)
    s, _=policy_routes(base,data,candidate,edges,"S")
    verify_routes(s,data,adj)
    assert len(candidate)==N
    assert any(i[v]!=s[v] for v in i) or all(len(x)==1 for x in candidate.values())
    for vid in i:
        if int(vid[-4:])%2:
            assert i[vid]==s[vid]
    q=count_assignments(i,{t["id"]:t for t in data},edges)
    for t in data[:30]:
        p=candidate[t["id"]][0]
        assert abs(delta(p,p,t["depart"],q,edges)["total"])<1e-8
    write_routes(i,data,out/"I-development.rou.xml")
    write_routes(s,data,out/"S-development.rou.xml")
    print(json.dumps({"development_seed":DEV_SEED,"n":N,
        "alternative_vehicle_count":sum(len(x)>1 for x in candidate.values()),
        "changed_I_S":sum(i[v]!=s[v] for v in i)}))


def main():
    a=argparse.ArgumentParser()
    a.add_argument("task",choices=("dev","probe","policy","aggregate-a","aggregate-b"))
    a.add_argument("--seed",type=int)
    a.add_argument("--out",required=True)
    a.add_argument("--scientific",default="scientific")
    a.add_argument("--root")
    a.add_argument("--gate")
    args=a.parse_args()
    if args.task=="dev":development(args.out,args.scientific)
    elif args.task=="probe":probe(args.seed,args.out,args.scientific)
    elif args.task=="policy":policy(args.seed,args.out,args.scientific)
    elif args.task=="aggregate-a":aggregate_a(args.root,args.out,args.gate)
    else:aggregate_b(args.root,args.out)

if __name__=="__main__":
    main()
