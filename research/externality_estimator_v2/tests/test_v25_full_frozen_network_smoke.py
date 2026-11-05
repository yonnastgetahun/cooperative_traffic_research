"""No-SUMO full-network readiness smoke, using ONLY inspected historical static inputs.

The original seed-5101 historical data are *engineering fixtures*, never held-out
development accuracy or independent validation. Original SUMO outcomes not opened.
"""
import json
import os
from pathlib import Path
import unittest

from research.externality_estimator.schema import Parameters
from research.externality_estimator.scenario_io import from_sumo_static_xml
from research.externality_estimator_v2.movement import compile_frozen_grid_network
from research.externality_estimator_v2.counterfactual import predict_counterfactual


class FullNetworkReadiness(unittest.TestCase):
    def test_V25_frozen_1000_driver_real_grid_no_sumo_pair(self):
        network=os.environ.get("E1_ORIGINAL_NETWORK")
        if network is None:
            self.skipTest("Historical static network path available only in CI")
        base=Path(network).parent
        s=from_sumo_static_xml(network,base/"trips.xml",base/"routes"/"I.rou.xml",
                               partition="HISTORICAL_DIAG_ONLY")
        mmap=compile_frozen_grid_network(network)
        manifest=json.loads((base/"scenario-manifest.json").read_text())
        first=manifest["probes"][0]
        self.assertEqual(len(s.vehicles),1000)
        outcome=predict_counterfactual(
            s,first["target_vehicle_id"],tuple(first["alternate_route"]),mmap,
            params=Parameters(q_sat=0.50,max_wall_s=120.0))
        print("V2-I2 real-grid static 1000-driver pair:",
              outcome.status,outcome.detail,outcome.elapsed_wall_s)
        self.assertEqual(outcome.status,"OK",
                         "Abstaining/full-network noncompletion prevents Stage V2-I2 readiness")
        self.assertEqual(len(outcome.per_driver_baseline_s),1000)
        self.assertEqual(len(outcome.per_driver_swap_s),1000)
        self.assertLessEqual(outcome.elapsed_wall_s,120.0)
