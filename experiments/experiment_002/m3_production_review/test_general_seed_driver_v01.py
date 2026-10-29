import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from general_seed_driver_v01 import scenario_plan,commands,run_development,Blocked,FROZEN_SHA

class DriverTests(unittest.TestCase):
 def test_inspected_development_seed_only(self):
  self.assertEqual(scenario_plan(2101,200)["mode"],"development_rehearsal")
 def test_all_reserved_seeds_denied(self):
  for seed in range(3101,3111):
   with self.assertRaises(Blocked):scenario_plan(seed,200)
 def test_invalid_windows_denied(self):
  for window in (0,100,300,999):
   with self.assertRaises(Blocked):scenario_plan(2101,window)
 def test_unknown_seed_denied(self):
  with self.assertRaises(Blocked):scenario_plan(9999,200)
 def test_original_frozen_generator_and_predictor_pinned(self):
  cs=commands("/tmp/m3-synthetic-only",2101,600)
  self.assertEqual(len(cs),4)
  self.assertIn("fixed_demand_v01.py",cs[1][1])
  self.assertIn("trace_actual_predictor.py",cs[2][1])
  self.assertEqual(cs[3][0],"sumo")
  self.assertIn("--vehroute-output.internal",cs[3])
 def test_no_execution_when_sha_mismatch(self):
  with tempfile.TemporaryDirectory() as d,patch("general_seed_driver_v01.subprocess.run") as run:
   with self.assertRaises(Blocked):run_development(d,2101,200,"wrong")
   run.assert_not_called()
 def test_no_files_or_subprocess_for_reserved_seed(self):
  with tempfile.TemporaryDirectory() as d,patch("general_seed_driver_v01.subprocess.run") as run:
   p=Path(d)/"out"
   with self.assertRaises(Blocked):run_development(p,3101,200,FROZEN_SHA)
   self.assertFalse(p.exists())
   run.assert_not_called()
 def test_no_implicit_evaluation_permission(self):
  self.assertFalse(scenario_plan(2101,1200)["evaluation_authorized"])

if __name__=="__main__":unittest.main()
