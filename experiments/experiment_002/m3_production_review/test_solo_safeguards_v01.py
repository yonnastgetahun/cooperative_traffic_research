import unittest
from solo_safeguards_v01 import assess_solo,authorize_heldout

def env(wait=10,bypass=False,protected=True,review=False):
    rules=[{"type":"wait_timer","wait_timer":wait}]
    if review:rules.append({"type":"required_reviewers","reviewers":[{"login":"x"}]})
    return {"protection_rules":rules,"can_admins_bypass":bypass,
            "deployment_branch_policy":{"protected_branches":protected}}

class SoloSafetyTests(unittest.TestCase):
    def setUp(self):
        self.branch={"protected":True}
        self.wf={"status":"ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED","active_heldout_workflows":[]}
    def test_expected_solo_configuration_is_review_only(self):
        r=assess_solo(env(),self.branch,self.wf)
        self.assertEqual(r["status"],"SOLO_CONTROLS_VERIFIED_REVIEW_ONLY")
        self.assertFalse(r["heldout_execution_authorized"])
    def test_missing_timer_fails(self):
        self.assertTrue(assess_solo(env(wait=0),self.branch,self.wf)["status"].startswith("BLOCKED"))
    def test_admin_bypass_fails(self):
        self.assertTrue(assess_solo(env(bypass=True),self.branch,self.wf)["status"].startswith("BLOCKED"))
    def test_missing_admin_field_fails(self):
        x=env();del x["can_admins_bypass"]
        self.assertTrue(assess_solo(x,self.branch,self.wf)["status"].startswith("BLOCKED"))
    def test_unprotected_branch_fails(self):
        self.assertTrue(assess_solo(env(),{"protected":False},self.wf)["status"].startswith("BLOCKED"))
    def test_unrestricted_deploy_fails(self):
        self.assertTrue(assess_solo(env(protected=False),self.branch,self.wf)["status"].startswith("BLOCKED"))
    def test_unexpected_reviewers_fail_solo_profile(self):
        self.assertTrue(assess_solo(env(review=True),self.branch,self.wf)["status"].startswith("BLOCKED"))
    def test_active_heldout_workflow_fails(self):
        wf=dict(self.wf,active_heldout_workflows=["m3-heldout.yml"])
        self.assertTrue(assess_solo(env(),self.branch,wf)["status"].startswith("BLOCKED"))
    def test_no_execution_bypass(self):
        with self.assertRaises(PermissionError):authorize_heldout(approved=True,seed=3101)

if __name__=="__main__":unittest.main()
