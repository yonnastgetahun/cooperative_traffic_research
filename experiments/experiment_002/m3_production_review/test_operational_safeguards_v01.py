#!/usr/bin/env python3
"""Operational-safeguard fixtures: no SUMO, secrets, deployment or evaluation."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
import operational_safeguards_v01 as m

ROOT=Path(__file__).resolve().parents[3]

class Operations(unittest.TestCase):
    def test_existing_legacy_manual_seed_input_is_actually_guarded(self):
        src=(ROOT/".github/workflows/experiment-001-calibration.yml").read_text()
        outcomes=m.test_seed_guard(src)
        for n in range(3101,3111):
            self.assertEqual(outcomes[str(n)],"rejected")
        self.assertEqual(outcomes["2101"],"accepted_dev")
        self.assertEqual(outcomes["bad;text"],"rejected")
    def test_active_workflow_inventory_has_no_heldout_executable_workflow(self):
        result=m.inspect_workflows(ROOT)
        self.assertEqual(result["status"],"ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED")
        self.assertEqual(result["active_heldout_workflows"],[])
        self.assertEqual(result["unguarded_user_seed_workflows"],[])
        self.assertIn("experiment-001-calibration.yml",result["user_seed_input_workflows"])
        self.assertEqual(result["inactive_template_check"]["disabled_job_count"],3)
    def test_environment_404_cannot_be_called_verified(self):
        e=m.assess_environment(None,404)
        self.assertEqual(e["status"],"NOT_VERIFIED")
        self.assertFalse(e["required_reviewers_verified"])
        self.assertFalse(e["admin_bypass_disabled_verified"])
    def test_weak_environment_is_not_approved(self):
        data=dict(name="m3-holdout-reviewers",
            protection_rules=[dict(type="required_reviewers",reviewers=[dict(type="User")])],
            deployment_branch_policy=dict(protected_branches=False,custom_branch_policies=False),
            can_admins_bypass=True)
        e=m.assess_environment(data,200)
        self.assertEqual(e["status"],"INCOMPLETE_OR_UNVERIFIED")
        self.assertFalse(e["admin_bypass_disabled_verified"])
    def test_independent_approvals_and_branch_controls_are_all_required(self):
        data=dict(name="m3-holdout-reviewers",
            protection_rules=[dict(type="required_reviewers",prevent_self_review=True,
                                   reviewers=[dict(type="User")])],
            prevent_self_review=True,can_admins_bypass=False,
            deployment_branch_policy=dict(protected_branches=True,custom_branch_policies=False))
        self.assertEqual(m.assess_environment(data,200)["status"],"VERIFIED_STRONG_PROTECTION")
        for changed in [
            dict(data,can_admins_bypass=True),
            dict(data,prevent_self_review=False,protection_rules=[dict(type="required_reviewers",reviewers=[dict(type="User")])]),
            dict(data,protection_rules=[dict(type="required_reviewers",reviewers=[])]),
            dict(data,deployment_branch_policy=dict(protected_branches=False,custom_branch_policies=False))
        ]:
            self.assertNotEqual(m.assess_environment(changed,200)["status"],"VERIFIED_STRONG_PROTECTION")
    def test_main_branch_not_protected_is_not_ready(self):
        self.assertEqual(m.assess_branch(dict(protected=False),200)["status"],"NOT_PROTECTED")
        self.assertEqual(m.assess_branch(None,403)["status"],"NOT_VERIFIED")
        self.assertEqual(m.assess_branch(dict(protected=True),200)["status"],"PROTECTED")

if __name__=="__main__":unittest.main()
