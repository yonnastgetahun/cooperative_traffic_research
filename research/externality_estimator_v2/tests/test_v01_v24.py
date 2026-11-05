"""V2-I1 frozen E1-v2-J1 no-SUMO physical, integrity and contamination checks.

These are independent deterministic engineering fixtures; no test establishes
prediction accuracy against SUMO, real-world feasibility or Test B efficacy.
"""
import os
from pathlib import Path
import time
import unittest

from research.externality_estimator.schema import (
    Feature, InvalidScenario, Link, Parameters, Scenario, Turn, Vehicle)
from research.externality_estimator.link_turn_queue import evolve as old_e1_evolve
from research.externality_estimator.audit import enforce_no_oracle_imports
from research.externality_estimator_v2.movement import (
    Movement, MovementMap, InvalidMovementMap, PriorityAmbiguity, bits,
    compile_frozen_grid_network, KNOWN_CANONICAL_GRID_SHA)
from research.externality_estimator_v2.scheduler import Candidate, select
from research.externality_estimator_v2.network_evolution import evolve_v2
from research.externality_estimator_v2.counterfactual import (
    predict_counterfactual, predict_bundle)


def m(junction,index,src,dst,*,foes=(),yield_to=(),cont=False,via=None):
    return Movement(junction,index,src,dst,via or f":{junction}_{index}_0",
                    frozenset(foes),frozenset(yield_to),cont)


def road_set(*names, storage=8):
    return tuple(Link(name,15.0,15.0,1,storage) for name in names)


def independent_case(foes=False, cont=False, q=.5):
    links=road_set("P","Q","R","S")
    turns=(Turn("P","Q","J"),Turn("R","S","J"))
    persons=(Vehicle("v1",0,("P","Q"),True),
             Vehicle("v2",0,("R","S"),False))
    scenario=Scenario(links,turns,persons)
    movements=MovementMap((
        m("J",0,"P","Q",foes=(1,) if foes else (),cont=cont),
        m("J",1,"R","S",foes=(0,) if foes else (),yield_to=(0,) if foes else ())))
    return scenario,movements,Parameters(q_sat=q)


def path_choice_case(*,other_depart=3,ego_route=("A","B","Z")):
    edges=road_set("A","B","C","Z","X","Y")
    turns=(Turn("A","B","JA"),Turn("A","C","JA"),
           Turn("B","Z","JB"),Turn("C","Z","JC"),
           Turn("X","Y","JB"))
    mm=MovementMap((
        m("JA",0,"A","B",foes=(1,)),
        m("JA",1,"A","C",foes=(0,)),
        m("JB",0,"B","Z",foes=(1,)),
        m("JB",1,"X","Y",foes=(0,),yield_to=(0,)),
        m("JC",0,"C","Z")))
    scenario=Scenario(edges,turns,(
        Vehicle("ego",0,ego_route,True),
        Vehicle("other",other_depart,("X","Y"),False)))
    return scenario,mm


class FrozenV2I1Tests(unittest.TestCase):
    def test_V01_source_network_provenance(self):
        scenario,mmap,_=independent_case()
        self.assertEqual(len(mmap.records),2)
        self.assertRaises(InvalidMovementMap, MovementMap,
                          mmap.records, "UNKNOWN", "wrong-SUMO-source")
        original=os.environ.get("E1_ORIGINAL_NETWORK")
        if original:
            built=compile_frozen_grid_network(original)
            self.assertEqual(built.canonical_sha,KNOWN_CANONICAL_GRID_SHA)
            self.assertEqual(len(built.records),1320)
            self.assertEqual(len(built.by_edge_pair()),1320)

    def test_V02_bit_order_index_and_response(self):
        self.assertEqual(bits("011"),frozenset((0,1)))
        self.assertEqual(bits("001"),frozenset((0,)))
        self.assertRaises(InvalidMovementMap,bits,"00x")
        self.assertRaises(InvalidMovementMap,m,"J",0,"P","Q",foes=(),yield_to=(1,))

    def test_V03_A0_nonfoes_move_same_tick_vs_old(self):
        s,mm,params=independent_case()
        new=evolve_v2(s,mm,params)
        before=old_e1_evolve(s,params)
        self.assertEqual(len({e.tick for e in new.events if e.action=="cross"}),1)
        self.assertEqual(len({e.tick for e in before.events if e.action=="cross"}),2)
        self.assertEqual(len(new.arrivals),2)

    def test_V04_foes_never_same_tick(self):
        s,mm,p=independent_case(foes=True)
        cross=[e.tick for e in evolve_v2(s,mm,p).events if e.action=="cross"]
        self.assertEqual(len(set(cross)),2)

    def test_V05_directional_priority_and_absent_claimant(self):
        a=m("J",0,"P","Q",foes=(1,))
        b=m("J",1,"R","S",foes=(0,),yield_to=(0,))
        ready=(Candidate("low",b),Candidate("high",a))
        result=select(ready,("R","P"),0,{"Q":1,"S":1})
        self.assertEqual(result.accepted[0].vehicle_id,"high")
        self.assertEqual(result.blocked[0][0],"low")
        lone=select((Candidate("low",b),),("R","P"),0,{"Q":1,"S":1})
        self.assertEqual(lone.accepted[0].vehicle_id,"low")

    def test_V06_priority_cycle_abstains(self):
        a=m("J",0,"P","Q",foes=(1,),yield_to=(1,))
        b=m("J",1,"R","S",foes=(0,),yield_to=(0,))
        with self.assertRaises(PriorityAmbiguity):
            select((Candidate("a",a),Candidate("b",b)),("P","R"),0,{"Q":1,"S":1})

    def test_V07_one_fifo_head_per_lane(self):
        a=m("J",0,"P","Q")
        b=m("J",1,"P","S")
        with self.assertRaises(PriorityAmbiguity):
            select((Candidate("a",a),Candidate("b",b)),("P",),0,{"Q":1,"S":1})

    def test_V08_shared_receiving_lane_exclusive(self):
        a=m("J",0,"P","Q")
        b=m("J",1,"R","Q")
        res=select((Candidate("a",a),Candidate("b",b)),("P","R"),0,{"Q":2})
        self.assertEqual(len(res.accepted),1)
        self.assertEqual(res.blocked[0][1],"SHARED_SOURCE_OR_OUTGOING_LANE")
        res2=select((Candidate("a",a),Candidate("b",b)),("P","R"),0,{"Q":1})
        self.assertEqual(len(res2.accepted),1)

    def test_V09_shared_initial_internal_via_exclusive(self):
        a=m("J",0,"P","Q",via=":shared_0")
        b=m("J",1,"R","S",via=":shared_0")
        result=select((Candidate("a",a),Candidate("b",b)),("P","R"),0,{"Q":1,"S":1})
        self.assertEqual(len(result.accepted),1)
        self.assertEqual(result.blocked[0][1],"SHARED_INTERNAL_VIA")

    def test_V10_cont_candidate_exclusive(self):
        a=m("J",0,"P","Q",cont=True)
        b=m("J",1,"R","S")
        result=select((Candidate("a",a),Candidate("b",b)),("P","R"),0,{"Q":1,"S":1})
        self.assertEqual(len(result.accepted),1)
        self.assertEqual(result.blocked[0][1],"TIER_C_EXCLUSIVE_SERVICE")

    def test_V11_fractional_service_and_capacity_tokens(self):
        for q in (0.35,0.5,0.65):
            s,mmap,p=independent_case(q=q)
            result=evolve_v2(s,mmap,p)
            self.assertEqual(len(result.arrivals),2)
            self.assertTrue(all(e.tick>=4 for e in result.events if e.action=="cross"))

    def test_V12_source_delay_counted_once(self):
        s=Scenario((Link("X",7.5,15,1,1),),(),(
            Vehicle("first",0,("X",),True),
            Vehicle("second",0,("X",),False)))
        r=evolve_v2(s,MovementMap(()))
        self.assertGreater(r.insertion["second"],r.insertion["first"])
        self.assertEqual(r.elapsed_s["second"],r.arrivals["second"])

    def test_V13_global_conservation_and_legal_transitions(self):
        s,mm,p=independent_case()
        r=evolve_v2(s,mm,p)
        self.assertEqual(set(r.arrivals),{"v1","v2"})
        self.assertEqual(len([e for e in r.events if e.action=="insert"]),2)
        self.assertEqual(len([e for e in r.events if e.action=="arrive"]),2)

    def test_V14_rr_pointer_and_blocked_guard_reproducibility(self):
        a=m("J",0,"P","Q",foes=(1,))
        b=m("J",1,"R","S",foes=(0,))
        ready=(Candidate("a",a),Candidate("b",b))
        first=select(ready,("P","R"),0,{"Q":1,"S":1})
        second=select(ready,("P","R"),first.pointer_after,{"Q":1,"S":1})
        self.assertEqual(len(first.accepted),len(second.accepted))
        self.assertNotEqual(first.accepted[0].vehicle_id,second.accepted[0].vehicle_id)
        self.assertEqual(first,select(ready,("P","R"),0,{"Q":1,"S":1}))

    def test_V15_identical_and_disjoint_counterfactual(self):
        s,mm=path_choice_case(other_depart=10)
        same=predict_counterfactual(s,"ego",("A","B","Z"),mm)
        self.assertEqual(same.status,"OK")
        self.assertEqual(same.pred_all_delta_network_s,0)
        alt=predict_counterfactual(s,"ego",("A","C","Z"),mm)
        self.assertEqual(alt.status,"OK")
        self.assertEqual(alt.pred_external_delta_network_s,0)

    def test_V16_equal_self_can_coexist_with_nonzero_externality(self):
        s,mm=path_choice_case(other_depart=3)
        p=predict_counterfactual(s,"ego",("A","C","Z"),mm)
        self.assertEqual(p.status,"OK")
        self.assertEqual(p.pred_self_delta_s,0)
        self.assertNotEqual(p.pred_external_delta_network_s,0)
        self.assertEqual(p.pred_external_delta_network_s,p.pred_nonparticipant_delta_network_s)

    def test_V17_signed_positive_negative_other_effect(self):
        s,mm=path_choice_case(other_depart=3)
        p=predict_counterfactual(s,"ego",("A","C","Z"),mm)
        alt,mm2=path_choice_case(other_depart=3,ego_route=("A","C","Z"))
        q=predict_counterfactual(alt,"ego",("A","B","Z"),mm2)
        self.assertLess(p.pred_external_delta_network_s,0)
        self.assertGreater(q.pred_external_delta_network_s,0)

    def test_V18_recompute_bundle_not_add_predictions(self):
        edges=road_set("A","P","B","C","Z","X","Y")
        turns=(Turn("A","B","JA"),Turn("A","C","JA"),
            Turn("P","B","JP"),Turn("P","C","JP"),
            Turn("B","Z","JB"),Turn("C","Z","JC"),Turn("X","Y","JB"))
        mm=MovementMap((m("JA",0,"A","B",foes=(1,)),m("JA",1,"A","C",foes=(0,)),
                        m("JP",0,"P","B",foes=(1,)),m("JP",1,"P","C",foes=(0,)),
                        m("JB",0,"B","Z",foes=(1,)),m("JB",1,"X","Y",foes=(0,),yield_to=(0,)),
                        m("JC",0,"C","Z")))
        s=Scenario(edges,turns,(Vehicle("ego1",0,("A","C","Z"),True),
            Vehicle("ego2",0,("P","C","Z"),True),Vehicle("other",3,("X","Y"))))
        p1=predict_counterfactual(s,"ego1",("A","B","Z"),mm)
        p2=predict_counterfactual(s,"ego2",("P","B","Z"),mm)
        joint=predict_bundle(s,{"ego1":("A","B","Z"),"ego2":("P","B","Z")},mm)
        self.assertEqual(joint.status,"OK")
        self.assertNotEqual(joint.pred_all_delta_network_s,
            p1.pred_all_delta_network_s+p2.pred_all_delta_network_s)

    def test_V19_future_feature_rejected_and_no_oracle_import(self):
        edges,turns=road_set("X","Y"),(Turn("X","Y","J"),)
        with self.assertRaises(InvalidScenario):
            Scenario(edges,turns,(Vehicle("e",0,("X","Y")),),
                     features=(Feature("future_fcd",1,"simulator"),))
        enforce_no_oracle_imports(Path(__file__).resolve().parents[1])

    def test_V20_deterministic_paired_hash(self):
        s,mm=path_choice_case(other_depart=3)
        a=predict_counterfactual(s,"ego",("A","C","Z"),mm,uncertainty_seed=7)
        b=predict_counterfactual(s,"ego",("A","C","Z"),mm,uncertainty_seed=7)
        self.assertEqual(a.prediction_hash,b.prediction_hash)
        self.assertEqual(a.per_driver_swap_s,b.per_driver_swap_s)

    def test_V21_full_arrival_or_abstain(self):
        s=Scenario((Link("X",7.5,15,1,1),),(),
            tuple(Vehicle(f"veh{i:04d}",0,("X",),eligible=(i==0)) for i in range(1000)))
        out=predict_counterfactual(s,"veh0000",("X",),MovementMap(()),
                                   params=Parameters(q_sat=.35,max_wall_s=None))
        self.assertEqual(out.status,"ABSTAIN_NONCOMPLETION")
        self.assertIsNone(out.pred_all_delta_network_s)
        self.assertEqual(out.per_driver_swap_s,{})

    def test_V22_tier_c_fairness_without_priority(self):
        a=m("J",0,"P","Q",cont=True)
        b=m("J",1,"R","S",cont=False)
        cases=(Candidate("a",a),Candidate("b",b))
        first=select(cases,("P","R"),0,{"Q":1,"S":1})
        second=select(cases,("P","R"),first.pointer_after,{"Q":1,"S":1})
        self.assertEqual(first.accepted[0].vehicle_id,"a")
        self.assertEqual(second.accepted[0].vehicle_id,"b")

    def test_V23_minimum_road_time_and_snapshot_space(self):
        s,mm,p=independent_case()
        evo=evolve_v2(s,mm,p)
        inserted={e.vehicle_id:e.tick for e in evo.events if e.action=="insert"}
        crossed={e.vehicle_id:e.tick for e in evo.events if e.action=="cross"}
        self.assertTrue(all(crossed[vid]>inserted[vid] for vid in crossed))
        # Two original same-second vehicles cannot overfill one-slot destination.
        rr=(Turn("P","Q","J"),Turn("R","Q","J"))
        s2=Scenario(road_set("P","R","Q",storage=1),rr,
            (Vehicle("a",0,("P","Q")),Vehicle("b",0,("R","Q"))))
        mm2=MovementMap((m("J",0,"P","Q"),m("J",1,"R","Q")))
        self.assertEqual(len(evolve_v2(s2,mm2).arrivals),2)

    def test_V24_offline_1000_driver_scaling_report(self):
        # Synthetic 40 disjoint one-edge roads: 25 scheduled per road, 1,000 IDs.
        links=tuple(Link(f"R{i}",15,15,1,8) for i in range(40))
        people=tuple(Vehicle(f"veh{i:04d}",(i//40)%25,(f"R{i%40}",),
                             eligible=i%2==0) for i in range(1000))
        s=Scenario(links,(),people)
        t=time.perf_counter()
        ev=evolve_v2(s,MovementMap(()),Parameters(max_wall_s=None))
        wall=time.perf_counter()-t
        self.assertEqual(len(ev.arrivals),1000)
        print(f"V2-I2 no-SUMO offline 1000 synthetic elapsed_seconds={wall:.3f}")


if __name__=="__main__":
    unittest.main()
