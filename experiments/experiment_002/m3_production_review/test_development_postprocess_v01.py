import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from development_postprocess_v01 import require_seed,postprocess,RehearsalBlocked,FROZEN_SHA

class PostprocessTests(unittest.TestCase):
 def test_all_reserved_seeds_rejected(self):
  for s in range(3101,3111):
   with self.assertRaises(RehearsalBlocked):require_seed(s,200)
 def test_only_prespecified_windows(self):
  for w in (100,300,0):
   with self.assertRaises(RehearsalBlocked):require_seed(2101,w)
 def test_inspected_seed_allowed(self):
  for w in (200,600,1200):self.assertIsNone(require_seed(2101,w))
 def test_no_side_effect_on_reserved_seed(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/"output"
   with self.assertRaises(RehearsalBlocked):postprocess(d,target,d,3101,200)
   self.assertFalse(target.exists())
 def test_missing_archived_source_fails_before_writing(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/"output"
   with self.assertRaises(RehearsalBlocked):postprocess(d,target,d,2101,200)
   self.assertFalse(target.exists())
 def test_no_execution_ever_imported(self):
  import inspect,development_postprocess_v01 as m
  src=inspect.getsource(m)
  self.assertNotIn("subprocess.run(",src)
  self.assertNotIn("netgenerate --grid",src)
  self.assertNotIn("sumo -n",src)
 def test_scientific_sha_fixed(self):
  self.assertEqual(FROZEN_SHA,"be2e8d27c78c8b6de4891115d6d951edc877ac6e")

if __name__=="__main__":unittest.main()
