#!/usr/bin/env python3
"""Review-only pure production adapters for frozen M3 scientific protocol.

No CLI, simulation, demand generation, network or side effects.
Use original frozen R3 audit and R4 mean_ci_if_ten, never new science.
"""
import hashlib
import math
import statistics

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
SUMO_IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
REGIMES=(200,600,1200)
N_VEHICLES=1000
N_SEEDS=10

class Ineligible(Exception):
    """Missing or invalid evidence; no silent dropping or imputation."""

def require(condition,reason):
    if not condition:raise Ineligible(reason)

def sha256_ok(s):
    return isinstance(s,str) and len(s)==64 and all(c in "0123456789abcdef" for c in s)

def od_pair_fingerprint(trips):
    """SHA-256 over ordered (vehicle ID, origin, destination), excluding departures."""
    ordered=[tuple(x) for x in trips]
    require(len(ordered)==N_VEHICLES,"Missing or extra OD pairs")
    require(all(len(x)==3 and all(isinstance(y,str) and y for y in x)
                for x in ordered),"Malformed OD record")
    require(len({x[0] for x in ordered})==N_VEHICLES,
            "Duplicate OD vehicle ID")
    data="\n".join("\t".join(x) for x in ordered)+"\n"
    return hashlib.sha256(data.encode("utf8")).hexdigest()

def assess_frozen_r3(raw,seed,window):
    """Validate the unchanged frozen R3 audit result with no new thresholds."""
    require(window in REGIMES,"Unknown congestion window")
    require(raw.get("seed")==seed and raw.get("window_seconds")==window,
            "R3 source seed/window mismatch")
    require(raw.get("matched_trip_count")==N_VEHICLES,
            "Incomplete original trip observations")
    require(raw.get("route_population_invariant") is True
            and raw.get("tripinfo_invariant") is True,
            "Route/trip invariance failed")
    teleport=raw.get("reported_teleports")
    require(isinstance(teleport,dict),"Missing native teleport evidence")
    require(teleport.get("teleport_state")=="ZERO_CONFIRMED"
            and teleport.get("teleports_total")==0,
            "Unknown or positive native teleport evidence")
    fcd=raw.get("reported_FCD")
    require(isinstance(fcd,dict)
            and fcd.get("distinct_observed_vehicles")==N_VEHICLES
            and fcd.get("timestep_count",0)>0,
            "Missing FCD coverage")
    require(not fcd.get("structural_anomalies")
            and fcd.get("within_trip_disappearance_count")==0,
            "Unexplained FCD gap/duplicate/vehicle disappearance")
    native=raw.get("native_edge_bins")
    require(isinstance(native,dict) and native.get("native_bins",0)>0,
            "Missing native edgeData")
    codes=native.get("status_counts",{})
    require(codes.get("MISSING_NATIVE_SAMPLED_SECONDS",0)==0
            and codes.get("MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES",0)==0,
            "Missing required occupied road-bin metric")
    require(raw.get("exception_gate")=="PASS_FOR_THIS_REPLAY"
            and not raw.get("scientific_exception_counts"),
            "Original frozen R3 exception gate not clear")
    return dict(status="ELIGIBLE_BY_FROZEN_R3_RULES",seed=seed,
        window_seconds=window,completed_vehicles=N_VEHICLES,
        teleports_reported=0,
        partial_native_bins=codes.get("PARTIAL_NATIVE_BIN",0),
        empty_native_bins=codes.get("EMPTY_NATIVE_EDGE_NO_SAMPLES",0),
        frozen_original_status=raw.get("status"))

def seed_record(seed,window,metrics,r3,bridge,source):
    """Preserve matched original per-seed/scenario timing and R3 eligibility."""
    eligible=assess_frozen_r3(r3,seed,window)
    require(bridge.get("planned_edges")==bridge.get("matched")
            and bridge.get("matched",0)>=N_VEHICLES
            and not bridge.get("missing_vehicle_ids"),
            "Incomplete native/FCD ordered road-entry matching")
    require(metrics.get("vehicles")==N_VEHICLES
            and metrics.get("edge_traversals")==bridge["matched"],
            "Timing error cohort not identical to planned vehicles")
    require(metrics.get("frozen_scientific_commit")==FROZEN_SHA,
            "Timing metric source code is not frozen")
    t=metrics.get("timing_metrics",{})
    require("timeaware" in t and "freeflow" in t,
            "Missing one of the frozen same-route comparators")
    require(t["timeaware"].get("n")==bridge["matched"]
            and t["freeflow"].get("n")==bridge["matched"],
            "Forecast comparators were scored on different road visits")
    mae_t=float(t["timeaware"]["mae_s"])
    mae_f=float(t["freeflow"]["mae_s"])
    bias=float(t["timeaware"]["bias_s"])
    require(all(map(math.isfinite,(mae_t,mae_f,bias)))
            and min(mae_t,mae_f)>=0,
            "Invalid seed timing errors")
    benefit=mae_f-mae_t
    require(abs(benefit-float(metrics["paired_MAE_benefit_ff_minus_timeaware_s"]))<0.0001,
            "Frozen seed-level paired timing score has changed")
    require(source.get("scientific_commit")==FROZEN_SHA
            and source.get("sumo_image")==SUMO_IMAGE,
            "Wrong original source commit or SUMO immutable image")
    for k in ("network_sha256","trips_sha256","routes_sha256","od_pair_sha256"):
        require(sha256_ok(source.get(k)),"Missing or invalid "+k)
    require(source.get("route_audit_byte_identical") is True,
            "Original route/audit invariance was not established")
    if "matches_preexisting_M2_forecast_errors" in metrics:
        require(metrics["matches_preexisting_M2_forecast_errors"] is True,
                "Previously inspected development timing reference mismatch")
    return dict(status=eligible["status"],
        seed=seed,window_seconds=window,vehicles=N_VEHICLES,
        matched_edges=bridge["matched"],
        MAE_timeaware_s=mae_t,MAE_freeflow_s=mae_f,
        paired_benefit_s=round(benefit,5),
        signed_timeaware_bias_s=bias,
        od_pair_sha256=source["od_pair_sha256"],
        network_sha256=source["network_sha256"],
        trips_sha256=source["trips_sha256"],
        routes_sha256=source["routes_sha256"],
        frozen_scientific_commit=FROZEN_SHA,
        R3_teleport_count=eligible["teleports_reported"],
        native_partial_edge_bins=eligible["partial_native_bins"])

def summarize_seed_level(records,expected_seed_ids,original_frozen_ci):
    """Run frozen n=10 R4 CI on independently paired seeds; no file access.

    Dummy integer seed labels are used during review tests. Only a separate
    approved experiment could ever supply observations for reserved IDs.
    """
    expected=tuple(expected_seed_ids)
    require(len(expected)==N_SEEDS and len(set(expected))==N_SEEDS,
            "Exactly ten unique prespecified seed labels required")
    allowed={(s,w) for s in expected for w in REGIMES}
    seen={}
    for r in records:
        seed=r.get("seed");window=r.get("window_seconds")
        key=(seed,window)
        require(key in allowed and key not in seen,
                "Unregistered or duplicated seed/regime")
        require(r.get("status")=="ELIGIBLE_BY_FROZEN_R3_RULES",
                "Ineligible seed/regime cannot contribute to planned analysis")
        require(r.get("frozen_scientific_commit")==FROZEN_SHA
                and r.get("vehicles")==N_VEHICLES
                and r.get("matched_edges",0)>=N_VEHICLES,
                "Wrong source or incomplete matched seed")
        for field in ("MAE_timeaware_s","MAE_freeflow_s","paired_benefit_s",
                      "signed_timeaware_bias_s"):
            require(isinstance(r.get(field),(int,float))
                    and math.isfinite(r[field]),"Missing or invalid seed metric")
        require(min(r["MAE_timeaware_s"],r["MAE_freeflow_s"])>=0,
                "Negative MAE")
        require(abs(r["MAE_freeflow_s"]-r["MAE_timeaware_s"]
                    -r["paired_benefit_s"])<0.0001,
                "Seed difference is not the paired MAE difference")
        require(sha256_ok(r.get("od_pair_sha256")),
                "No comparable demand OD fingerprint")
        seen[key]=r
    require(set(seen)==allowed,
            "Missing prespecified paired seed: no substitution or imputation")
    for seed in expected:
        require(len({seen[(seed,w)]["od_pair_sha256"] for w in REGIMES})==1,
                "Demand OD pairs differ across regimes for same seed")
    regimes=[]
    for w in REGIMES:
        values=[seen[(s,w)]["paired_benefit_s"] for s in expected]
        ci=original_frozen_ci(values)
        require(ci["seed_count"]==N_SEEDS,
                "Frozen seed-level Student-t method returned unexpected count")
        regimes.append(dict(window_seconds=w,
            role="primary" if w==200 else "secondary",
            seed_count=N_SEEDS,paired_benefit_mean_s=ci["mean"],
            seed_level_sd_s=ci["sd"],
            paired_benefit_median_s=statistics.median(values),
            paired_benefit_range_s=[min(values),max(values)],
            confidence_interval_95_s=[ci["lower"],ci["upper"]],
            timeaware_MAE_seed_mean_s=statistics.mean(
                seen[(s,w)]["MAE_timeaware_s"] for s in expected),
            freeflow_MAE_seed_mean_s=statistics.mean(
                seen[(s,w)]["MAE_freeflow_s"] for s in expected),
            signed_bias_seed_mean_s=statistics.mean(
                seen[(s,w)]["signed_timeaware_bias_s"] for s in expected)))
    return dict(status="PURE_SYNTHETIC_REVIEW_NOT_HELDOUT_EVALUATION",
        expected_seed_count=N_SEEDS,
        scenario_count=len(seen),primary_regime_seconds=200,
        regimes=regimes,
        restrictions=["Independent replicates are demand seeds, not vehicle edges",
                      "Better timing accuracy is not systemwide routing benefit",
                      "No evaluation workflow or seed generation in this module"])
