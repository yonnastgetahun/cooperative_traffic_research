# Experiment 002 — M3 Solo-Researcher Operational Safeguards Amendment v0.1

**Date:** October 28, 2026. **Status: PROPOSED; NOT YET ADOPTED. NO HELD-OUT EXECUTION AUTHORIZED.**

## Scope

This proposed amendment addresses **GitHub operational release controls only**, replacing the earlier independent-review requirement for a one-person repository. It does not modify the [frozen scientific protocol](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md), authoritative SHA `be2e8d27c78c8b6de4891115d6d951edc877ac6e`, predictor, R3/R4 rules, seed registry, confidence intervals, or evaluation objectives.

## Solo-controlled release requirements

1. **Protected main:** verify GitHub reports `main.protected=true`; an active ruleset applies to `main`, blocks force-push/deletion, and requires a pull request. Zero required approvals is acceptable for solo operation, but is **not** independent review. Never bypass a blocked merge silently.
2. **Environment:** `m3-holdout-reviewers` must exist with deployment restricted to protected branches and a **10-minute wait timer**. Required reviewers may be absent under this proposed solo exception. Explicitly verify admin bypass is disabled; absent or contradictory API fields remain **UNVERIFIED**, not PASS.
3. **Separate authorization:** The user must explicitly authorize running the reserved 3101–3110 evaluation seeds **after** reviewing the final executable workflow. A 10-minute wait automatically expires and is **not** a second authorization.
4. **No automatic execution:** The future held-out workflow must be manual-only, pin the frozen SHA and immutable SUMO image, require a separately approved release record, validate inputs and full R3/R4 evidence, and retain exception ledgers. An `approved=true` workflow input is insufficient.
5. **Fail closed:** Any missing protection evidence, source drift, unrecognized workflow, or unclassified exception blocks readiness. No seed substitution or silent missing-data imputation.
6. **Risk acknowledgment:** The solo administrator can modify GitHub settings or run code outside the guarded workflows. These measures reduce accidental execution, **not** provide independent security review. If another trusted reviewer becomes available, revisit this exception.

## Evidence and open checks

The [October 28 audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40755533101) verified that `main` is protected, the environment exists, and protected-branch deployment restrictions are present. It did **not** verify the 10-minute timer or disabled administrator bypass. Those remain blockers. The previous auditor's independent-review requirement remains in effect until this amendment is separately approved.

## Decision

**PROPOSED FOR REVIEW.** Approving this document would authorize adopting a weaker solo operational approval model, **not** executing any held-out experiment. This change is not a scientific-protocol amendment. No reserved seeds are generated, simulated, or read during its verification.
