"""18 frozen Stage 1B no-SUMO scientific/integrity gates.

Fixtures are deliberately tiny synthetic graphs; passing proves implementation
invariants, not empirical SUMO prediction skill.
"""
import copy
import math
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from research.externality_estimator import (
    Feature, InvalidScenario, Link, Parameters, Scenario, Turn, UncertainScenario,
    Vehicle, predict_counterfactual, predict_bundle,
)
from research.externality_estimator.audit import (
    check_partition, enforce_no_oracle_imports, save_prediction_once, sha256,
)
from research.externality_estimator.link_turn_queue import evolve, NonCompletion
from research.externality_estimator.externality_outputs import effects
from research.externality_estimator.uncertainty import reliability


def network(*, storage=8):
    edges = tuple(Link(e, 15, 15, 1, storage) for e in ('A', 'B', 'C', 'Z', 'X', 'Y'))
    turns = (Turn('A','B','JA'), Turn('A','C','JA'),
             Turn('B','Z','JB'), Turn('C','Z','JC'), Turn('X','Y','JB'))
    return edges, turns


def identity_case(other_depart=3, target_route=('A','B','Z')):
    edges,turns=network()
    return Scenario(edges,turns, (
        Vehicle('ego',0,target_route,True),
        Vehicle('other',other_depart,('X','Y'),False)))


def coupled_case():
    edges=tuple(Link(e,15,15,1,8) for e in ('A','P','B','C','Z','X','Y'))
    turns=(Turn('A','B','JA'),Turn('A','C','JA'),
           Turn('P','B','JP'),Turn('P','C','JP'),
           Turn('B','Z','JB'),Turn('C','Z','JC'),Turn('X','Y','JB'))
    return Scenario(edges,turns,(Vehicle('ego1',0,('A','C','Z'),True),
                                 Vehicle('ego2',0,('P','C','Z'),True),
                                 Vehicle('other',3,('X','Y'))))


class FrozenStage1BGates(unittest.TestCase):
    def test_T01_global_mass_conservation(self):
        s=identity_case()
        r=evolve(s)
        self.assertEqual(set(r.arrivals),{'ego','other'})
        self.assertEqual(len([v for v in r.events if v.action=='insert']),2)
        self.assertEqual(len([v for v in r.events if v.action=='arrive']),2)
        self.assertTrue(all(v in r.insertion for v in r.arrivals))

    def test_T02_finite_storage_and_nonnegative_queues(self):
        edges,turns=network(storage=1)
        s=Scenario(edges,turns,tuple(Vehicle('o'+str(i),0,('X','Y')) for i in range(8)))
        r=evolve(s)
        self.assertEqual(len(r.arrivals),8)
        insertions=[v.tick for v in r.events if v.action=='insert' and v.edge=='X']
        self.assertEqual(insertions,sorted(insertions))
        self.assertTrue(all(b>a for a,b in zip(insertions,insertions[1:])))

    def test_T03_shared_junction_conflict_and_receiving(self):
        s=identity_case()
        r=evolve(s)
        # Two competing movements to independent receiving links are never
        # accepted in same second at shared JB conflict class.
        crosses=[v for v in r.events if v.action=='cross' and v.edge in ('B','X')]
        self.assertEqual(len({v.tick for v in crosses}),len(crosses))
        self.assertEqual(r.arrivals['ego'],8)
        self.assertEqual(r.elapsed_s['other'],6)

    def test_T04_fifo_and_freeflow_minimum(self):
        edges,turns=network(storage=2)
        s=Scenario(edges,turns,tuple(Vehicle(f'o{i}',0,('X','Y')) for i in range(5)))
        r=evolve(s)
        insert={x.vehicle_id:x.tick for x in r.events if x.action=='insert'}
        arrival={x.vehicle_id:x.tick for x in r.events if x.action=='arrive'}
        order=[x.vehicle_id for x in r.events if x.action=='insert']
        # Event insertion order must not be inverted at destination.
        arrival_order=[x.vehicle_id for x in r.events if x.action=='arrive']
        self.assertEqual(order,arrival_order)
        self.assertTrue(all(arrival[k]>=insert[k]+2 for k in arrival))

    def test_T05_same_route_zero_effect(self):
        s=identity_case()
        p=predict_counterfactual(s,'ego',('A','B','Z'))
        self.assertEqual((p.pred_self_delta_s,p.pred_external_delta_network_s,
                          p.pred_nonparticipant_delta_network_s,p.pred_all_delta_network_s),(0,0,0,0))

    def test_T06_disjoint_paths_no_external_harm(self):
        edges,turns=network()
        s=Scenario(edges,turns,(Vehicle('ego',0,('A','B','Z'),True),Vehicle('other',10,('X','Y'))))
        p=predict_counterfactual(s,'ego',('A','C','Z'))
        self.assertEqual(p.pred_external_delta_network_s,0)

    def test_T07_old_external_self_identity_is_broken(self):
        s=identity_case(other_depart=3)
        p=predict_counterfactual(s,'ego',('A','C','Z'))
        self.assertEqual(p.pred_self_delta_s,0)
        self.assertEqual(p.pred_external_delta_network_s,-1)
        self.assertNotEqual(p.pred_external_delta_network_s,p.pred_self_delta_s)
        self.assertNotEqual(p.pred_all_delta_network_s,2*p.pred_self_delta_s)
        self.assertEqual(p.pred_nonparticipant_delta_network_s,-1)

    def test_T08_beneficial_and_harmful_externalities(self):
        s=identity_case(other_depart=3)
        gain=predict_counterfactual(s,'ego',('A','C','Z'))
        adverse=predict_counterfactual(identity_case(3,('A','C','Z')),'ego',('A','B','Z'))
        self.assertLess(gain.pred_external_delta_network_s,0)
        self.assertGreater(adverse.pred_external_delta_network_s,0)

    def test_T09_upstream_spillback_under_storage(self):
        # One-slot target route A->B->Z, other delayed in A by downstream
        # receiving block; route of second driver never changes.
        edges=(Link('A',15,15,1,2),Link('B',15,15,1,1),
               Link('C',15,15,1,1),Link('Z',15,15,1,2))
        turns=(Turn('A','B','JA'),Turn('A','C','JA'),
               Turn('B','Z','JB'),Turn('C','Z','JC'))
        s=Scenario(edges,turns,(Vehicle('ego',0,('A','B','Z'),True),
                                Vehicle('other',0,('A','B','Z'))))
        p=predict_counterfactual(s,'ego',('A','C','Z'))
        self.assertNotEqual(p.per_driver_baseline_s['other'],p.per_driver_swap_s['other'])
        self.assertTrue(math.isfinite(p.pred_external_delta_network_s))

    def test_T10_joint_bundle_is_not_sum(self):
        s=coupled_case()
        p1=predict_counterfactual(s,'ego1',('A','B','Z'))
        p2=predict_counterfactual(s,'ego2',('P','B','Z'))
        together=predict_bundle(s,{'ego1':('A','B','Z'),'ego2':('P','B','Z')})
        self.assertEqual(together.pred_all_delta_network_s,1)
        self.assertNotEqual(together.pred_all_delta_network_s,
                            p1.pred_all_delta_network_s+p2.pred_all_delta_network_s)

    def test_T11_schedule_to_insertion_delay_exactly_once(self):
        edges=(Link('X',15,15,1,1),)
        s=Scenario(edges,(),(Vehicle('first',0,('X',)),Vehicle('second',0,('X',))))
        r=evolve(s)
        self.assertGreater(r.insertion['second'],r.insertion['first'])
        for v in s.vehicles:
            self.assertEqual(r.elapsed_s[v.vehicle_id],r.arrivals[v.vehicle_id]-v.scheduled_departure_s)

    def test_T12_illegal_routes_rejected_and_conflict_shared(self):
        s=identity_case()
        with self.assertRaises(InvalidScenario):
            predict_counterfactual(s,'ego',('A','X','Z'))
        self.test_T03_shared_junction_conflict_and_receiving()

    def test_T13_byte_identical_deterministic_outputs(self):
        s=identity_case()
        a=predict_counterfactual(s,'ego',('A','C','Z'),uncertainty_seed=103)
        b=predict_counterfactual(s,'ego',('A','C','Z'),uncertainty_seed=103)
        self.assertEqual(a.prediction_hash,b.prediction_hash)
        self.assertEqual(a.per_driver_baseline_s,b.per_driver_baseline_s)
        self.assertEqual(a.per_driver_swap_s,b.per_driver_swap_s)
        self.assertEqual(a.scenario_sha,b.scenario_sha)

    def test_T14_future_observation_blocked_at_t0(self):
        edges,turns=network()
        for name,t,source in [('measured_current_speed',1,'road_sensor'),
                              ('future_fcd',0,'sensor'),('current',0,'post_treatment_queues')]:
            with self.assertRaises(InvalidScenario):
                Scenario(edges,turns,(Vehicle('e',0,('A','B','Z')),),
                         features=(Feature(name,t,source),))
        enforce_no_oracle_imports(Path(__file__).resolve().parents[1])

    def test_T15_missing_state_abstention(self):
        edges,turns=network()
        with self.assertRaises(UncertainScenario):
            Scenario(edges,turns,(Vehicle('e',0,('A','B','Z')),),t0_s=3)
        self.assertEqual(reliability(complete=False,known_turn_conflicts=False).status,'ABSTAIN')
        self.assertFalse(reliability(complete=True,known_turn_conflicts=True).calibrated)

    def test_T16_others_and_nonparticipants_accounting(self):
        s=identity_case()
        p=predict_counterfactual(s,'ego',('A','C','Z'))
        expected=effects(p.per_driver_baseline_s,p.per_driver_swap_s,{'ego'},{'other'})
        self.assertEqual(expected['external_delta_network_s'],p.pred_external_delta_network_s)
        self.assertEqual(expected['nonparticipant_delta_network_s'],p.pred_nonparticipant_delta_network_s)
        self.assertEqual(expected['self_delta_s']+expected['external_delta_network_s'],p.pred_all_delta_network_s)

    def test_T17_all_1000_or_abstain_no_completed_only(self):
        edge=Link('X',7.5,15,1,1)
        s=Scenario((edge,),(),tuple(Vehicle(f'veh{i:04d}',0,('X',),eligible=(i==0)) for i in range(1000)))
        p=predict_counterfactual(s,'veh0000',('X',),params=Parameters(q_sat=.35,max_wall_s=None))
        self.assertEqual(p.status,'ABSTAIN_NONCOMPLETION')
        self.assertEqual(p.per_driver_baseline_s,{})
        self.assertIsNone(p.pred_all_delta_network_s)

    def test_T18_partitions_and_prediction_first_write(self):
        check_partition(5101,'DEV_BUILD',for_calibration=True)
        check_partition(5111,'DEV_CHECK')
        for seed,part in [(5111,'DEV_CHECK'),(4201,'DEV_BUILD'),(4101,'DEV_BUILD'),(5101,'DEV_CHECK')]:
            with self.assertRaises(InvalidScenario):
                check_partition(seed,part,for_calibration=True)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'predictions.json'
            first=save_prediction_once(path,{'seed':5101,'pred_external':-3})
            self.assertTrue(len(first)==64)
            with self.assertRaises(FileExistsError):
                save_prediction_once(path,{'seed':5101,'pred_external':+7})
            with self.assertRaises(InvalidScenario):
                save_prediction_once(Path(d)/'bad.json',{'label':'realized future'})


if __name__=='__main__':
    unittest.main()
