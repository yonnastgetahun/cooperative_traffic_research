import json,tempfile,unittest
from pathlib import Path
from native_observation_integration_v01 import validate_observations,validate_identity,authorize,ObservationBlocked,REQUIRED_OBSERVATIONS,FROZEN_SHA

class NativeIntegrationTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.folder=Path(self.temp.name)
  for name in REQUIRED_OBSERVATIONS:(self.folder/name).write_text("synthetic")
  (self.folder/"paired-reference-report.json").write_text(json.dumps(dict(planned_edges=8393,matched=8393)))
  (self.folder/"r3-exception-audit.json").write_text(json.dumps(dict(seed=2101,window_seconds=200,exception_gate="PASS_FOR_THIS_REPLAY",reported_teleports=dict(teleport_state="ZERO_CONFIRMED",teleports_total=0))))
  (self.folder/"seed-level-metrics.json").write_text(json.dumps(dict(vehicles=1000,edge_traversals=8393,frozen_scientific_commit=FROZEN_SHA)))
 def test_synthetic_complete_cohort(self):
  x=validate_observations(self.folder,2101,200)
  self.assertEqual(len(x["source_sha256"]),len(REQUIRED_OBSERVATIONS))
  self.assertFalse(x["heldout_authorized"])
 def test_all_reserved_seeds_rejected(self):
  for s in range(3101,3111):
   with self.assertRaises(ObservationBlocked):validate_identity(s,200)
 def test_missing_fcd_rejected(self):
  (self.folder/"observed-fcd.xml").unlink()
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,200)
 def test_missing_native_edge_rejected(self):
  (self.folder/"native-external.xml").unlink()
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,200)
 def test_teleport_unknown_rejected(self):
  p=self.folder/"r3-exception-audit.json";d=json.loads(p.read_text());d["reported_teleports"]["teleport_state"]="UNKNOWN_NOT_CAPTURED";p.write_text(json.dumps(d))
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,200)
 def test_incomplete_join_rejected(self):
  p=self.folder/"paired-reference-report.json";p.write_text(json.dumps(dict(planned_edges=8393,matched=8392)))
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,200)
 def test_wrong_frozen_commit_rejected(self):
  p=self.folder/"seed-level-metrics.json";d=json.loads(p.read_text());d["frozen_scientific_commit"]="wrong";p.write_text(json.dumps(d))
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,200)
 def test_wrong_regime_rejected(self):
  with self.assertRaises(ObservationBlocked):validate_observations(self.folder,2101,300)
 def test_execution_blocked(self):
  with self.assertRaises(ObservationBlocked):authorize(seed=3101)

if __name__=="__main__":unittest.main()
