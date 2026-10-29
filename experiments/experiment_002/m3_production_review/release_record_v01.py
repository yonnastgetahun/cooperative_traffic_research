"""M3 held-out release-record validator: pure, deliberately non-executing.

No GitHub Actions job or simulator is invoked. The guard is not an approval
mechanism by itself: actual user approval must occur in a separate later turn.
"""
from datetime import datetime, timezone

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
SUMO_IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
SEEDS=tuple(range(3101,3111))
WINDOWS=(200,600,1200)

class ReleaseBlocked(RuntimeError):pass

def review_release_record(record):
    """Validate a hypothetical release record; never authorize execution."""
    if not isinstance(record,dict):raise ReleaseBlocked("No reviewed release record")
    required=("scientific_commit","sumo_image","seed_ids","windows","review_commit",
              "approval_reference","approved_scope","approved_at_utc")
    if any(k not in record for k in required):
        raise ReleaseBlocked("Incomplete release provenance")
    if record["scientific_commit"]!=FROZEN_SHA or record["sumo_image"]!=SUMO_IMAGE:
        raise ReleaseBlocked("Frozen scientific code or SUMO image drift")
    if type(record["seed_ids"]) is not list or record["seed_ids"]!=list(SEEDS):
        raise ReleaseBlocked("Seed registry differs from frozen study")
    if type(record["windows"]) is not list or record["windows"]!=list(WINDOWS):
        raise ReleaseBlocked("Congestion regime registry differs")
    if record["approved_scope"]!="M3_HELDOUT_30_SCENARIOS":
        raise ReleaseBlocked("Wrong explicit execution scope")
    if not isinstance(record["review_commit"],str) or len(record["review_commit"])!=40 or any(c not in "0123456789abcdef" for c in record["review_commit"]):
        raise ReleaseBlocked("Unpinned runner review commit")
    if not isinstance(record["approval_reference"],str) or not record["approval_reference"].strip():
        raise ReleaseBlocked("Missing independently recorded user approval reference")
    try:
        approved=datetime.fromisoformat(record["approved_at_utc"].replace("Z","+00:00"))
        if approved.tzinfo is None:raise ValueError()
    except (ValueError,AttributeError,TypeError):
        raise ReleaseBlocked("Approval timestamp invalid")
    return {"status":"STRUCTURE_VALID_ONLY_NOT_EXECUTION_AUTHORIZATION",
            "scientific_commit":FROZEN_SHA,"seed_count":10,"regime_count":3,
            "execution_authorized":False}

def authorize_execution(*args,**kwargs):
    raise ReleaseBlocked("Release-record review cannot authorize or dispatch held-out evaluation")
