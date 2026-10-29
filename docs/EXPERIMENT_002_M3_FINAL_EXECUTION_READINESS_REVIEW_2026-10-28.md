# Experiment 002 — M3 Final Execution-Readiness Review

**Review date:** 2026-10-28 (Pacific). **Decision: NOT READY TO EXECUTE; SCIENTIFIC PROTOCOL FROZEN; NO HELD-OUT EXECUTION AUTHORIZED.**

## Scope and sources

This review uses the frozen [M3 scientific protocol v1.0](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md), approved at Git commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`; the [production adapter review](EXPERIMENT_002_M3_PRODUCTION_ADAPTER_REVIEW_FINDINGS_2026-10-27.md); the [solo operational amendment](EXPERIMENT_002_M3_SOLO_OPERATIONAL_SAFEGUARDS_AMENDMENT_V0_1.md); and read-only GitHub repository/Actions checks. No new simulation, demand generation, or held-out seed inspection was performed.

## Confirmed gates

| Gate | Finding | Decision |
|---|---|---|
| Frozen scientific reference | Frozen commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e` remains the designated source; no amendment to estimand, R3/R4 or seed registry | PASS as protocol baseline |
| Main branch | GitHub API reports `protected: true`; current main SHA `f0a7d9d4525cf1e3b1ac6ced24bb04e558062a43` | PASS |
| Ruleset | Active `Protect main - M3 Research`, default branch targeted, PR required, required approving reviews **0**, force-push/deletion blocked, no bypass actors | PASS for documented solo branch policy |
| Solo amendment | PR #2 merged at `f0a7d9d4525cf1e3b1ac6ced24bb04e558062a43` | PASS as adopted operational text |
| Non-executing test suite | [Run 40756119010](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40756119010) succeeded; nine synthetic tests from PR #2 | PASS, but tests are not proof of live environment settings |
| Previous production adapter qualification | Synthetic R4 fixtures and archived seed-2101 R3 equivalence passed | PASS for development equivalence only |
| Active workflow inventory | No `m3-heldout` or held-out evaluation workflow in `.github/workflows`; disabled template remains under `docs/templates` | PASS for nonactivation |
| Reserved seed status | No authorized held-out run or evidence of seed 3101–3110 simulation in reviewed Actions | NOT STARTED |

## Open blockers — cannot certify execution readiness

1. **Live GitHub environment protection is not independently machine-verified.** The user supplied screenshots showing Required reviewers off, 10-minute wait timer, administrator bypass unchecked, and protected branches only, and confirmed they saved settings. These are useful user-provided configuration evidence, but the available GitHub connector rejects the environment administration GET endpoint. The automated solo checker has **not** been rerun against an authenticated live environment object. Treat wait timer and bypass as **SCREENSHOT-SUPPORTED, NOT API-VERIFIED**, rather than claiming a security guarantee.
2. **No executable held-out production workflow has been deployed or reviewed.** The template `docs/templates/experiment-002-m3-heldout-evaluation.yml.disabled` contains three `if: false` jobs and intentionally fails. It does not yet implement general-seed R3/R4 execution, per-scenario source manifest generation, 30-scenario integrity checks, protected-environment activation, and release-record validation. A working execution runner must be separately implemented, tested using fabricated/development inputs, and reviewed **before** any authorization to run reserved seeds.
3. **No independently enforced second approval in solo mode.** A 10-minute timer expires automatically. Solo operation replaces independent review with explicit user authorization and recorded release provenance; this is a weaker operational control and cannot prevent an administrator from changing settings or running code outside audited workflows.
4. **No held-out execution release record exists.** Approval to perform this readiness review, or to merge the solo amendment, does not authorize running any reserved seed. Do not create or infer such a record without an explicit subsequent instruction.

## Recommendation and next actions

**No-go for execution today.** Continue with a separate *implementation-only* milestone: build a manual-only production runner and guarded release-record verification, exercise all paths using synthetic and previously inspected development data, verify source hashes, eligibility, no-seed-substitution behavior and 10-seed aggregation. Keep all jobs that could use 3101–3110 disabled until the user explicitly approves the actual held-out evaluation in a later decision.

For environment protection, retain the saved GitHub screenshots as evidence and independently verify administrative settings through an appropriately authorized GitHub UI/account or API when available; never mark unavailable fields as true.

**Scientific boundaries:** chosen-route entry-time prediction accuracy is not evidence of better network-wide cooperative routing, physical occupancy calibration, causal intersection delay, or real-world safety. The original scientific freeze remains unchanged.

**Final status: READINESS REVIEW COMPLETE — EXECUTION NOT READY AND NOT AUTHORIZED.**
