# Experiment 007 — E1-v2-J1 D1 Final Development Scientific Audit

**Research date:** November 4, 2026 (GitHub execution November 5 UTC).  
**Formal verdict: DEVELOPMENT NOT QUALIFIED.** The complete frozen development cohort was executed successfully, but E1-v2 **failed accuracy, directional-skill, and across-seed improvement gates**. Independent estimator validation **NOT STARTED** and cooperative Test B **NOT RUN**. This finding is not a software failure and does not establish that cooperation cannot work.

**Controlling prespecified protocol:** [E1-v2 D1 frozen development protocol](POST_EXP007_E1_V2_D1_FROZEN_DEVELOPMENT_PROTOCOL_V1_2026-11-04.md).  
**Original unmodified simulation run:** [GitHub Actions 41966516110](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41966516110) at commit `a54b6f650b16a22b0eb5543bb507f9faf5eea034`; original full-development artifact **13387764476**, archived ZIP SHA-256 `c8b7e508ecbffd2c4b5ea7803dc83024780e1beecd42002c080ebf6b4d0c88e5`.

## 1. Executive result

The connection-aware E1-v2-J1 engineering model completed 60 original synthetic SUMO arms (ten independent 1,000-driver demand seeds, each with one independent traffic-aware baseline I, four fixed single-route changes, and a joint bundle). All prospective model predictions for the **ten** development seeds were frozen and hashed before any of the new counterfactual SUMO outcomes were generated. Six seeds **6101–6106** belong to development-build and four seeds **6111–6114** to development-check. There was **no new hyperparameter fitting** in this particular study.

**E1-v2 did not meet the frozen progression rules.** On 16 material singleton cases across four independent development-check demand seeds:

| Prospective estimator | Mean across four seed-level externality MAEs (network-seconds; lower is better) |
|---|---:|
| B0: zero externality | **1,478.0625** |
| B1: original quadratic proxy | **1,478.332478** |
| E1-v1: old all-class queue model | **1,478.3125** |
| **E1-v2-J1: connection-aware junctions** | **1,478.5625** |

The **best comparator is B0**, not the former E1-v1. E1-v2 worsened its mean externality MAE by **0.5 network-seconds**, or **0.033828%** relative to the B0 benchmark; the frozen gate required an **improvement of at least 10%**, meaning an E1-v2 mean no greater than **1,330.25625 network-seconds**. E1-v2's observed MAE was therefore approximately **148.30625 network-seconds above** the threshold.

**Additional independent gate failures:** E1-v2 was better than its best comparator **in just 1 of 4 development-check seeds** (required ≥3/4). Directional sign accuracy was only **5/16 = 31.25%** (required ≥60% over at least ten material cases).

**One favorable diagnostic:** **0** predicted-benefit / observed-large-harm cases using the frozen definition (`predicted externality < 0 and actual externality > 30 network-seconds`), satisfying that *particular* hazard rule. But the lack of predicted negative effects, poor directional accuracy, and very small predicted magnitude mean this cannot establish reliable safety, calibration, or forecasting usefulness.

## 2. Evidence lineage and independent re-audit

The original workflow completed operationally. The earlier failed [first execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41964194079) stopped **before any SUMO arm** because its prediction collector expected a different storage path; this was a [documented pre-outcome repair](POST_EXP007_E1_V2_D1_PREOUTCOME_COLLECTOR_PATH_REPAIR_2026-11-04.md) with scientific inputs and thresholds unchanged. The repaired run **41966516110** is the source of all 60 outcomes and the verdict.

A separate **archive-only numerical audit**, without rerunning SUMO or either E1 model, downloaded the original 695-member 284MiB evidence ZIP and verified:

- Original ZIP SHA-256: `c8b7e508ecbffd2c4b5ea7803dc83024780e1beecd42002c080ebf6b4d0c88e5`.
- **Ten** original seed manifests with exact network and demand SHA-256 matches.
- **Ten** per-seed frozen prediction locks and hashed prediction files; **50** immutable model prediction records for single swaps and bundles.
- All **60** original route manifests matched source hashes; original SUMO tripinfo hashes matched the saved observation summaries.
- Exactly **1,000 unique completed tripinfo driver IDs per arm**, **60,000 original records** overall.
- The independent re-audit calculated MAE from the original saved per-probe effect records, reproduced the four per-seed and across-seed mean MAEs, **5/16** direction matches, **0** severe wrong-sign benefit flags, and the formal **DEVELOPMENT NOT QUALIFIED** verdict.

**Important distinction:** The saved file hashes and code sequence establish internal provenance consistent with prediction-before-outcome; they are not an independent cryptographic record of every real-world wall-clock write event. The original workflow explicitly freezes predictions before invoking SUMO and its log records 60 scenarios only afterward.

The underlying simulation study uses a fixed synthetic grid, complete announced routes, 200-second congested departure demand, 1,000 identities per arm, and 50% nominal eligibility. Neither full advance intent knowledge nor 100% compliance is a real-world consent measurement.

## 3. Full development-check comparison by independent seed

| DEV_CHECK demand seed | B0 MAE | B1 MAE | E1-v1 MAE | E1-v2 MAE |
|---|---:|---:|---:|---:|
| **6111** | 968.000 | 968.810 | **964.750** | 970.750 |
| **6112** | 1,382.250 | **1,381.710** | 1,382.750 | 1,382.250 |
| **6113** | **2,403.500** | 2,404.310 | 2,406.000 | 2,403.750 |
| **6114** | 1,158.500 | 1,158.500 | 1,159.750 | **1,157.500** |
| **Mean** | **1,478.0625** | 1,478.3325 | 1,478.3125 | 1,478.5625 |

*The independent demand seed is the correct replication unit.* The four probes per seed reuse a baseline and are dependent; 16 route swaps are not 16 independently generated demand scenarios. The 16,000 driver observations are not 16,000 independent replicates.

## 4. Why E1-v2 did not qualify

The frozen development gates from the preregistered protocol evaluate together:

| Gate | Observed | Decision |
|---|---|---|
| E1-v2 ≥10% lower mean MAE than best B0/B1/E1-v1 | **−0.033828% improvement** (worse than B0) | **FAIL** |
| E1-v2 strictly better than each frozen comparator | Worse than all three in across-seed mean | **FAIL** |
| Lower error on ≥3/4 independent check seeds versus each seed's best | **1/4** | **FAIL** |
| At least ten materially nonzero singleton effects | **16** | PASS |
| Correct externality sign ≥60% | **5/16 = 31.25%** | **FAIL** |
| Zero predicted-benefit/realized-harm >30 *aggregate* network-seconds | **0** | PASS |
| Prediction and route locks complete | Matched and hashed | PASS |
| All 60 SUMO arms and 60,000 trips complete | Verified | PASS |
| Offline compute ≤120s/pair and ≤2GiB peak RSS | Max pair wall **1.501s**; process peak **91,608 KiB** (~89.46 MiB) | PASS |

The model's **point estimates were also much smaller than realized effects**: E1-v2 predicted externalities between **−4 and +8 network-seconds**, whereas realized development-check effects spanned **−3,960 to +3,215 network-seconds**. This is a clear, direct *magnitude-sensitivity mismatch* in this selected cohort. It does **not** identify which physical or algorithmic feature caused it.

The reconstructed nonparticipant effects, own time, and two-route bundle records are available in the permanent, machine-readable per-probe tables. Their outcomes remain **development-only**, not independent scientific confirmation.

## 5. Interpretation and scientific limitations

The J0–J4 [source verification](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md) established that E1-v1's junction conflict rule excludes many static non-foe movements; E1-v2-J1 addressed this *structural restriction*. This completed development study does **not** demonstrate that the revised junction service improved externality prediction against SUMO. A more faithful static foe/priority representation alone was **insufficient** to pass the complete simulator's network externality forecasting gate.

This result does not isolate an underlying causal bottleneck. Other candidate mechanisms include the one-second arrival/turn service clock, simplified FIFO storage, source insertion, partial internal-junction handling, downstream spillback, or more broadly the inability of a coarse finite-capacity approximation to reproduce the timing of nonlinear traffic interactions. These are **hypotheses**, not proven causes. The new seed cohort and modest sample size provide no real-road generalization.

The original Experiment 007 Test A remains **NO-GO**; historical E1-v1 Stage 1D remains **DEVELOPMENT NOT QUALIFIED**. E1-v2-J1's development failure does not imply that all cooperative traffic coordination is impossible, or that cooperation could not benefit some future network. It means **this estimator has not earned the right to direct a cooperative policy experiment under our prespecified scientific sequence**.

## 6. Formal decision and next scientific stage

**STOP: E1-v2-J1 DEVELOPMENT NOT QUALIFIED.** Preserve these unsuccessful results. Do **not** open the reserved new independent estimator-validation seeds **6201–6212** or future cooperative Test B seeds **6301–6312**, and do not run the cooperative-routing experiment simply because of the broader conditional approval. The frozen policy required advancing only after development qualification followed by successful independent confirmation.

The next appropriate milestone is an **archive-only E1-v2 failure-mechanism investigation and new prospective model hypothesis**, explicitly focused on *why its other-driver forecasts remain so compressed and often wrong-sign despite a corrected static junction conflict map*. Existing 6101–6114 seeds are now inspected/contaminated for later model redesign; they cannot become independent E1-v3 or E1-v2-retuned holdouts. If a future alternative is justified, freeze its new scientific protocol and select **new, disjoint development cohorts and an independent holdout** before observing their outcomes.

**No automatic E1-v2 retuning or fresh follow-on simulations are authorized by a failed development gate.** Future Test B remains separately conditional upon a genuinely validated estimator and must measure actual scheduled-to-arrival network time for *all drivers*, individual harm and **nonparticipant fairness** against an **equally informed independent traffic-aware baseline**.

## 7. Reproducibility and permanent evidence

- [Original frozen V2-D1 scientific design](POST_EXP007_E1_V2_D1_FROZEN_DEVELOPMENT_PROTOCOL_V1_2026-11-04.md).
- [Original completed execution and 60-arm artifact](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41966516110), original 60-arm artifact ID **13387764476**, with 30-day workflow-artifact retention.
- [Local archive-only audit source](../../research/audits/e1_v2_d1_archive_no_go_audit.py) and its compact CSVs, which recompute input, prediction, observation and externality integrity without SUMO execution.
- [Compact independently verified seed MAE table](results/exp007_e1v2_d1_devcheck_seed_mae.csv), [16 check probes](results/exp007_e1v2_d1_devcheck_singletons.csv), [50 arm effect rows](results/exp007_e1v2_d1_all_arm_effects.csv), and [ten source/lock manifests](results/exp007_e1v2_d1_original_manifest.csv).
- **[Permanent original E1-v2 D1 60-arm evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-d1-development-nogo-2026-11-04)**: successfully verified all five uploaded assets, including the repackaged ZIP of the same **695 original extracted file bytes** (299,118,955-byte ZIP), a per-member SHA256 ledger, release-asset checksum, source/decision manifest, and unmodified `development-verdict.json`. The original GitHub Actions ZIP wrapper SHA256 was `c8b7e508ecbffd2c4b5ea7803dc83024780e1beecd42002c080ebf6b4d0c88e5`; the **repackaged** ZIP checksum differs due to ZIP-wrapper metadata and compression, while the ledger verifies each original member. [Read-only post-merge preservation workflow 41969929377](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41969929377) succeeded. **No SUMO was rerun** for preservation.

**Final immutable statement:** **E1-v2 D1 DEVELOPMENT NOT QUALIFIED**. Stage 2 validation **NOT STARTED**. Cooperative Test B **NOT RUN**. No social publication requested.
