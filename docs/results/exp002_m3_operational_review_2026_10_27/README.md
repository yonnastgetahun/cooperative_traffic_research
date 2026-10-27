# M3 Operational Safeguards — Read-Only GitHub Security Audit

**Review completed. Execution BLOCKED. No reserved seeds generated, inspected or simulated.**

- [Machine-readable environment, branch, seed-path and activation audit](operational-safeguards.json)
- [SHA-256 source guard fingerprints](source-hashes.txt)
- [Successful read-only Actions run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40581795907)
- [Operational scientific decision report](../../EXPERIMENT_002_M3_OPERATIONAL_READINESS_REVIEW_2026-10-27.md)

A legacy calibration workflow formerly allowed an arbitrary manually supplied seed. It now blocks the M3 reserved seed range **3101–3110 before any network or OD generation** and quotes user-supplied values. Six non-simulation adversarial checks passed.

GitHub API returned HTTP 404 for environment \`m3-holdout-reviewers\`: required reviewers, self-review prevention and admin-bypass restrictions are **not verified**, and no environment has been created or modified by this audit. The main branch was explicitly reported as **not protected**. These remain separate human GitHub administration actions before any held-out execution can be considered.

No evaluation workflow has been deployed or activated. The frozen scientific commit is \`be2e8d27c78c8b6de4891115d6d951edc877ac6e\`.
