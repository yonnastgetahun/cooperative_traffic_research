"""Read-only, non-executing solo M3 safeguard verifier."""
FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"

def assess_solo(environment,branch,workflows):
    """No missing GitHub field is treated as evidence of protection."""
    rules=(environment or {}).get("protection_rules") or []
    wait=[r for r in rules if r.get("type")=="wait_timer"]
    timer=any(r.get("wait_timer")==10 for r in wait)
    policy=(environment or {}).get("deployment_branch_policy") or {}
    protected=policy.get("protected_branches") is True
    bypass=(environment or {}).get("can_admins_bypass") is False
    no_reviewers=not any(r.get("type")=="required_reviewers" for r in rules)
    branch_ok=(branch or {}).get("protected") is True
    workflows_ok=(workflows or {}).get("status")=="ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED" and not workflows.get("active_heldout_workflows")
    checks=dict(wait_timer_10_minutes_verified=timer,protected_branches_only_verified=protected,
        admin_bypass_disabled_verified=bypass,no_required_reviewers_verified=no_reviewers,
        main_protected_verified=branch_ok,active_heldout_workflow_absent=workflows_ok)
    return dict(status="SOLO_CONTROLS_VERIFIED_REVIEW_ONLY" if all(checks.values()) else "BLOCKED_UNVERIFIED_SOLO_CONTROLS",
        checks=checks,independent_review=False,heldout_execution_authorized=False,
        note="Even all checks passing does not authorize evaluation or replace explicit release approval.")

def authorize_heldout(*args,**kwargs):
    raise PermissionError("Held-out evaluation not authorized by operational amendment or tests")
