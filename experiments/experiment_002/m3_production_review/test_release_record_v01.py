import unittest
from release_record_v01 import review_release_record,authorize_execution,ReleaseBlocked,FROZEN_SHA,SUMO_IMAGE,SEEDS,WINDOWS

def fixture():
    return dict(scientific_commit=FROZEN_SHA,sumo_image=SUMO_IMAGE,
        seed_ids=list(SEEDS),windows=list(WINDOWS),review_commit="a"*40,
        approval_reference="synthetic-only-placeholder",
        approved_scope="M3_HELDOUT_30_SCENARIOS",approved_at_utc="2026-10-28T00:00:00Z")

class ReleaseGuardTests(unittest.TestCase):
    def test_fixture_only_checks_structure(self):
        r=review_release_record(fixture())
        self.assertFalse(r["execution_authorized"])
    def test_no_release(self):
        with self.assertRaises(ReleaseBlocked):review_release_record(None)
    def test_wrong_seed(self):
        r=fixture();r["seed_ids"]=[3101]*10
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_missing_seed(self):
        r=fixture();r["seed_ids"].pop()
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_wrong_regimes(self):
        r=fixture();r["windows"]=[200,600]
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_science_drift(self):
        r=fixture();r["scientific_commit"]="b"*40
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_image_drift(self):
        r=fixture();r["sumo_image"]="latest"
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_missing_approval_reference(self):
        r=fixture();r["approval_reference"]=""
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_bad_timestamp(self):
        r=fixture();r["approved_at_utc"]="yesterday"
        with self.assertRaises(ReleaseBlocked):review_release_record(r)
    def test_no_authorization_even_with_valid_fixture(self):
        with self.assertRaises(ReleaseBlocked):authorize_execution(fixture())

if __name__=="__main__":unittest.main()
