#!/usr/bin/env python3
import unittest, xml.etree.ElementTree as ET
from g3_native_vehroute_v01 import extract_events

class NativeExitTimeTests(unittest.TestCase):
    def test_interleaved_external_internal_and_repeated_road(self):
        root=ET.fromstring('<routes><vehicle id="v1" depart="0" arrival="10"><route edges="A :J_0 B :J_1 A" exitTimes="2 3 7 8 10"/></vehicle></routes>')
        events,vehicles,issues=extract_events(root)
        self.assertFalse(issues)
        self.assertEqual(vehicles['v1']['external_route'],['A','B','A'])
        self.assertEqual(vehicles['v1']['internal_links'],2)
        self.assertEqual([x['interval_s'] for x in events],[2.,1.,4.,1.,2.])
        self.assertEqual(events[1]['kind'],'internal')
        self.assertEqual(events[4]['enter_at_prior_exit_s'],8.)
    def test_route_distribution_is_supported(self):
        root=ET.fromstring('<routes><vehicle id="v" depart="2" arrival="3"><routeDistribution><route edges="A :J B" exitTimes="2 3 3"/></routeDistribution></vehicle></routes>')
        events,veh,issues=extract_events(root)
        self.assertEqual(len(events),3)
        self.assertEqual(len(veh),1)
        self.assertFalse(issues)
    def test_missing_native_exittime_is_rejected(self):
        root=ET.fromstring('<routes><vehicle id="v" depart="1" arrival="3"><route edges="A :J B" exitTimes="2 3"/></vehicle></routes>')
        ev,veh,issues=extract_events(root)
        self.assertEqual(len(veh),0)
        self.assertEqual(issues[0]['issue'],'edge_exittime_count_mismatch')
    def test_time_regression_is_visible(self):
        root=ET.fromstring('<routes><vehicle id="v" depart="1" arrival="4"><route edges="A B" exitTimes="3 2"/></vehicle></routes>')
        ev,veh,issues=extract_events(root)
        self.assertEqual(issues[0]['issue'],'nonmonotone_exit_times')
        self.assertEqual(len(veh),0)
    def test_monotone_equal_timestep_is_allowed(self):
        root=ET.fromstring('<routes><vehicle id="v" depart="1" arrival="2"><route edges="A :J B" exitTimes="2 2 2"/></vehicle></routes>')
        ev,veh,issues=extract_events(root)
        self.assertEqual(len(ev),3)
        self.assertFalse(issues)
        self.assertEqual(ev[2]['interval_s'],0.)
if __name__=='__main__':unittest.main()
