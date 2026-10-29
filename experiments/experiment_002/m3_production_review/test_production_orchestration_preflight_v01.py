import tempfile
import unittest
from pathlib import Path
from production_orchestration_preflight_v01 import (
    planned_registry, inspect_plan, frozen_preflight, require_execution_authorization,
    PreflightBlocked)
from release_record_v01 import ReleaseBlocked
from adapters_v01 import FROZEN_SHA, SUMO_IMAGE

class ProductionPreflightTests(unittest.TestCase):
    def test_complete_registry(self):
        self.assertEqual(inspect_plan(planned_registry())["scenarios"], 30)
    def test_missing_and_duplicate(self):
        a=list(planned_registry())
        with self.assertRaises(PreflightBlocked):inspect_plan(a[:-1])
        a[-1]=a[0]
        with self.assertRaises(PreflightBlocked):inspect_plan(a)
    def test_unexpected_execution_state(self):
        a=list(planned_registry());a[0]=dict(a[0],state="COMPLETE")
        with self.assertRaises(PreflightBlocked):inspect_plan(a)
    def test_dispatch_always_blocked(self):
        with self.assertRaises(ReleaseBlocked):require_execution_authorization()
    def test_immutable_frozen_source_preflight(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            p=root/"docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json"
            p.parent.mkdir(parents=True);p.write_text("{}")
            q=root/"experiments/experiment_002/time_aware.py"
            q.parent.mkdir(parents=True);q.write_text("# test")
            self.assertEqual(frozen_preflight(root,FROZEN_SHA,SUMO_IMAGE)["scientific_commit"],FROZEN_SHA)
            with self.assertRaises(PreflightBlocked):frozen_preflight(root,"wrong",SUMO_IMAGE)
            with self.assertRaises(PreflightBlocked):frozen_preflight(root,FROZEN_SHA,"latest")

if __name__=="__main__":
    unittest.main(verbosity=2)
