#!/usr/bin/env python3
"""M3 production adapter review tests use fabricated records, never heldouts."""
import hashlib
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"frozen/experiments/experiment_002"))
from g3_r4_seed_analysis_v01 import mean_ci_if_ten
from adapters_v01 import (
    Ineligible,FROZEN_SHA,SUMO_IMAGE,
    assess_frozen_r3,seed_record,summarize_seed_level,od_pair_fingerprint)
from activation_gate_v01 import (
    ActivationBlocked,assert_not_executing_reserved_seed,
    require_heldout_execution_authorization,inspect_inactive_template,
    inspect_active_workflow_inventory)

def mock_r3():
    return dict(seed=2101,window_seconds=200,matched_trip_count=1000,
        route_population_invariant=True,tripinfo_invariant=True,
        reported_teleports=dict(teleport_state="ZERO_CONFIRMED",teleports_total=0),
        reported_FCD=dict(distinct_observed_vehicles=1000,timestep_count=100,
            structural_anomalies={},within_trip_disappearance_count=0),
        native_edge_bins=dict(native_bins=1000,status_counts=dict(
            FULL_30_SECOND_BIN=640,PARTIAL_NATIVE_BIN=360,
            EMPTY_NATIVE_EDGE_NO_SAMPLES=150,
            MISSING_NATIVE_SAMPLED_SECONDS=0,
            MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES=0)),
        exception_gate="PASS_FOR_THIS_REPLAY",scientific_exception_counts={},
        status="R3_DEVELOPMENT_OBSERVATION_POLICY_APPLIED")

def fake_seed_record(seed,window,benefit=2):
    return dict(seed=seed,window_seconds=window,
        status="ELIGIBLE_BY_FROZEN_R3_RULES",
        frozen_scientific_commit=FROZEN_SHA,vehicles=1000,matched_edges=8393,
        MAE_timeaware_s=10.0,MAE_freeflow_s=10.0+benefit,
        paired_benefit_s=benefit,signed_timeaware_bias_s=5.0,
        od_pair_sha256=hashlib.sha256(str(seed).encode()).hexdigest())

class ReviewTests(unittest.TestCase):
    def test_teleport_unknown_or_positive_is_never_silently_eligible(self):
        r=mock_r3()
        self.assertEqual(assess_frozen_r3(r,2101,200)["status"],
                         "ELIGIBLE_BY_FROZEN_R3_RULES")
        for state,total in [("UNKNOWN_NOT_CAPTURED",None),
                            ("NONZERO_CONFIRMED",1)]:
            q=mock_r3();q["reported_teleports"]["teleport_state"]=state
            q["reported_teleports"]["teleports_total"]=total
            with self.assertRaises(Ineligible):assess_frozen_r3(q,2101,200)
    def test_FCD_missing_and_native_positive_missing_fail(self):
        a=mock_r3();a["reported_FCD"]["within_trip_disappearance_count"]=2
        with self.assertRaises(Ineligible):assess_frozen_r3(a,2101,200)
        a=mock_r3();a["native_edge_bins"]["status_counts"]["MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES"]=1
        with self.assertRaises(Ineligible):assess_frozen_r3(a,2101,200)
    def test_compact_seed_scoring_preserves_frozen_pair(self):
        m=dict(vehicles=1000,edge_traversals=8393,
            frozen_scientific_commit=FROZEN_SHA,
            paired_MAE_benefit_ff_minus_timeaware_s=5.33344,
            timing_metrics=dict(timeaware=dict(n=8393,mae_s=51.31636,bias_s=51.22124),
                                freeflow=dict(n=8393,mae_s=56.6498)),
            matches_preexisting_M2_forecast_errors=True)
        b=dict(planned_edges=8393,matched=8393,missing_vehicle_ids=[])
        s=dict(scientific_commit=FROZEN_SHA,sumo_image=SUMO_IMAGE,
            network_sha256="a"*64,trips_sha256="b"*64,
            routes_sha256="c"*64,od_pair_sha256="d"*64,
            route_audit_byte_identical=True)
        a=seed_record(2101,200,m,mock_r3(),b,s)
        self.assertEqual(a["paired_benefit_s"],5.33344)
        self.assertEqual(a["native_partial_edge_bins"],360)
        s["scientific_commit"]="moved"
        with self.assertRaises(Ineligible):seed_record(2101,200,m,mock_r3(),b,s)
    def test_dummy_ten_seed_paired_CI_reuses_frozen_calculation(self):
        labels=list(range(101,111))
        rows=[fake_seed_record(seed,w,benefit=seed-100)
              for seed in labels for w in (200,600,1200)]
        result=summarize_seed_level(rows,labels,mean_ci_if_ten)
        self.assertEqual(result["scenario_count"],30)
        self.assertAlmostEqual(result["regimes"][0]["paired_benefit_mean_s"],5.5)
        self.assertGreater(result["regimes"][0]["confidence_interval_95_s"][1],
                           result["regimes"][0]["paired_benefit_mean_s"])
    def test_missing_duplicate_ineligible_or_changed_OD_blocks_full_CI(self):
        labels=list(range(101,111))
        rows=[fake_seed_record(seed,w) for seed in labels for w in (200,600,1200)]
        for bad in (rows[:-1],rows+[rows[0]]):
            with self.assertRaises(Ineligible):summarize_seed_level(bad,labels,mean_ci_if_ten)
        damaged=[dict(x) for x in rows]
        damaged[1]["od_pair_sha256"]="e"*64
        with self.assertRaises(Ineligible):summarize_seed_level(damaged,labels,mean_ci_if_ten)
        damaged=[dict(x) for x in rows]
        damaged[1]["status"]="INELIGIBLE"
        with self.assertRaises(Ineligible):summarize_seed_level(damaged,labels,mean_ci_if_ten)
    def test_ordered_OD_fingerprint_ignores_departure_only(self):
        records=[(f"veh{i:04d}","A","B") for i in range(1000)]
        a=od_pair_fingerprint(records)
        self.assertEqual(a,od_pair_fingerprint(records))
        records[5]=(records[5][0],"A","C")
        self.assertNotEqual(a,od_pair_fingerprint(records))
        with self.assertRaises(Ineligible):od_pair_fingerprint(records[:-1])
    def test_actual_heldout_execution_permanently_denied_in_review_code(self):
        for seed in range(3101,3111):
            with self.assertRaises(ActivationBlocked):assert_not_executing_reserved_seed(seed)
            with self.assertRaises(ActivationBlocked):require_heldout_execution_authorization(seed)
        with self.assertRaises(ActivationBlocked):require_heldout_execution_authorization(
             "workflow_dispatch",protected_environment_approved=True)
    def test_disabled_template_and_no_armed_workflow(self):
        t=inspect_inactive_template(ROOT)
        self.assertEqual(t["template_job_count"],3)
        self.assertEqual(t["disabled_job_count"],3)
        self.assertFalse(t["protected_environment_reviewers_verified"])
        self.assertFalse(inspect_active_workflow_inventory(ROOT)["active_heldout_evaluation_workflow_found"])

if __name__=="__main__":unittest.main()
