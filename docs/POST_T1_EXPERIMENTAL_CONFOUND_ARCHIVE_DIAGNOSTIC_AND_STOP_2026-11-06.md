# Cooperative Traffic Research — T1 B/C driver-heterogeneity confound: archival diagnostic and decision to stop

**Date:** November 6, 2026 Pacific (GitHub run completed November 7 UTC)  
**Scientific decision:** **STOP / NEW PHYSICAL REPLAY NOT EXECUTED.** Original current T1 10-second proxy/policy **DEVELOPMENT NO-GO** remains unchanged.  
**Scope:** One post-authorization, archive-first control-integrity discovery using the immutable original T1 development evidence, not a new SUMO comparison or a new predictive model.

## 1. Research question and why the stop matters

The approved [controlled physical-interaction observation plan](POST_T1_CONTROLLED_PHYSICAL_INTERACTION_OBSERVATION_PLAN_2026-11-06.md) asked whether we could find the earliest traffic interactions through which twelve +10-second T1 departure changes affected 988 drivers whose departures remained unchanged, and identify measurable features that might support a future falsifiable externality forecast. The study was to reuse original development-seed-2101 B and C inputs, perform at most two passively instrumented SUMO replays, and **preserve vehicle dynamics and physical conditions across arms**.

A more fundamental control-integrity problem emerged **before either authorized replay executed**: the original B and C simulations assigned differing realized vehicle-specific speed factors to hundreds of the same driver IDs. The original comparison does not isolate the effects of voluntary departure timing alone.

This matters to the overarching research question — whether voluntary collective decisions outperform equally informed independent decisions without unacceptable harm to participants and nonparticipants — because the comparison must hold all nonintervention driver characteristics fixed before attributing changes among nonparticipants to cooperative decisions.

## 2. Authoritative evidence and independent verification

- [Original successful T1 run 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), [original artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479); 24-entry archive SHA-256: `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`. The original artifact's digest was separately confirmed by GitHub Actions download; it had previously been downloaded and SHA-checked for the [archive-first analysis](POST_T1_ARCHIVE_FIRST_PREDICTION_FAILURE_SCIENTIFIC_FINDINGS_2026-11-06.md).
- Original unchanged B/C route inputs: `sumo_B/routes.rou.xml` SHA256 `3d2984a4010445e8abe03d5855e796a3291b95ca2b0de763f05c0869a1f8a01e`; `sumo_C/routes.rou.xml` SHA256 `707b6c215b0792d4cf4d99c15e1a34670595e51995cd6814bc8ea8a7aa2d1718`.
- Original SUMO B/C tripinfos: B SHA256 `b1afa3b889602af2431a1cd7838da5e9f7d9ac8251d9df84aa937e6a6ddffb1a`; C SHA256 `3a2c1d3873902f3f000819dd273cd2bce2428fc917312453184b350dde22b9a9`.
- Original run code revision `bbc0fadefcaa11d499e394d648526358d97358ee`, SUMO 1.28.0 pinned image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`.

**Independent archival method:** Parse every `vehicle` record in each original B/C `routes.rou.xml` in its *file presentation order*. Parse every `tripinfo` by driver `id`, preserving the `speedFactor` string recorded by SUMO. Compare B/C speedFactor for matched IDs, compare their ordered speedFactor sequences in route-input order, and compare A/B for the unchanged-schedule control. No simulated movement was generated or re-run to obtain these figures.

### Results

| Original archive check | Result |
|---|---:|
| Matched driver identities B/C | 1,000 / 1,000 |
| Drivers whose requested departure changed | 12, each +10 s |
| Matched IDs with different B/C `speedFactor` | **380 / 1,000** |
| Of those, drivers with unchanged requested departures | **368 / 988** |
| Of those, the 12 shifted drivers | **12 / 12** |
| B/C speedFactor strings compared **in input-file presentation order** | **1,000 / 1,000 identical positions** |
| A/B matched-ID speedFactor disagreements (unchanged schedules) | **0 / 1,000** |
| Earliest original preferred departure among speed-factor-changed IDs | **22.6 s** (veh0113) |

The first affected driver `veh0113` was originally scheduled for **22.6 s in B** and **32.6 s in C**. Its recorded `speedFactor` changed from **0.90 (B)** to **1.12 (C)**. The next driver `veh0114`, whose departure was unchanged, changed from **1.22 (B)** to **0.90 (C)**. The latter is exactly the preceding driver's original B factor. The identical B/C **1,000-position input-order sequence** provides especially strong evidence that randomized vehicle attributes were associated with load/file order, not held fixed by driver identity, as requested-departure reordering changed the ordering of vehicles.

**Qualified interpretation:** These observations directly establish *different realized per-vehicle speed parameters between original B and C*. The order-sequence identity strongly supports assignment from a common order-dependent random stream; the simulator's internal source mechanism was not separately inspected. We must not infer that all 618 added network-seconds were caused by speed factor reassignment, nor that no departure timing effects occurred. Their contributions cannot be identified from this confounded B/C comparison.

### Reproducibility sketch (archive-only)

```python
# z is the SHA-verified original T1 ZIP archive; xml.etree.ElementTree as ET
def order(arm):
    root = ET.fromstring(z.read(f"sumo_{arm}/routes.rou.xml"))
    return [v.get("id") for v in root.findall("vehicle")]
def factors(arm):
    root = ET.fromstring(z.read(f"sumo_{arm}/tripinfo.xml"))
    return {v.get("id"): v.get("speedFactor") for v in root.findall("tripinfo")}
b, c = factors("B"), factors("C")
assert sum(b[v] != c[v] for v in b) == 380
assert [b[v] for v in order("B")] == [c[v] for v in order("C")]
```

## 3. Numerical and fairness evidence is retained, but causal attribution is restricted

The observed original **C−B = +618 network-seconds** remains the recorded difference: +120 intentional predeparture wait, +9 SUMO insertion delay and +489 in-network duration. Of this, +614 was experienced by 988 *unchanged-requested-departure* drivers; +543 among 500 nonparticipants; 205 / 1,000 drivers and 102 / 500 nonparticipants had >30s additional observed journey cost.

Those are accurate **descriptive contrasts between the original two SUMO outputs**. They **are not an isolated timing-intervention causal effect**, because 380 matched vehicle IDs had differing realized speed factors between arms. The previously documented 10-second forecast phase fragility is a separate independent warning against treating the nominal edge-bin proxy as physically qualified. Thus the original **DEVELOPMENT NO-GO** still holds; it does not establish that cooperative departure timing itself harms traffic or is futile.

**Correction to prior causal language:** “Twelve shifts caused +618 network-seconds” is unsupported. The scientifically valid statement is “The original C schedule, as simulated with changes both to requested departure times and to some drivers' realized speed factors, produced +618 network-seconds relative to the original B simulation.” The original no-shift B equilibrium, predicted `−50.626`, and all original decisions remain historically intact.

## 4. Authorized run record and reason for stopping

On explicit authorization, a single-use [GitHub Actions observational workflow run 42339346968](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42339346968) began from [PR #103](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/103). The pinned container started, the immutable original artifact was downloaded and its SHA256 digest verified by GitHub Actions, but the offline preflight script **did not execute** because the runner used POSIX `sh` and rejected `set -euo pipefail`: `set: Illegal option -o pipefail`. Every subsequent step, including both B and C SUMO arms and the physical trace analysis, was **skipped**.

Therefore this is **NO REPLAY EXECUTED**, not a failed SUMO experiment, an invalid replay, or a successful physical study. The shell issue is straightforward engineering, but **correcting and restarting the workflow is not scientifically justified under the original observational question now that the central timing-only isolation assumption is violated**. No additional execution attempt is being authorized or initiated.

## 5. Scientific decision and next justified option

**Decision: STOP the original B/C physical-observation replay as currently designed.** Observing the same confounded scenarios with more trajectories could describe the temporal consequences of a *joint perturbation* in departure order and vehicle speed characteristics, but could not isolate the physical externalities produced by the twelve voluntary timing decisions. Retain original archives, the negative T1 decision, the new integrity finding, and the unsuccessful workflow record.

A scientifically meaningful *different* prospective study would first lock every driver's immutable attributes (especially `speedFactor`) identically across independently informed B and cooperative C, preserve routes/network/demand and timing choice parity, and verify per-ID input-and-parameter equality **before simulation**. Only then could two genuinely controlled timing-only schedules test whether the unshifted-driver externalities and early movement chronology survive. Such a study would create a **new corrected development comparison**; it must not be retroactively substituted for original T1 outcomes, must not reuse unseen/reserved cohorts, and requires its own reviewed design and explicit approval. Any forward prediction claim still needs separate independent validation and fairness gates.

**Scientific contribution:** The high-information result here is not a newly discovered junction bottleneck. It is identification of a previously unrecognized randomized vehicle-characteristic confound that prevents a clean inference about voluntary cooperation's effect on nonparticipants. Resolving causal identification is necessary before investing in a better externality predictor. No external/social publication is authorized.
