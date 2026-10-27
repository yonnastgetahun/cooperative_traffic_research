# Experiment 002 — M3 Operational Safeguards: Readiness Decision

**Date:** October 27, 2026 (America/Los_Angeles).  
**Verdict:** **NOT READY TO ACTIVATE HELD-OUT EXECUTION.** This is an operational review, not new predictor evidence or authorization to run evaluation seeds.  
**Frozen scientific source:** `be2e8d27c78c8b6de4891115d6d951edc877ac6e` — [frozen M3 protocol](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md).  
**Read-only review:** [GitHub Actions run 40581795907](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40581795907) (**successful**) · [permanent machine-readable audit and SHA fingerprints](results/exp002_m3_operational_review_2026_10_27/README.md) · [successful archive publication run 40582095688](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40582095688).

## Findings — distinguish verified safeguards from unconfigured permissions

| Area | Measured state | Gate |
|---|---|---|
| Frozen M3 scientific protocol and pinned code | Already approved, immutable SHA recorded | **PASS** |
| Previous R3/R4 production adapter review | Passed eight adversarial tests and reproduced original frozen R3 on inspected development scenarios | **PASS** |
| Existing active held-out workflow | **None found** in `.github/workflows` | **PASS for present repository content** |
| Disabled future workflow template | Located in `docs/templates` outside active Actions; all three jobs `if: false` | **PASS as disabled** |
| Legacy Experiment 001 arbitrary-seed workflow | **Hardened** to reject seeds 3101–3110 before any `netgenerate`/OD generation, with safe shell quoting | **PASS:** executable unit tests denied every reserved seed |
| Static audit of existing active workflow seed input paths | One user-controlled seed input found; the legacy calibration path is now guarded | **PASS in present scanned repository** |
| GitHub environment `m3-holdout-reviewers` | Read-only REST `GET` returned **HTTP 404**; no protection rules or reviewers could be verified | **BLOCKED — UNKNOWN / UNVERIFIED** |
| `main` branch protection | GitHub REST `GET branches/main` returned **`protected: false`** | **BLOCKED — NOT PROTECTED** |
| Independent approvals / self-review prevention / admin bypass restrictions | Cannot verify until a protected environment is configured and readable | **BLOCKED** |
| Held-out evaluation seed generation or simulations | **None** | **NOT AUTHORIZED** |

Six no-SUMO fixture tests passed in the [read-only audit run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40581795907). They verified the *actual* legacy calibration seed guard, strong/weak/missing environment protection interpretations, explicit main-branch protection status, and inactive held-out workflow. This is a **static source and read-only GitHub API** audit; it is not a cryptographic restriction on a repository administrator manually running arbitrary scripts outside the monitored workflows.

**Special caution:** GitHub can **automatically create an unprotected environment** when a workflow references a name that does not already exist. Never move the inactive template into `.github/workflows` or add a job referencing `m3-holdout-reviewers` before configuration is independently verified. See [GitHub's official environment documentation](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).

## Required manual GitHub administration — no environment mutations were performed by this review

The repository is **public**, so standard GitHub environment required-reviewer rules are supported under current public-repository plans. GitHub's integration available to this research session does **not** provide the administration write/read endpoints required to configure and reliably verify those settings directly.

### A. Protect the main branch

In [repository Settings](https://github.com/yonnastgetahun/cooperative_traffic_research/settings), configure a branch protection rule or ruleset targeting `main`. Require a pull request and independent approving review for workflow/code changes, prevent direct force pushes and deletions, and disable bypass permissions where available. **Do not assume the frozen snapshot branch is immutable because of its name**: the authoritative freeze is the SHA `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.

The present `main` branch is explicitly **not protected**. Even excellent workflow guards can be edited by a writer when the branch is unprotected. Documentation: [GitHub branch-protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### B. Create the reviewed execution environment manually

In **Settings → Environments → New environment**, create `m3-holdout-reviewers`. Configure and save:
- **Required reviewers:** at least one other authorized person with repository read access. A sole triggering account does **not** provide an independent approval.
- **Prevent self-review:** **enabled**.
- **Disallow administrator bypass:** **enabled**, by deselecting "Allow administrators to bypass configured protection rules".
- **Deployment branches:** restricted to protected branches (after protecting `main`) or an explicitly reviewed equivalent branch policy. Confirm at least one intended release branch satisfies the rule.
- Optional: a short wait timer to reduce accidental activation; a wait timer **does not replace** required reviewers.

Source: [GitHub Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) and [Deployment protection rules](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

**The human GitHub UI configuration is an uncompleted prerequisite, not something this report claims to have performed.** If no independent reviewer is available, do not activate the held-out workflow. A one-person self-approval or merely typed "approved" workflow input does not meet this protocol's operational independence requirement.

### C. Reverify and authorize in distinct steps

Once (A) and (B) are configured, rerun the **read-only** [M3 operational safeguard audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/workflows/experiment-002-m3-operational-safeguards-audit.yml) manually and verify its environment protection fields, main-branch protection status, source SHA and workflow inventory. If GitHub token permissions yield incomplete REST fields, obtain an independent owner-visible configuration review; do not upgrade `NOT_VERIFIED` to `PASS` by assumption.

Only after all safeguards pass should a **separate** reviewer-approved production workflow be considered. That workflow must use `workflow_dispatch` only, a truly configured protected environment, the frozen scientific code SHA, strict per-scenario source manifests, the locked seed registry, and the frozen R3/R4 analysis. Production code may **not** change scientific estimands. **Even then, executing evaluation seeds 3101–3110 requires another explicit user instruction**, separately from enabling or reviewing a workflow.

## Scientific boundary preserved

The previous development trials remain unchanged. Lower time-aware entry-error MAE than free flow along driven routes does **not** establish predictor calibration, a network-wide cooperative-routing benefit, causal junction delay, real-world traffic generalization or safety.

**Current action decision:** Continue hardening and verifying GitHub settings; **do not** activate an M3 held-out evaluation workflow or generate reserved seeds until the two GitHub administration blockers are resolved and a distinct execution approval is given.
