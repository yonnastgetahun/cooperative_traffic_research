"""Additional no-SUMO integration fixtures: static SUMO XML and partition contract."""
import tempfile
import unittest
from pathlib import Path

from research.externality_estimator.schema import InvalidScenario, Scenario, Link, Turn, Vehicle
from research.externality_estimator.scenario_io import from_sumo_static_xml
from research.externality_estimator.candidate_routes import legal_alternatives,check_candidate
from research.externality_estimator.audit import check_partition
from research.externality_estimator.dataset_contract import select_development_probes
from research.externality_estimator.counterfactual_rollout import predict_counterfactual


class StaticInputContract(unittest.TestCase):
    def test_static_sumo_xml_parsing_no_simulation(self):
        net='''<net>
         <edge id="A" from="n0" to="n1"><lane id="A_0" index="0" length="15" speed="15"/></edge>
         <edge id="B" from="n1" to="n2"><lane id="B_0" index="0" length="15" speed="15"/></edge>
         <edge id="C" from="n1" to="n2"><lane id="C_0" index="0" length="15" speed="15"/></edge>
         <edge id="Z" from="n2" to="n3"><lane id="Z_0" index="0" length="15" speed="15"/></edge>
         <connection from="A" to="B" fromLane="0" toLane="0"/>
         <connection from="A" to="C" fromLane="0" toLane="0"/>
         <connection from="B" to="Z" fromLane="0" toLane="0"/>
         <connection from="C" to="Z" fromLane="0" toLane="0"/>
         </net>'''
        trips='''<trips><trip id="veh0000" depart="0.200" from="A" to="Z"/>
                       <trip id="veh0001" depart="1.400" from="A" to="Z"/></trips>'''
        routes='''<routes><vehicle id="veh0000" depart="0.200"><route edges="A B Z"/></vehicle>
                         <vehicle id="veh0001" depart="1.400"><route edges="A C Z"/></vehicle></routes>'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            for name,data in [('net.xml',net),('trips.xml',trips),('routes.xml',routes)]:
                (p/name).write_text(data)
            s=from_sumo_static_xml(p/'net.xml',p/'trips.xml',p/'routes.xml')
        self.assertEqual(len(s.links),4)
        self.assertEqual(len(s.turns),4)
        self.assertEqual(s.vehicles[0].scheduled_departure_s,.2)
        self.assertEqual(s.vehicles[1].scheduled_departure_s,1.4)
        self.assertTrue(s.vehicles[0].eligible)
        self.assertFalse(s.vehicles[1].eligible)
        p=predict_counterfactual(s,'veh0000',('A','C','Z'))
        self.assertEqual(p.status,'OK')

    def test_candidate_rejects_endpoint_and_nominal_detour(self):
        edges=(Link('A',15,15),Link('B',15,15),Link('C',15,15),Link('Z',15,15),Link('D',30,15))
        turns=(Turn('A','B','J1'),Turn('A','C','J1'),Turn('A','D','J1'),
               Turn('B','Z','J2'),Turn('C','Z','J2'),Turn('D','Z','J2'))
        s=Scenario(edges,turns,(Vehicle('veh0000',0,('A','B','Z'),True),))
        self.assertEqual(legal_alternatives(s,'veh0000')[0],('A','B','Z'))
        check_candidate(s,'veh0000',('A','C','Z'))
        with self.assertRaises(InvalidScenario):
            check_candidate(s,'veh0000',('A','D','Z'))
        with self.assertRaises(InvalidScenario):
            check_candidate(s,'veh0000',('B','Z'))

    def test_partitions_cannot_swap_build_and_check(self):
        check_partition(5101,'DEV_BUILD')
        check_partition(5111,'DEV_CHECK')
        with self.assertRaises(InvalidScenario):
            check_partition(5101,'DEV_CHECK')
        with self.assertRaises(InvalidScenario):
            check_partition(4201,'DEV_BUILD')


if __name__ == '__main__':
    unittest.main()
