#!/usr/bin/env python3
"""Non-executable M3 activation guard and workflow-template checks.

No way to grant execution from this module: a new explicit user approval,
separately reviewed code change, and verified GitHub environment protections
will be required before any held-out job may be enabled.
"""
from pathlib import Path
import re

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
REVIEW_ONLY=True
HELDOUT_EXECUTION_ENABLED=False
RESERVED_SEEDS=tuple(range(3101,3111))
REQUIRED_MANUAL_EVENT="workflow_dispatch"
PROPOSED_REVIEW_ENVIRONMENT="m3-holdout-reviewers"

class ActivationBlocked(PermissionError):
    pass

def assert_not_executing_reserved_seed(seed):
    if int(seed) in RESERVED_SEEDS:
        raise ActivationBlocked("No approval for reserved M3 seed execution, generation or preview")
    return True

def require_heldout_execution_authorization(*args,**kwargs):
    # Deliberately no receipt, token or user-provided bypass option.
    raise ActivationBlocked(
        "M3 held-out evaluation is NOT authorized. A separately reviewed "
        "protected-environment workflow and explicit later user approval are required.")

def inspect_inactive_template(root):
    """Inspect review template only, never execute it or register a workflow."""
    root=Path(root)
    path=root/"docs/templates/experiment-002-m3-heldout-evaluation.yml.disabled"
    if not path.is_file():
        raise ActivationBlocked("Inactive template not found")
    if str(path).endswith(".github/workflows"):
        raise ActivationBlocked("The template must not be an active workflow")
    text=path.read_text(encoding="utf8")
    if "workflow_dispatch:" not in text:
        raise ActivationBlocked("Manual dispatch requirement missing")
    # Each job must have a literal hard-disabled condition.
    jobs=re.findall(r"^  (explicit-activation-approval|evaluate|aggregate-if-all-eligible):\s*$",text,re.M)
    disabled=re.findall(r"^    if: false\s*$",text,re.M)
    if set(jobs)!={"explicit-activation-approval","evaluate","aggregate-if-all-eligible"} or len(disabled)!=3:
        raise ActivationBlocked("All three held-out jobs must remain hard disabled")
    if FROZEN_SHA not in text:
        raise ActivationBlocked("Frozen source commit missing from inactive template")
    return dict(status="INACTIVE_NOT_AUTHORIZED",
        frozen_scientific_commit=FROZEN_SHA,
        heldout_execution_enabled=HELDOUT_EXECUTION_ENABLED,
        manual_event_required=REQUIRED_MANUAL_EVENT,
        proposed_protected_environment=PROPOSED_REVIEW_ENVIRONMENT,
        protected_environment_reviewers_verified=False,
        template_job_count=len(jobs),disabled_job_count=len(disabled),
        caveat="Template is outside active Actions directory. Protected environment has not been configured or independently verified.")

def inspect_active_workflow_inventory(root):
    root=Path(root)
    wf=root/".github/workflows"
    if not wf.is_dir():
        raise ActivationBlocked("Cannot verify active workflow directory")
    forbidden=[]
    for file in wf.glob("*.yml"):
        text=file.read_text(encoding="utf8")
        if re.search(r"^\s*seed:\s*\[\s*3101\b",text,re.M):
            forbidden.append(str(file))
        if re.search(r"\bheldout[-_ ]?evaluation\b",file.stem,re.I):
            forbidden.append(str(file))
    if forbidden:
        raise ActivationBlocked("Active heldout seeds/workflow unexpectedly present: "+str(forbidden))
    return dict(checked_active_workflow_files=len(list(wf.glob("*.yml"))),
                active_heldout_evaluation_workflow_found=False)

if __name__=="__main__":
    raise ActivationBlocked("Review-only activation safeguards have no executable CLI")
