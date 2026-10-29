import hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import production_bundle_validator_v01 as v
from adapters_v01 import Ineligible,FROZEN_SHA,SUMO_IMAGE

class BundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.seed=101
        self.window=200
        self.files={
          "seed-level-metrics.json":json.dumps({"vehicles":1000}).encode(),
          "r3-exception-audit.json":json.dumps({"seed":101}).encode(),
          "paired-reference-report.json":b"{}",
          "network.net.xml":b"<net/>","trips.xml":b"<routes/>",
          "original.rou.xml":b"<routes/>"}
        for name,data in self.files.items():(self.root/name).write_bytes(data)
        self.manifest=dict(seed=101,window_seconds=200,scientific_commit=FROZEN_SHA,
            sumo_image=SUMO_IMAGE,od_pair_sha256="f"*64,
            route_audit_byte_identical=True,
            files={name:hashlib.sha256(data).hexdigest() for name,data in self.files.items()})
        self.save()
    def save(self):
        (self.root/"scenario-manifest.json").write_text(json.dumps(self.manifest))
    def test_valid_manifest_passes_to_original_scoring_adapter(self):
        with patch.object(v,"seed_record",return_value={"status":"synthetic"}) as f:
            self.assertEqual(v.validate_bundle(self.root,101,200)["status"],"synthetic")
            self.assertEqual(f.call_args.args[:2],(101,200))
    def test_wrong_seed_rejected(self):
        with self.assertRaises(Ineligible):v.validate_bundle(self.root,102,200)
    def test_wrong_image_rejected(self):
        self.manifest["sumo_image"]="latest";self.save()
        with self.assertRaises(Ineligible):v.validate_bundle(self.root,101,200)
    def test_tampered_bytes_rejected(self):
        (self.root/"trips.xml").write_bytes(b"tampered")
        with self.assertRaises(Ineligible):v.validate_bundle(self.root,101,200)
    def test_missing_file_rejected(self):
        del self.manifest["files"]["original.rou.xml"];self.save()
        with self.assertRaises(Ineligible):v.validate_bundle(self.root,101,200)
    def test_path_traversal_rejected(self):
        self.manifest["files"]["../outside"]="a"*64;self.save()
        with self.assertRaises(Ineligible):v.validate_bundle(self.root,101,200)
    def test_missing_scenario_never_substituted(self):
        with self.assertRaises(Ineligible):v.validate_registry(self.root,tuple(range(3101,3111)),lambda x:None)
    def test_registry_drift_rejected(self):
        with self.assertRaises(Ineligible):v.validate_registry(self.root,[101]*10,lambda x:None)

if __name__=="__main__":unittest.main()
