"""Offline T1 feasibility unit tests: no SUMO, no validation cohorts."""
import unittest
from feasibility import Schedule, prove_potential, BIN_S, SHIFTS


class T1FeasibilityTests(unittest.TestCase):
    def sample(self, phase=0.0):
        rides = [
            {"id": f"veh{i:04d}", "preferred": i * .2,
             "route": ("north", "junction", "south") if i % 2 else ("west", "junction", "east")}
            for i in range(20)
        ]
        info = {key: (8.0, 2.0) for key in ("north", "south", "west", "east", "junction")}
        return Schedule(rides, info, seed=2101, phase=phase)

    def test_exact_rosenthal_potential_identity(self):
        self.assertTrue(prove_potential())

    def test_10s_shifts_change_profiles_across_bin_phase(self):
        for phase in (0.0, 2.5, 5.0, 7.5):
            m = self.sample(phase)
            for vid in m.eligible:
                profiles = [frozenset(m.profile(vid, sh).items()) for sh in SHIFTS]
                self.assertEqual(len(set(profiles)), 4)
                for sh in SHIFTS:
                    self.assertEqual(len(m.profile(vid, sh)), 3)

    def test_global_delta_matches_direct_total(self):
        m = self.sample()
        vid = m.order[0]
        old = m.predicted_total()
        d = m.global_delta(vid, 10)
        m.apply(vid, 10)
        self.assertAlmostEqual(m.predicted_total() - old, d, places=7)
        self.assertTrue(m.audit()["counts_match"])

    def test_b_and_c_stability_and_nonparticipants(self):
        for policy in ("B", "C"):
            m = self.sample()
            result = m.optimize(policy)
            self.assertTrue(result["stable"], result)
            self.assertLessEqual(result["max_residual_gain_s"], .5 if policy == "B" else .05 + 1e-8)
            self.assertTrue(m.audit()["counts_match"])
            self.assertTrue(all(m.offsets[v] == 0 for v in m.ids if v not in m.eligible))

    def test_shift_cost_is_explicit_and_can_outweigh_congestion(self):
        m = Schedule([{"id": f"v{i}", "preferred": float(i),
                       "route": ("lonely",)} for i in range(6)],
                     {"lonely": (8.0, 1000000.0)}, seed=2101)
        for v in m.eligible:
            self.assertGreater(m.personal(v, 10), m.personal(v, 0) + 9.9)
        # If congestion prediction is essentially unchanged, a departure
        # penalty must not masquerade as a meaningful traffic forecast signal.
        self.assertEqual(m.initial_sensitivity()["traffic_cost_spread_gt_0p5_s"], 0)

    def test_forecast_traffic_signal_excludes_predeparture_penalty(self):
        m = self.sample()
        diagnostic = m.initial_sensitivity()
        self.assertEqual(diagnostic["eligible"], 10)
        self.assertEqual(diagnostic["different_edge_bin_footprints"], 10)
        self.assertGreater(diagnostic["mean_traffic_cost_spread_s"], 0)


if __name__ == "__main__":
    unittest.main()
