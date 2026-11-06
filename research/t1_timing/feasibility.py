#!/usr/bin/env python3
"""T1 development-only timing feasibility. No confirmatory seed access.

This is a fixed-route, assigned-demand timing proxy; NOT SUMO prediction
validation, an E1-v3 estimator, a human acceptance experiment, or a policy GO.
"""
import argparse
import collections
import hashlib
import json
import math
import sys
from pathlib import Path

SHIFTS = (0, 10, 20, 30)
BIN_S = 10
CONSENT_ALLOWANCE = 5.0
EPS_B = 0.5
EPS_C = 0.05
MAX_SWEEPS = 60


def ordering(seed, vid):
    return hashlib.sha256(f"T1:{seed}:{vid}".encode()).hexdigest(), vid


def eligible_id(seed, vid):
    # For exactly N/2 participants, rank by this independent hash.
    return hashlib.sha256(f"T1:eligible:{seed}:{vid}".encode()).hexdigest(), vid


class Schedule:
    """A finite atomic congestion game over (edge,10-second bin) resources.

    Edge arrivals are fixed nominal free-flow offsets from *requested*
    departure, not predictions of actual congestion-dependent entry clocks.
    All route paths and edges must be prespecified, identical between B/C.
    """
    def __init__(self, records, edge_info, seed, phase=0.0):
        self.seed = seed
        self.phase = phase
        self.records = {r["id"]: r for r in records}
        if len(self.records) != len(records):
            raise ValueError("Nonunique vehicle IDs")
        self.ids = sorted(self.records)
        self.eligible = set(sorted(self.ids, key=lambda vid: eligible_id(seed, vid))[:len(self.ids)//2])
        self.order = sorted(self.eligible, key=lambda vid: ordering(seed, vid))
        self.edge_info = edge_info  # edge -> (freeflow_seconds, capacity_proxy)
        if any(ff <= 0 or cap <= 0 for ff, cap in edge_info.values()):
            raise ValueError("Invalid edge model")
        self.profiles = {}
        for vid in self.ids:
            r = self.records[vid]
            if not r["route"] or len(set(r["route"])) != len(r["route"]):
                raise ValueError("Invalid/loopy route for " + vid)
            if any(e not in edge_info for e in r["route"]):
                raise ValueError("Unknown route edge")
            for offset in SHIFTS if vid in self.eligible else (0,):
                clock = float(r["preferred"]) + offset
                p = collections.Counter()
                for e in r["route"]:
                    b = math.floor((clock + phase) / BIN_S)
                    p[(e, b)] += 1
                    clock += edge_info[e][0]
                if max(p.values()) != 1:
                    raise ValueError("Repeated edge-time resource")
                self.profiles[(vid, offset)] = p
        self.offsets = {vid: 0 for vid in self.ids}
        self.q = collections.Counter()
        for vid in self.ids:
            self.q.update(self.profiles[(vid, 0)])

    def available(self, vid):
        return SHIFTS if vid in self.eligible else (0,)

    def profile(self, vid, offset):
        return self.profiles[(vid, offset)]

    def post_count(self, key, old, new):
        n = self.q[key] - old.get(key, 0) + new.get(key, 0)
        if n < 0:
            raise AssertionError("Negative forecast count")
        return n

    def personal(self, vid, candidate):
        old = self.profile(vid, self.offsets[vid])
        new = self.profile(vid, candidate)
        cost = float(candidate)
        for (eid, b), copies in new.items():
            ff, cap = self.edge_info[eid]
            cost += copies * ff * (1.0 + self.post_count((eid, b), old, new) / cap)
        return cost

    def own_consent(self, vid, candidate):
        # Counterfactual at current others' announcements, own delay reset to 0.
        return self.personal(vid, candidate) <= self.personal(vid, 0) + CONSENT_ALLOWANCE + 1e-9

    def global_delta(self, vid, candidate):
        oldshift = self.offsets[vid]
        if candidate == oldshift:
            return 0.0
        old = self.profile(vid, oldshift)
        new = self.profile(vid, candidate)
        result = float(candidate - oldshift)
        for key in old.keys() | new.keys():
            eid, b = key
            ff, cap = self.edge_info[eid]
            q0 = self.q[key]
            q1 = self.post_count(key, old, new)
            result += ff * (q1 + q1*q1/cap - q0 - q0*q0/cap)
        return result

    def potential(self):
        # Exact Rosenthal potential for unilateral own-cost differences,
        # because each shift selects a fixed set of edge-bin resources.
        result = sum(self.offsets.values())
        for (eid, _), q in self.q.items():
            ff, cap = self.edge_info[eid]
            result += ff * (q + q*(q+1)/(2*cap))
        return result

    def predicted_total(self):
        result = sum(self.offsets.values())
        for (eid, _), q in self.q.items():
            ff, cap = self.edge_info[eid]
            result += ff * (q + q*q/cap)
        return result

    def apply(self, vid, offset):
        current = self.offsets[vid]
        if current == offset:
            return
        if offset not in self.available(vid):
            raise ValueError("Ineligible shift")
        old, new = self.profile(vid, current), self.profile(vid, offset)
        for key, n in old.items():
            self.q[key] -= n
        self.q.update(new)
        if any(v < 0 for v in self.q.values()):
            raise AssertionError("Negative counter after update")
        self.offsets[vid] = offset

    def residual(self, policy):
        worst = 0.0
        for vid in self.order:
            current = self.offsets[vid]
            current_cost = self.personal(vid, current)
            for offset in self.available(vid):
                if not self.own_consent(vid, offset):
                    continue
                gain = (current_cost - self.personal(vid, offset)) if policy == "B" else -self.global_delta(vid, offset)
                worst = max(worst, gain)
        return worst

    def optimize(self, policy):
        if policy not in ("B", "C"):
            raise ValueError("Only B/C can optimize")
        tol = EPS_B if policy == "B" else EPS_C
        history = []
        maxregret = None
        for sweep in range(1, MAX_SWEEPS+1):
            changed = 0
            start_phi = self.potential() if policy == "B" else self.predicted_total()
            for vid in self.order:
                curr = self.offsets[vid]
                options = []
                for candidate in self.available(vid):
                    if not self.own_consent(vid, candidate):
                        continue
                    value = self.personal(vid, candidate) if policy == "B" else self.global_delta(vid, candidate)
                    options.append((value, 0 if candidate == curr else 1, candidate))
                if not options:
                    raise AssertionError("Own-zero must always satisfy consent")
                best = min(options)
                old_value = self.personal(vid, curr) if policy == "B" else 0.0
                if best[2] != curr and old_value - best[0] > tol + 1e-9:
                    self.apply(vid, best[2])
                    changed += 1
            end_phi = self.potential() if policy == "B" else self.predicted_total()
            if end_phi > start_phi + 1e-6:
                raise AssertionError("Optimized objective unexpectedly increased")
            maxregret = self.residual(policy)
            history.append({"pass": sweep, "moves": changed,
                            "objective": round(end_phi, 6), "max_residual_gain_s": round(maxregret, 6)})
            if maxregret <= tol + 1e-9:
                break
            if changed == 0:
                raise AssertionError("No moves but feasible improvement remains")
        stable = maxregret <= tol + 1e-9
        return {"policy": policy, "passes": len(history), "stable": stable,
                "max_residual_gain_s": maxregret, "moves": sum(h["moves"] for h in history),
                "shifted": sum(x > 0 for x in self.offsets.values()),
                "shift_seconds": sum(self.offsets.values()),
                "predicted_total_s": self.predicted_total(),
                "history": history}

    def initial_sensitivity(self):
        # Crucially exclude chosen departure shifts when measuring the
        # *traffic forecast* signal. A raw total cost spread of >=30 seconds
        # is automatic from the 0/10/20/30s schedule options and proves nothing.
        affected, traffic_substantive, traffic_benefit, net_improving = 0, 0, 0, 0
        spreads = []
        for vid in self.order:
            profiles = {tuple(sorted(self.profile(vid, k).items())) for k in SHIFTS}
            total = [self.personal(vid, k) for k in SHIFTS]
            traffic = [total[j] - sh for j, sh in enumerate(SHIFTS)]
            spread = max(traffic) - min(traffic)
            affected += len(profiles) > 1
            traffic_substantive += spread > 0.5
            traffic_benefit += min(traffic[1:]) < traffic[0] - 0.5
            net_improving += min(total[1:]) < total[0] - 0.5
            spreads.append(spread)
        return {
            "eligible": len(self.order),
            "different_edge_bin_footprints": affected,
            "traffic_cost_spread_gt_0p5_s": traffic_substantive,
            "traffic_benefit_over_zero_gt_0p5_s": traffic_benefit,
            "total_cost_improvement_over_zero_gt_0p5_s": net_improving,
            "mean_traffic_cost_spread_s": sum(spreads)/max(1,len(spreads)),
            "max_traffic_cost_spread_s": max(spreads) if spreads else 0
        }

    def audit(self):
        fresh = collections.Counter()
        for vid, offset in self.offsets.items():
            if vid not in self.eligible and offset:
                raise AssertionError("Shifted nonparticipant")
            fresh.update(self.profile(vid, offset))
        if any(fresh[k] != self.q[k] for k in fresh.keys() | self.q.keys()):
            raise AssertionError("Occupancy mismatch")
        return {"counts_match": True, "profiles": len(self.profiles)}


def prove_potential():
    sample = [
        {"id": "a", "preferred": 0., "route": ("e1", "e2")},
        {"id": "b", "preferred": 1., "route": ("e1", "e2")},
        {"id": "c", "preferred": 2., "route": ("e1", "e2")},
        {"id": "d", "preferred": 3., "route": ("e1", "e2")},
    ]
    m = Schedule(sample, {"e1": (6., 1.), "e2": (8., 1.)}, 2101)
    for vid in m.eligible:
        for shift in (10,20,30):
            before = m.potential()
            own_before = m.personal(vid, m.offsets[vid])
            own_after = m.personal(vid, shift)
            m.apply(vid, shift)
            if abs((m.potential()-before) - (own_after-own_before)) > 1e-7:
                raise AssertionError("Expected exact potential identity")
            m.apply(vid, 0)
    return True


def development(seed, out, scientific, simulate):
    # Only an already-examined development seed is allowed, never unseen.
    if seed != 2101:
        raise ValueError("T1 feasibility only permits previously inspected development seed 2101")
    root = Path(out)
    if root.exists():
        raise ValueError("Fail closed: output path already exists")
    root.mkdir(parents=True)
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "experiments" / "experiment_007"))
    import run_v01 as old
    net, data, edges, adj, _, _, common_routes, _ = old.setup(seed, root/"source", scientific)
    edge_info = {eid: (old.time_aware.freeflow(e), old.cap(e)) for eid, e in edges.items()}
    records = [{"id": x["id"], "preferred": x["depart"], "route": tuple(common_routes[x["id"]])}
               for x in data]
    by_id = {x["id"]: x for x in records}
    phase_results = []
    selected = None
    for phase in (0.0, 2.5, 5.0, 7.5):
        base = Schedule(records, edge_info, seed, phase)
        sensitivity = base.initial_sensitivity()
        b, c = Schedule(records, edge_info, seed, phase), Schedule(records, edge_info, seed, phase)
        report_b = b.optimize("B")
        report_c = c.optimize("C")
        phase_results.append({"phase_seconds": phase, "initial_sensitivity": sensitivity,
                              "B": report_b, "C": report_c, "B_audit": b.audit(), "C_audit": c.audit(),
                              "different_B_C_shift_assignments":
                                  sum(b.offsets[v] != c.offsets[v] for v in b.ids)})
        if phase == 0:
            selected = (b, c)
    main = phase_results[0]
    max_prevalence = [r["initial_sensitivity"]["traffic_cost_spread_gt_0p5_s"] for r in phase_results]
    summary = {"classification": "DEVELOPMENT_ONLY_NO_INDEPENDENT_CONFIRMATION",
               "demand_seed": seed, "routes_frozen_across_arms": True,
               "sources": {"route_policy": "Experiment 007 independent traffic-aware I", "forecast": "T1 10s nominal-edge assigned demand"},
               "potential_identity_unit_check": prove_potential(),
               "phase_results": phase_results,
               "phase_signal_spread_counts": max_prevalence,
               "feasibility": {
                   "B_converged_all_phases": all(p["B"]["stable"] for p in phase_results),
                   "C_converged_all_phases": all(p["C"]["stable"] for p in phase_results),
                   "offset_profiles_distinguished_all_phases": all(p["initial_sensitivity"]["different_edge_bin_footprints"] == len(selected[0].order) for p in phase_results),
                   "nontrivial_traffic_signal_all_phases": min(max_prevalence) >= 1,
                   "phase_robust_outcome_not_established": True,
                   "forecast_real_world_accuracy_not_established": True
               }}
    if simulate:
        b, c = selected
        arms = {"A": {v: 0 for v in b.ids}, "B": b.offsets, "C": c.offsets}
        originals = {t["id"]: t["depart"] for t in data}
        realized = {}
        for arm, shifts in arms.items():
            shifted = sorted([dict(t, depart=t["depart"]+shifts[t["id"]]) for t in data],
                             key=lambda t: (t["depart"], t["id"]))
            if any(a["depart"] > b["depart"] for a, b in zip(shifted, shifted[1:])):
                raise AssertionError("SUMO requested-departure records are not chronologically ordered")
            # SUMO route files MUST be ordered by the *modified requested departure*.
            # The prior failed development attempt iterated original preferred
            # departure order after shifts and SUMO omitted late listed vehicles.
            obs = old.simulate(root, f"sumo_{arm}", common_routes, shifted, net, seed, adj)
            wanted = {v: obs[v]["total"] + shifts[v] for v in b.ids}
            if len(wanted) != 1000 or any(not math.isfinite(x) for x in wanted.values()):
                raise AssertionError("Invalid SUMO completion or elapsed time")
            total = sum(wanted.values())
            realized[arm] = {
                "all_driver_preferred_to_arrival_s": total,
                "mean_per_driver_s": total / len(wanted),
                "requested_predeparture_shift_s": sum(shifts.values()),
                "sumo_insertion_delay_s": sum(x["depart_delay"] for x in obs.values()),
                "in_network_trip_duration_s": sum(x["duration"] for x in obs.values()),
                "nonparticipant_mean_s": sum(wanted[v] for v in b.ids if v not in b.eligible)/(len(b.ids)-len(b.eligible)),
                "all_completed": True
            }
            if abs(total - (realized[arm]["requested_predeparture_shift_s"] +
                            realized[arm]["sumo_insertion_delay_s"] +
                            realized[arm]["in_network_trip_duration_s"])) > .05:
                raise AssertionError("Total cost decomposition mismatch")
        summary["realized_dev_only"] = realized
        summary["dev_C_minus_B_mean_s"] = realized["C"]["mean_per_driver_s"] - realized["B"]["mean_per_driver_s"]
    (root/"feasibility_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2101)
    parser.add_argument("--out", required=True)
    parser.add_argument("--scientific", default="scientific")
    parser.add_argument("--simulate", action="store_true")
    args = parser.parse_args()
    s = development(args.seed, args.out, args.scientific, args.simulate)
    print(json.dumps({"feasibility": s["feasibility"],
                      "initial_10s_signal": s["phase_signal_spread_counts"],
                      "B_passes": [p["B"]["passes"] for p in s["phase_results"]],
                      "C_passes": [p["C"]["passes"] for p in s["phase_results"]],
                      "realized_dev_only": s.get("realized_dev_only")},
                     sort_keys=True))
