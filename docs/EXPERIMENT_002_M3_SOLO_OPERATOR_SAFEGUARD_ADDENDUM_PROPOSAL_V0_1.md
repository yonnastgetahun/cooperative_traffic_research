# Experiment 002 — M3 Solo-Operator Operational Safeguards: PROPOSED Addendum v0.1

**Date:** October 27, 2026, America/Los_Angeles.  
**Status:** **DRAFT FOR REVIEW; NOT AN EXECUTION APPROVAL.** No held-out workflow enabled and no reserved seeds 3101–3110 generated, previewed, or simulated.  
**Owner context:** This is a solo-maintained GitHub research repository. Independent human approval is unavailable; the original operational two-person approval requirement cannot be satisfied without another eligible collaborator. This proposal explicitly records a **weaker alternative**, not an equivalent substitute.  
**Unchanged scientific freeze:** [M3 protocol v1.0](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md) at `be2e8d27c78c8b6de4891115d6d951edc877ac6e`. All R0–R4 scientific/measurement definitions, original policy, outcomes, eligibility rules, ten-seed statistical method, and seed registry remain unchanged.

## Verified GitHub state at drafting time

- Live GitHub ruleset `Protect main - M3 Research`, id **26009049**, is **active** and targets `~DEFAULT_BRANCH` (`main`).
- `main` reports **protected: true**. The ruleset requires a PR before merging, **0** required external approvals (appropriate for solo maintenance), dismisses stale reviews, requires resolved review threads, and restricts deletion and non-fast-forward pushes. Its bypass list is empty.
- Redundant ruleset id **26009401** was deleted and is no longer returned.
- A [successful **read-only** safeguard rerun](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40581795907) (attempt 2, October 27) confirms environment `m3-holdout-reviewers` **exists** (HTTP 200), **protected-branch deployment restriction** is reported, and `main` is protected. Six static and legacy-seed guard tests passed.
- The same audit reports **zero required reviewers**, consistent with solo operation. Its `admin_bypass_disabled_verified` and `prevent_self_review_verified` checks are **false / unverified**, and it does not report the wait timer. These are **NOT proof** that bypass is enabled, nor proof that the intended **10-minute** timer is saved. Obtain owner-visible saved-setting evidence before considering activation.
- No active held-out workflow exists in `.github/workflows`. The historical Experiment 001 manually supplied seed input is now guarded, rejecting **3101–3110 before any demand generation**, but a sufficiently privileged human can still run a standalone generator or change repository settings. Workflow safeguards are not a security boundary against the repository owner.

## Explicit proposed solo alternative to independent review

**A. Separate approvals, not self-review.** The owner must issue **two independent, deliberate instructions at different stages**: (1) permission to integrate and enable the *manual-only* held-out workflow after reviewing its final code and safeguarding evidence; (2) a fresh explicit instruction to generate/run reserved evaluation seeds, after seeing the activation-ready report. Neither approval is inferred from this addendum, a generic "proceed," opening a PR, or the 10-minute timer.

**B. Technical time and branch controls.** Before activation, independently verify that environment `m3-holdout-reviewers` has **Required reviewers OFF**, **Wait timer = 10 minutes**, **administrator bypass OFF**, and **Deployment branches and tags = Protected branches only**. Maintain a protected `main` ruleset requiring PRs and blocking force pushes/deletions. A timer **automatically expires** and provides no independent human authorization.

**C. Disabled until after review.** Keep the review template at [`docs/templates/experiment-002-m3-heldout-evaluation.yml.disabled`](templates/experiment-002-m3-heldout-evaluation.yml.disabled), outside GitHub Actions' executable workflow directory. No push, schedule, PR, workflow_run, API automation, or background process may access held-out seeds. A final production workflow must use `workflow_dispatch` **only**, and be inactive until explicit activation permission. There is presently no production pipeline capable of legitimately running the complete 30-scenario frozen study.

**D. Immutable science and reproducible provenance.** All source operations must pin frozen commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e` and immutable SUMO image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. Verify OD demand equivalence across same-seed regimes, fixed 1-second simulator step, 30-second bins, unchanged original time-aware routing, native edge-entry outcomes, explicit teleport statistics, original frozen R3 eligibility, and frozen R4 seed-level paired error analysis. Preserve full input/output hashes and every attempted seed/exception.

**E. Incident handling and one-time experimental integrity.** Once separately authorized, a run is recorded even if incomplete or unsuccessful. No undocumented seed substitution, selective rerun, reparameterization, or peeking at held-out outcomes. Failed/ineligible scenarios block the planned ten-seed confirmatory summary and require another expressly approved incident procedure. No new success threshold is added after viewing data.

**F. Explicit remaining risk.** The repository owner controls GitHub administration and can change rules, disable timers, or manually run code. Without another reviewer, there is **no independent separation of duties**. This weaker solo-operating procedure should be treated as an *operational risk exception* to the original independent-review safeguard, not a scientific protocol amendment or independent approval.

## Readiness decision gates — all must be evidenced before held-out execution

| Requirement | Status at proposal | Consequence |
|---|---|---|
| R0–R4 scientific measurement and statistical protocol | Frozen and unchanged | Scientific protocol remains M3 v1.0 |
| Exact frozen commit, image and development rehearsal | Previously verified | Ready for future technical review |
| Original R3/R4 production adapters | Synthetic and development-only tests passed | Needs full production runner integration review |
| Active `main` branch ruleset | Verified by live GitHub REST | Passed for current revision |
| Protected environment exists / deployment only from protected branches | Verified by read-only audit | Passed for current environment |
| Saved 10-minute wait and administrator bypass disabled | **Not independently verified** | **Block activation pending owner-visible evidence** |
| Independent human required reviewers | None, as solo researcher | **Needs explicit approval of weaker solo risk exception** |
| Final manual-only held-out execution driver, complete hash/archive mechanics | **Not deployed or reviewed** | Block activation |
| Authorization to enable production workflow | **Not granted** | Workflow remains disabled |
| Authorization to generate/run any reserved seed | **Not granted** | Seeds 3101–3110 remain unopened |

## Decision requested

Review this **proposed** solo-operator safeguard alternative, including the explicit admission that it is **weaker** than independent review. If acceptable, approve **this operational exception only**, without authorizing held-out execution. Separately provide evidence that the timer and bypass settings are saved. Then review the final production workflow integration and activation guard before any separate authorization to run the untouched evaluation seeds.

**Current verdict: SOLO SAFEGUARD PROPOSAL UNDER REVIEW. NO HELD-OUT SIMULATION AUTHORIZED.**
