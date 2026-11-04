# E1 Stage 1D — Final Development Scientific Report and Independent Archive Audit

**Research date:** November 3, 2026.  
**Decision: DEVELOPMENT NOT QUALIFIED.** Operational simulation and archive checks succeeded; the prospectively frozen **predictive accuracy** and **false-benefit** gates failed. No independent validation or Test B was executed.  
**Audit type:** Read-only re-analysis of already completed Stage 1D SUMO, model predictions and manifests. **No new simulations, recalibration, probe reselection or model changes.**  
**Source:** [Stage 1B frozen protocol](POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md), [Stage 1D source/physics review](POST_EXP007_E1_STAGE1D_SOURCE_AND_PHYSICS_REVIEW_2026-11-03.md), [original successful GitHub Actions workflow run 41737336992](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992), code snapshot commit \`05b770cf000f84677524e0a1e89bea06ec0e703b\` and original raw evidence [artifact 13280496865](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992/artifacts/13280496865).

## 1. Executive result

E1 is a forward, link/turn queue-aware counterfactual model designed to predict both a selected driver's own journey-time change and the time changes for the **999 other drivers**. The prior assigned-demand model failed original Experiment 007 Test A, and six exploratory replays clarified structural and time-dependent limitations. The new Stage 1D study addressed only **development qualification**, not independent scientific validation or whole-policy cooperative efficacy.

A frozen 10-seed, 60-SUMO-arm development experiment executed successfully. E1's one globally tuned saturation-flow parameter was selected using **DEV_BUILD 5101–5106** only. An independently recalculated audit of the four **DEV_CHECK 5111–5114** seeds found:

| Development-check metric | B0: zero externality | B1: frozen historical proxy | E1 queue model |
|---|---:|---:|---:|
| **Mean seed-level externality MAE**, network-seconds | **1,555.875** | **1,555.267549** | **1,555.125** |
| Nonzero directional predictions matching realized sign (16 material probe effects) | 0 nonzero predictions; sign undefined | **11/16** | **6/16** |
| Exact zero externality predictions | **16** | **0** | **4** |

The MAE values are arithmetic means of **four independent demand-seed MAEs**, each computed from four fixed single-route probes. The 16 probes share within-seed baselines and are **not** 16 independent replications. All 16 realized externalities had absolute magnitude ≥10 network-seconds (the historic diagnostic materiality floor). E1 sign agreement was **6/16 = 37.5%** when its four predicted zeros are counted as nonmatches; among its 12 nonzero predictions, agreement was **6/12 = 50%**. This is descriptive, **not** a newly authorized sign gate and not directly comparable to the old 20-probe Experiment 007 Test A sample.

**Primary gate failure:** The frozen development requirement was E1 externality MAE at least **5% lower** than the better of B0 and B1, while strictly beating both. Here B1 was best at 1,555.267549 and E1 was 1,555.125: an improvement of **0.142549 network-seconds**, or **0.00917%**, well below 5%. The minimum passing E1 MAE would have been **1,477.504171** network-seconds; the observed E1 MAE missed that threshold by **77.620829** network-seconds. An operationally successful workflow is not a scientific GO.

**Separate adverse-outcome gate failure:** E1 predicted a **negative externality (benefit for others)** in two cases that actually yielded very large **positive externalities (harm to others)**. Both exceeded the development script's >30 **network-seconds** adverse sign threshold. These are aggregate effects, **not a claim that each individual lost 30 seconds**.

**Principal measurement pattern:** E1 predicted singleton externalities between **−6 and +21 network-seconds**, compared with realized externalities between **−2,267 and +3,945 network-seconds**. Mean absolute predicted externality magnitude was **3.625 network-seconds**, versus a **1,555.875 network-second** mean absolute realized effect. This strong *magnitude compression* is a descriptive feature of this cohort, not a uniquely identified physical cause of the failure.

## 2. Audit integrity, scope and what was independently reconstructed

We downloaded the original \`exp007-e1-stage1d-original-development-cohort\` ZIP from run 41737336992 and **read the original archived tripinfo XML files**, rather than merely repeating the workflow's \`development-verdict.json\`. The audit verified:

- **706 ZIP members**, SHA-256 of the downloaded archive **\`f8d2b76bd6eda63e11889bd7708888bfdb55af78edd0b30526a9d981feb72fa6\`**. Original ZIP size approximately 297 MB. Original GitHub Actions retention expiry **December 3, 2026 UTC**.
- **Ten** fixed seeds; exactly **six arms per seed**, comprising independent I, four distinct eligible single-driver route changes, and one two-driver bundle: **60/60 completed simulations**, **60,000 matched observed trip records**, all scheduled-to-arrival values independently reconstructed from \`tripinfo.arrival − scheduled trip depart\`.
- All **60 raw tripinfo SHA-256 hashes** matched the archived observation manifests; all 60 observed driver-ID sets had **exactly 1,000** identities; their aggregate scheduled-to-arrival totals matched the archived labels.
- Each scenario's network/trips/route SHA-256 matched its frozen scenario manifest; each singleton changed **exactly the one declared target planned route**, bundle changed **exactly two designated routes**, and all other initial assignments stayed fixed.
- **Ten prediction locks**, all **22 parameter-specific model prediction files** and **110 per-arm prospective prediction rows** matched their saved records; for every model row the predicted self, external, nonparticipant and total effects reconciled from the **full 1,000 predicted individual elapsed times**.
- The source-reviewed Stage 1D driver produces and locks DEV_BUILD predictions **before build SUMO outcomes**, selects q using build outcomes only, then produces and locks DEV_CHECK predictions before generating check SUMO outcomes. The archive's prediction-lock hashes and manifest confirm internal consistency; **archive files and lock hashes alone are not cryptographic proof of wall-clock precedence**, so this is a procedural/provenance finding.
- Recomputed selected q, all reported seed-level E1/B0/B1 MAEs, aggregate accuracy, both false-benefit cases and resource metrics **match the original frozen-script verdict**. The audit used no SUMO and did not recompute any predictions or alter any route.

**Validity boundary:** This review checks stored data and the original workflow source; it is **not** an external replication of E1 on a new simulator or independent holdout. The frozen Experiment 007 Test A remains NO-GO; policy Test B remains NOT RUN.

## 3. Build-only calibration and lock

The only tuned E1 model parameter was a global nominal link/turn saturation rate (\`q_sat\`) from the **frozen set {0.35, 0.50, 0.65 vehicles/second/lane}**. It was chosen based on DEV_BUILD 5101–5106 (four singleton probes nested within each seed).

| \`q_sat\` candidate | Mean of six build seed-level E1 externality MAEs (network-seconds) |
|---|---:|
| 0.35 | **1,584.041667** |
| 0.50 | **1,575.208333** |
| 0.65 | **1,575.208333** |

The 0.50/0.65 tie was resolved by the **prespecified 0.50 preference**. The saved lock confirms **no DEV_CHECK outcome used in q selection**. DEV_CHECK only evaluated the selected 0.50 model and did not perform a post-hoc alternative search. The tie and similarly poor build magnitude accuracy indicate limited observed development discriminability of these two priors; they do **not**, without further controlled tests, establish why E1 underpredicted.

## 4. Detailed results on the four development-check seeds

**Externality MAE in network-seconds (smaller is better):**

| Fresh development-check seed | B0 | B1 | E1 |
|---|---:|---:|---:|
| **5111** | 1,350.000 | 1,350.405 | **1,345.000** |
| **5112** | 1,409.500 | **1,405.855** | 1,408.750 |
| **5113** | **1,036.750** | 1,039.315 | 1,039.750 |
| **5114** | 2,427.250 | **2,425.495** | 2,427.000 |
| **Mean across four independent seeds** | **1,555.875** | **1,555.268** | **1,555.125** |

E1 had the lowest MAE only on seed 5111. It was worse than the best per-seed comparator on seeds 5112, 5113, and 5114. No standard-error claim is inferred from the 16 dependent probes. The development-check seed count is four; this is a **development screen**, not independent confirmation.

**Critical predicted-benefit / realized-harm cases:**

| Seed / single probe | Predicted externality | Realized externality | Interpretation |
|---|---:|---:|---|
| **5111 / probe2** | **−4 network-s** | **+2,567 network-s** | Predicted small benefit to others; observed large harm |
| **5114 / probe2** | **−6 network-s** | **+3,945 network-s** | Predicted small benefit to others; observed large harm |

The original script counted both as \`severe_false_benefit_gt30_network_s\` and required **zero** such adverse cases for qualification. The name's 30-second threshold applies to the **aggregate effect across other drivers**, not to a single driver's harm. There is no implication that changing one planned route made every other driver slower; each externality is the **net sum** of many positive and negative individual differences.

**Additional descriptive diagnostics:**
- E1 signed mean prediction error (predicted externality minus realized externality) across 16 probes: **−820.75 network-seconds**, indicating a cohort-average **downward signed bias**; error magnitude remains large even where signs agree.
- E1 own-driver effect MAE: **42.25 seconds per rerouted driver** (different unit and estimand from externality MAE).
- E1 nonparticipant aggregate-effect MAE: **995.3125 network-seconds** (computed over the 500 nonparticipants in each probe; these are not 500 independent replications).
- Among the 16 singleton perturbations, realized fractions of **individual drivers delayed >30 seconds** ranged from **4.6% to 19.5%**, while the **nonparticipant** fractions ranged **4.2% to 19.8%**. These are per-probe *diagnostic harm exposures*, not an efficacy/fairness outcome from the unexecuted Test B policy. Eight of sixteen probes had a nonparticipant >30s harm fraction above 10%; the historic prospective Test B fairness gate must **not** be silently applied to unrelated Stage 1D single-probe scenarios.

Detailed original-value rows and independent calculation are preserved in the accompanying [per-probe source table](results/exp007_e1_stage1d_devcheck_probes.csv) and [seed MAE table](results/exp007_e1_stage1d_devcheck_seed_mae.csv).

## 5. Interaction evidence and a limitation of the forecast

For each development-check seed, the original frozen bundle used **two distinct already-selected individual route swaps**, with no other planned routes altered. The actual interaction is:

\[
J_{\mathrm{actual}}
=[C(A_{bundle})-C(A_I)]
-[C(A_a)-C(A_I)]-[C(A_b)-C(A_I)] .
\]

The same quantity can be computed from E1's four **joint forward-predicted network** outcomes.

| Seed | Realized joint-minus-single network time interaction | E1 predicted interaction |
|---|---:|---:|
| 5111 | **−3,424 network-s** | 0 |
| 5112 | **−2,839 network-s** | 0 |
| 5113 | **−383 network-s** | −7 |
| 5114 | **−799 network-s** | 0 |

All four bundles had **zero declared predicted edge-time overlap score** and used the frozen low-overlap fallback. Their observed nonadditivity therefore matters, but **this sample is not a prospectively designed high-overlap interaction test**. It does not uniquely identify a junction mediator or establish that every route pair interacts similarly. The E1 model *can* produce nonadditive interactions in deterministic unit fixtures, yet did not meaningfully reproduce these four empirical interaction magnitudes.

## 6. Exact reason for the development NO-GO — what passed and failed

| Frozen gate / scientific concern | Verified outcome | Decision |
|---|---|---|
| 60-arm designed dev study and all 1,000 trips per arm | 60/60 archived and independently matched; per-driver route-change/hash checks passed | **PASS** |
| Prediction-first workflow, build/check partition isolation, q selection | 10 valid prediction locks; q=0.50 selected only from build; check has only frozen q | **Procedural PASS**, noting limits of archive timestamp proof |
| Main E1 MAE at least 5% better than better B0/B1 | **0.00917%** better than best B1 | **FAIL** |
| E1 strictly better than both B0 and B1 in mean MAE | 1,555.125 vs 1,555.875 and 1,555.268 | **PASS**, but trivial gain |
| Severe false-benefit requirement | **2**, whereas zero was required | **FAIL** |
| Offline resource screen | Max sampled pair prediction wall time **2.353s**; archived maximum process peak RSS **76,192 KiB ≈74.4 MiB**, below 120s and 2 GiB ceilings | **PASS** |
| Readiness to claim calibrated risk or realistic junction physics | Explicitly **UNCALIBRATED / LOW FIDELITY**; no independent calibration of uncertainty | **NOT ESTABLISHED** |
| Independent estimator validation | No unseen Stage 2 cohort executed | **NOT RUN** |
| Cooperative versus independent Test B and realized whole-policy fairness | No route policy comparison run | **NOT RUN** |

**Formal disposition is DEVELOPMENT NOT QUALIFIED.** This status is a scientific stop rule, not a software failure. All existing records and thresholds are preserved as originally frozen.

## 7. Mechanism interpretation: direct observations vs hypotheses

**Directly established:**
1. E1 has a mathematically separate externality computation and passed its basic no-SUMO physical fixtures, yet its observed externality prediction magnitudes on 16 DEV_CHECK probes were **orders of magnitude smaller** than realized aggregate effects.
2. The E1 saturation parameter changes made modest differences to build MAE and 0.50 and 0.65 tied; this one-dimensional adjustment did not produce a credible externality signal.
3. E1 missed substantial multi-route interactions even though it permits them in carefully constructed toy fixtures.
4. There were two dangerous *sign errors for network-benefit decisions* on the development-check probes. The model's risk/uncertainty estimates remained uncalibrated.

**Plausible—but NOT causally established—contributors:**
- The E1 implementation's conservatively aggregated **all-conflicting-turns** junction rule does not reproduce SUMO's full lane-/turn-specific priority and conflict physics. In the original 10×10 grid, junctions are priority controlled, not traffic light controlled. This rule could produce unrealistic queue placement/discharge, but changing it after seeing these results would be a **new model version** requiring a prospective amendment and fresh development evaluation.
- One-second link-wide FIFO aggregation does not resolve lane changing, within-edge shockwave propagation or all detailed car-following heterogeneity. Forecasting edge entry and intersection capacity more carefully might be necessary; that is a scientific hypothesis, not a proven fix.
- The deliberately small, frozen four-probe-per-seed design and route-candidate constraints limit generalizability. Some planned routes include legal immediate reversals/repeated graph nodes because of the original frozen route construction; further route realism would require a separately justified prospective design and should not be used to retroactively exclude unfavorable probes.
- The original P0–P3 and six-run traces were previously inspected, so they cannot become fresh independent validation for revised E1.

**What this does not establish:** It does not demonstrate that all queue-based models fail, that coordinated traffic routing is inherently ineffective, that a specific synthetic junction is the causal bottleneck, or that an improved predictor would guarantee fair whole-policy outcomes.

## 8. Research preservation, limitations and next decision

**Archive-only evidence:** [Original workflow run 41737336992](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992), [original raw archive artifact](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992/artifacts/13280496865), original development source at [commit 05b770c](https://github.com/yonnastgetahun/cooperative_traffic_research/commit/05b770cf000f84677524e0a1e89bea06ec0e703b), [frozen protocol](POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md), [pre-execution review](POST_EXP007_E1_STAGE1D_SOURCE_AND_PHYSICS_REVIEW_2026-11-03.md). **The large original Actions artifact has a finite expiry of December 3, 2026 UTC.** The compact permanent tables and exact artifact SHA-256 in this report preserve a readable scientific record but are not a substitute for all raw trajectories; a durable raw archive release is advisable.

**Reproducibility:** Independently calculated from ten scenario/route manifests, ten prediction locks, 22 frozen parameter-specific prediction files, all 60 archived \`tripinfo.xml\` files and their observation SHA-256. Per-probe and per-seed CSVs reproduce the frozen verdict. No new random seeds or models were evaluated.

**Scientific decision:** **STOP before Stage 2 independent validation and before Test B.** Complete the archival record and choose a **new prospective hypothesis** for the next estimator version. A later proposal may test junction conflict fidelity and physically observed queue timing, including meaningful interactions and false-benefit risk, but cannot quietly change the frozen E1 parameters, swap choices, or development-check gates after these outcomes. Any E1-v2 development protocol must reserve fresh development-check seeds and keep later independent confirmation separate.

**Scientific stage sequence preserved:** Stage 1D completed with **DEVELOPMENT NOT QUALIFIED** → possible separately frozen estimator redesign/development → only if it succeeds, a fresh independently frozen externality validation → only if that succeeds, the separate matched-seed cooperative-versus-independent Test B with participant and nonparticipant fairness.

**Public dissemination:** Scientific GitHub publication only. LinkedIn/X posts are **not** authorized by this audit task and have not been initiated.
