import tempfile,unittest
from pathlib import Path
from development_integration_v01 import (
 plan_development,check_archive,execution_authorization,
 IntegrationBlocked,REQUIRED,FROZEN_SHA,IMAGE)

class DevelopmentIntegrationTests(unittest.TestCase):
 def test_three_fixed_regimes(self):
  plans=plan_development()
  self.assertEqual([x.window for x in plans],[200,600,1200])
  self.assertTrue(all(x.seed==2101 and x.frozen_sha==FROZEN_SHA and x.sumo_image==IMAGE for x in plans))
 def test_reserved_seed_is_rejected(self):
  for seed in range(3101,3111):
   with self.assertRaises(IntegrationBlocked):plan_development(seed)
 def test_other_development_seeds_not_in_this_rehearsal(self):
  with self.assertRaises(IntegrationBlocked):plan_development(2102)
 def test_wrong_or_reordered_windows_rejected(self):
  for windows in ((200,600),(600,200,1200),(200,200,1200)):
   with self.assertRaises(IntegrationBlocked):plan_development(2101,windows)
 def test_archive_missing_is_blocking(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(IntegrationBlocked):check_archive(d,plan_development()[0])
 def test_complete_archive_is_hash_manifest_only(self):
  with tempfile.TemporaryDirectory() as d:
   for name in REQUIRED:(Path(d)/name).write_text("synthetic fixture")
   r=check_archive(d,plan_development()[0])
   self.assertEqual(len(r["source_sha256"]),len(REQUIRED))
   self.assertFalse(r["heldout_authorized"])
 def test_changed_file_changes_digest(self):
  with tempfile.TemporaryDirectory() as d:
   for name in REQUIRED:(Path(d)/name).write_text("a")
   before=check_archive(d,plan_development()[0])
   (Path(d)/"trips.xml").write_text("b")
   after=check_archive(d,plan_development()[0])
   self.assertNotEqual(before["source_sha256"]["trips.xml"],after["source_sha256"]["trips.xml"])
 def test_execution_never_authorized(self):
  with self.assertRaises(IntegrationBlocked):execution_authorization(seed=3101,approved=True)

if __name__=="__main__":unittest.main()
