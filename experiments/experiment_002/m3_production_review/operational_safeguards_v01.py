#!/usr/bin/env python3
"""M3 operational safeguards — read-only repository and API evidence.

This script cannot enable or execute held-out simulation. Inspect existing
workflow files and extract/test the legacy free-form seed input guard.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
PROTECTED_ENV="m3-holdout-reviewers"
LEGACY_CALIBRATION="experiment-001-calibration.yml"
RESERVED=tuple(range(3101,3111))

def legacy_python_guard(source):
    m=re.search(r"(?m)^\s*# Research integrity: reserved M3 validation seeds.*?^\s*python3 - <<'PY'\n(?P<body>.*?)^\s*PY\s*$", source, re.S|re.M)
    if not m:
        raise RuntimeError("Older calibration lacks its pre-generation seed guard")
    return textwrap.dedent(m.group("body"))

def test_seed_guard(source):
    snippet=legacy_python_guard(source)
    tested={}
    for seed in (*RESERVED,1001,2101,2103,"bad;text"):
        p=subprocess.run([sys.executable,"-c",snippet],
             env={**os.environ,"SEED":str(seed)},capture_output=True,text=True,timeout=5)
        expected=int(seed) not in RESERVED if str(seed).isdigit() else False
        actual=(p.returncode==0)
        if actual!=expected:
            raise RuntimeError("Legacy seed guard failed for "+str(seed))
        tested[str(seed)]="accepted_dev" if actual else "rejected"
    return tested

def inspect_workflows(root):
    root=pathlib.Path(root)
    folder=root/".github/workflows"
    if not folder.is_dir():raise RuntimeError("No active workflow directory")
    files=sorted(folder.glob("*.yml"))+sorted(folder.glob("*.yaml"))
    active_heldout=[]
    uncontrolled=[]
    forms=[]
    for path in files:
        text=path.read_text()
        name=path.name
        if re.search(r"(?i)heldout.*(?:execution|evaluate).*\.ya?ml$",name):
            active_heldout.append(name)
        direct_seed=re.findall(r"\$\{\{\s*(?:inputs|github\.event\.inputs)\.seed\s*\}\}",text)
        if direct_seed:
            forms.append(name)
            if name!=LEGACY_CALIBRATION:
                uncontrolled.append(name)
        if re.search(r"(?m)^\s*seed:\s*\[\s*3101(?:\s*[,\]])",text):
            uncontrolled.append(name)
    legacy=folder/LEGACY_CALIBRATION
    if not legacy.is_file():raise RuntimeError("Missing older calibration workflow")
    c=legacy.read_text()
    if "netgenerate" not in c or c.index("M3 held-out seed RESERVED")>c.index("netgenerate"):
        raise RuntimeError("Reserved seed check must appear before demand/network generation")
    if "--seed ${{ inputs.seed }}" in c:
        raise RuntimeError("Unquoted input interpolation remains in simulator command")
    guard=test_seed_guard(c)
    from activation_gate_v01 import inspect_inactive_template
    disabled=inspect_inactive_template(root)
    return dict(status="ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED" if not active_heldout and not uncontrolled else "UNSAFE_ACTIVE_WORKFLOW_PATH",
        active_workflow_count=len(files),
        active_heldout_workflows=active_heldout,
        user_seed_input_workflows=forms,
        unguarded_user_seed_workflows=uncontrolled,
        legacy_seed_guard_test=guard,
        inactive_template_check=disabled,
        source_scan_limit="Static source audit plus executable legacy guard test; cannot constrain admins manually editing workflows or running scripts elsewhere.")

def api_get(repo,resource,token):
    url=f"https://api.github.com/repos/{repo}/{resource}"
    headers={"Accept":"application/vnd.github+json","User-Agent":"M3-NonExecuting-SafeguardAudit",
             "X-GitHub-Api-Version":"2022-11-28"}
    if token:headers["Authorization"]="Bearer "+token
    try:
        req=urllib.request.Request(url,headers=headers,method="GET")
        with urllib.request.urlopen(req,timeout=10) as response:
            return response.status,json.loads(response.read())
    except urllib.error.HTTPError as e:
        return e.code,None
    except (urllib.error.URLError,TimeoutError,ValueError):
        return None,None

def assess_environment(data,status):
    """Fail CLOSED: unavailable rule fields never become proof of protection."""
    if status!=200 or not isinstance(data,dict):
        return dict(status="NOT_VERIFIED",http_status=status,
             required_reviewers_verified=False,prevent_self_review_verified=False,
             admin_bypass_disabled_verified=False,
             reviewer_count=0,protected_branch_policy_verified=False)
    rules=data.get("protection_rules") or []
    reviews=[r for r in rules if r.get("type")=="required_reviewers"]
    reviewer_count=max((len(r.get("reviewers") or []) for r in reviews),default=0)
    # GitHub API versions have exposed prevent_self_review on environment or rule.
    prevent=(data.get("prevent_self_review") is True or
             any(r.get("prevent_self_review") is True for r in reviews))
    no_admin=data.get("can_admins_bypass") is False
    policy=data.get("deployment_branch_policy") or {}
    branch_restricted=(policy.get("protected_branches") is True or
                       policy.get("custom_branch_policies") is True)
    all_ok=reviewer_count>0 and prevent and no_admin and branch_restricted
    return dict(status="VERIFIED_STRONG_PROTECTION" if all_ok else "INCOMPLETE_OR_UNVERIFIED",
        http_status=status,
        required_reviewers_verified=reviewer_count>0,
        reviewer_count=reviewer_count,
        prevent_self_review_verified=prevent,
        admin_bypass_disabled_verified=no_admin,
        protected_branch_policy_verified=branch_restricted,
        # No reviewer login IDs or personal info are reported.
        environment_exists=data.get("name")==PROTECTED_ENV)

def assess_branch(data,status):
    if status!=200 or not isinstance(data,dict):
        return dict(status="NOT_VERIFIED",http_status=status)
    return dict(status="PROTECTED" if data.get("protected") is True else "NOT_PROTECTED",
                http_status=status,protected=data.get("protected"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True)
    p.add_argument("--repo",required=True)
    p.add_argument("--report",required=True)
    a=p.parse_args()
    workflows=inspect_workflows(a.root)
    token=os.environ.get("GITHUB_TOKEN")
    env_status,env_data=api_get(a.repo,"environments/"+PROTECTED_ENV,token)
    branch_status,branch_data=api_get(a.repo,"branches/main",token)
    env=assess_environment(env_data,env_status)
    branch=assess_branch(branch_data,branch_status)
    report=dict(schema="exp002-m3-operational-readiness-v0.1",
       status="REVIEW_COMPLETE_EXECUTION_BLOCKED",
       scientific_commit=FROZEN_SHA,active_workflows=workflows,
       environment=env,main_branch=branch,
       heldout_execution_authorized=False,heldout_seeds_generated_or_run=False,
       evaluation_activation_ready=(workflows["status"]=="ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED" and
            env["status"]=="VERIFIED_STRONG_PROTECTION" and branch["status"]=="PROTECTED"),
       actions_taken="GET repository settings and static guard checks only. No environment created or workflow dispatched.",
       next_step="Require human-configured protected environment/reviewers and branch protection, then independently verify before future execution authorization")
    pathlib.Path(a.report).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="active_workflows"},indent=2))
    if workflows["status"]!="ACTIVE_REPO_M3_HELDOUT_PATH_GUARDED":
        raise RuntimeError("Existing Actions have an unguarded path to reserved seeds")

if __name__=="__main__":main()
