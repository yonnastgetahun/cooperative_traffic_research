# Direction B — B-H1: single-template development 9101, final scientific findings

**Date:** November 14, 2026 Pacific (GitHub execution November 15 UTC).  
**Status:** **DEVELOPMENT-ONLY NEGATIVE POLICY FINDING; NO CONFIRMATORY COOPERATION EFFICACY CLAIM**.  
**Decision:** **STOP / DO NOT ADVANCE the current shared-forecast, limited voluntary timing policy into confirmatory testing.** Its single fixed development comparison produced **higher**, not lower, all-driver cost. The broader voluntary-cooperation hypothesis is **not refuted**. Physical spillback is plausible in the constructed model but the causal pathway is not uniquely qualified.

## 1. Protocol, run and frozen provenance

The investigator approved moving B-H1 from [integrated prospective plan v0.1](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md) through [PR #122 source/static qualification](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/122) to **one** [precommitted development-only physical protocol](DIRECTION_B_BH1_FROZEN_DEVELOPMENT_ONLY_PHYSICAL_VALIDATION_2026-11-14.md).

- [Development implementation PR #123](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/123); frozen execution head **bca819f31c847122345b0a01b5734897bd013376**, independently pinned original **SUMO 1.28.0** image digest **b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb**.
- [Original successful GitHub Actions run 43666351039](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/43666351039): the 4-gate source/static preflight passed before the physical job, and **all four physical executions completed once**. This was a **single development-only seed 9101**, fixed original 96 driver IDs, 1-second steps, no hidden confirmatory cohort, no altered geometry after outcome inspection, and no parameter sweep.
- [Original 45-member, full physical evidence ZIP (artifact 14141239895)](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/43666351039/artifacts/14141239895): original S/N compiled networks; four route files, per-ID input manifests, physical TripInfo, per-step FCD, queue E2 outputs, SUMO logs, attempt manifest and evaluation JSON. Downloaded ZIP **SHA-256 dd52dee16e7108ad95710a065b88cfbeefc7f6569b0611fb9c42eda104d5739a**, matching GitHub's published Actions digest.
- [Permanent compact original-run summary JSON](results/BH1_DEVELOPMENT_9101_EVIDENCE_SUMMARY_2026-11-14.json) retains the primary results, subgroup effects, physical diagnostics, changed IDs and provenance after the GitHub Actions ZIP's 30-day retention. This compact JSON is **not a byte-for-byte replacement of the full FCD/tripinfo archive**.

The only requested voluntary timing change in the spillback-capable S arm was **m031 +10 seconds**, chosen by the frozen *shared forecast* with predicted **+3 seconds of personal cost**. The N control made **no proposed voluntary shifts**. Six originally eligible IDs were designated willing-to-consider offers by a hash rule; **this is a behavioral assumption, not evidence of actual driver enrollment or consent**.

### Full-journey accounting

The original preferred departure p_i is unchanged in all four cells, and cost sums include all original drivers: **Σ_i(actual arrival_i − preferred departure_i)**. Each arm's **96/96 intended drivers completed**, with actual road insertion and arrival source-audited from TripInfo; no censoring or missing IDs were observed. This is not the same as summing only road travel durations or stopped time.

## 2. Primary development comparison — unfavorable

| Fixed physical setting | Independently informed I | Voluntary-style V | V − I network-seconds |
|---|---:|---:|---:|
| **S: junction blocking allowed** | **8,838** | **8,876** | **+38 (worse under V)** |
| **N: J keep-clear enabled** | **6,088** | **6,088** | **0** |

The diagnostic difference in differences is **Ψ = +38 network-seconds**. The observed +38 is a loss of about **0.396 seconds per intended driver**, not a statistically significant population effect. **There is no independent statistical sample** here: one development template was evaluated under four matched conditions.

**Prespecified direction of hypothesis:** negative V−I would favor cooperation. The primary observed V−I is **positive**. Therefore the frozen candidate **does not show incremental voluntary network benefits** in this development case.

**Important negative-control limitation:** V made no adjustment in N, so the N V/I outputs are identically zero by design. Accordingly, Ψ=Δ_S is not a controlled mediation experiment holding the *same* scheduling intervention fixed across physical settings; the contrast cannot uniquely identify spillback as the cause of the observed +38.

### The forecast failed to anticipate the realized treatment effect

Under the previously fixed paper forecast, S–I's predicted total was **6,062.172662 seconds** and S–V's predicted total was **5,962.158273 seconds**, an **anticipated ~100.014-second improvement**. Physical SUMO outcomes instead showed **+38 network-seconds of harm**.

For driver **m031**, the accepted ten-second later departure was forecast to add only **+3 seconds** to personal cost, but the realized increase was **+33 seconds** compared with the same driver's S–I baseline. This demonstrates a **development-only counterfactual ranking failure** of this particular shared forecast and voluntary offer in this fixed network. It is not an estimate of general model accuracy across future scenarios.

## 3. Subgroups, fairness and completeness

| Matched S-arm driver group | Count | Total V−I seconds | Further information |
|---|---:|---:|---|
| Main-movement drivers | 48 | **+48** | Delays increased |
| Cross-traffic drivers | 48 | **−10** | Some aggregate benefit; not universal |
| Twelve timing-eligible drivers | 12 | **+40** | Includes m031 |
| Six assumed willing-to-consider offers | 6 | **+38** | One actual schedule shift |
| Six modeled decliners | 6 | **+2** | All requested times unchanged |
| Eighty-four ineligible drivers | 84 | **−2** | All requested times unchanged |
| All 90 nonparticipants (ineligible + decliners) | 90 | **0** | **Eight nevertheless harmed**, maximum individual +2s |

Across all **96 drivers**, **12 experienced additional journey cost, one benefited, and 83 were unchanged**. The 13 nonzero matched driver differences are preserved in the compact [evidence JSON](results/BH1_DEVELOPMENT_9101_EVIDENCE_SUMMARY_2026-11-14.json); the single largest harm was the participating m031 **+33s**. One cross driver x011 benefited **−12s**.

**Fairness caveat:** The predicted +5s personal-concession allowance was *not a bound on realized harm*. The +33s realized harm to the sole shifted driver must not be portrayed as genuinely accepted. Aggregate zero nonparticipant change also masks eight individually harmed nonparticipants. Previous study-specific harm thresholds have not been independently validated as human preferences.

## 4. What the physical model actually showed — and did not show

The fixed S/N source networks were independently verified to be **identical except for the single keep-clear flag** at J. SUMO v1_28_0 normally tries to avoid entering a blocked junction; S disabled that heuristic for one movement. This is an intentionally constructed **behavioral junction control**, not a neutral observational intervention.

| Source observation, development-only | S–I | S–V | N–I | N–V |
|---|---:|---:|---:|---:|
| Per-step FCD samples with main vehicle stationary on internal J lane | **14** | **17** | **2** | **2** |
| Simultaneous stationary main-in-J and stopped upstream cross-vehicle samples | **14** | **17** | **2** | **2** |
| Samples with any upstream cross vehicle stopped | **259** | **259** | **225** | **225** |
| Maximum pocket E2 jam length (meters) | **39** | **39** | **35** | **35** |
| SUMO cross-driver total recorded waiting time (seconds) | **3,540** | **3,503** | **1,180** | **1,180** |

**Interpretation boundaries:**

- Actual stalled main vehicles inside J were observed, supporting the **existence of the source-visible crossing-stall phenomenon** in this constructed network. V did **not** reduce these observations under S: it increased them from **14 to 17**.
- N still produced **two stalled internal-J samples**, so the keep-clear negative control is **not literally free of stationary junction occupancy**.
- Coincident stopped main and cross vehicles could reflect **normal right-of-way yielding**, priorities or other dynamics; these counts **do not prove one vehicle physically caused another's delay**. Source-visible jam and road detector measurements add context, not a controlled causal mediator.
- Recorded road waiting time is **not the primary outcome**: cross drivers' stopped-time sum decreased under V but their preferred-to-arrival total decreased by only ten seconds. The physical signal, priority regime and queue behavior all need interpretation.
- The large S-versus-N absolute cost difference cannot be claimed as a **cooperative** benefit, because it is driven by the physical keep-clear regime being changed, not by voluntary timing under identical rules.

## 5. Scientific decisions and stop rule

| Decision | Disposition |
|---|---|
| Were all four physical arms, IDs and journey-time clocks recorded? | **PASS — 96/96 completed per cell; source data and SHA preserved** |
| Was some physical crossing-stall behavior observed? | **YES, descriptively**, with causation and negative-control purity unqualified |
| Did the current voluntary schedule beat the equally informed I in S? | **NO — +38 network-seconds harm** |
| Did the forecast reliably rank the observed personal/system consequences in this case? | **NO — predicted collective benefit and small personal sacrifice did not materialize** |
| Is actual volunteer consent or acceptable nonparticipant harm established? | **NO — consent modeled, and individual harms occurred** |
| Can this result qualify the present B-H1 policy for confirmation? | **NO — DEVELOPMENT POLICY NO-GO / STOP** |
| Does this disprove the broader coordination hypothesis? | **NO — one synthetic setting, imperfect forecast, unqualified mediation, no independent replication** |

**Final finding:** For the one frozen B-H1 development template and shared-forecast voluntary offer, cooperation was **38 network-seconds worse** and the supposed spillback-relief mechanism did **not** improve under the candidate FCD diagnostic. This negative result is the result to preserve. **Do not modify the simulator, adjust the cohort, retune the forecast, relax fairness or run another seed to rescue this particular protocol.**

**Next scientific decision, not automatically another experiment:** Decide whether the research question warrants a *new, separately justified* physical mechanism or decision design that can truly distinguish voluntary coordination from informed independence, or whether B-H1 should remain closed as a valuable negative development finding. No further traffic execution is authorized by recording these results.

**Historical verdicts preserved:** Experiment 004 D NO-GO, Experiment 006 independent comparison INCONCLUSIVE/fairness failed, Experiment 007 Test A NO-GO, T1 ten-second development NO-GO, and PR #115 cross-framework EVIDENCE INSUFFICIENT.
