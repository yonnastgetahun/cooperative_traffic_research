# Cooperative Traffic Research — Post-T1 SUMO random-event ordering versus physical propagation: source-and-archive final findings

**Date:** November 7, 2026 UTC (approved investigation November 6 Pacific)  
**Classification:** **READ-ONLY SUMO SOURCE + EXISTING T1 B*/C* ARCHIVE INVESTIGATION. ZERO NEW SIMULATIONS.**  
**Preserved scientific decision:** T1 10-second forecast/cooperative policy **DEVELOPMENT NO-GO**. Original Experiment 007 Test A and E1-v2 NO-GO unchanged; reserved cohorts remain unopened.  
**Scientific disposition:** **CONTROL CANDIDATE IDENTIFIED** for a specific *cross-lane random-stream alias*; **actual numerical contribution and any unique physical mediator remain unresolved**. No new model, experiment or simulator modification is approved by this report.

## 1. Why this question matters

The project's foundational question remains whether voluntary collective decisions can outperform equally informed independent traffic decisions **without unacceptable participant or nonparticipant harm**. A useful coordination system would need to predict how volunteers' choices affect drivers who never change their own decisions. Before investing in another externality predictor, we must determine whether observed effects of a departure change arise from the traffic system or from the simulation's treatment of random draws.

The original T1 B/C comparison on previously inspected synthetic development seed 2101 predicted **−50.626 network-seconds** but observed **+618**. The latter was confounded by different per-driver `speedFactor` values (380/1,000 matched IDs). The new B*/C* [controlled development study](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) locked each driver's speed factor to the same identity, retained the twelve original +10-second shifts, and measured **C*−B* = +2,131 network-seconds**: +120 intentional predeparture waiting, +8 insertion delay, +2,003 in-network duration. Among 988 unshifted drivers the descriptive cost difference was +2,177; among 500 nonparticipants +294, including 91 harms >30 seconds.

Those observations are **one development comparison**, not a general causal claim. The earliest changed unshifted FCD observations appeared at **t=27s**, two steps after the first shifted driver appeared in B* but not C*, including one vehicle ~914m away. The [approved source-inspection plan](POST_T1_SUMO_STOCHASTIC_EVENT_ORDER_VS_PHYSICAL_PROPAGATION_SOURCE_INSPECTION_PLAN_2026-11-07.md) called for source-proven explanation candidates before any further simulations.

## 2. Source and evidence provenance (R0)

**Observed engine:** the stored executed command and original logs identify **Eclipse SUMO 1.28.0**, with `--seed 2101` and no `--random`, `--thread-rngs`, `--threads`, `--step-length` or simulation configuration-file override. The original pinned container was `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`.

**Audited official source:** SUMO repository [annotated tag `v1_28_0`](https://github.com/eclipse-sumo/sumo/tree/v1_28_0), whose Git tag object `3deeb6e984b98f167309a76b6780d317a2fd626d` points to **source commit `daf91b5578901d599ac9af53f49d26eeb9aefc3b`**. All code citations below are anchored to this immutable commit; newer documentation or `main` is not substituted for the version under study.

**Source-build limitation:** The container's *version string and image digest* are verified, but this archive contains **no independent image-build manifest establishing that the compiled binary was built from precisely that Git commit** or disclosing every compiler/build flag. Thus the source-path conclusions are **high confidence for the official matching version tag**, and strongly relevant to the pinned 1.28.0 image, but exact binary-to-source SHA parity is **not independently certified**. This is not a reason to invent an unobserved runtime trace.

**Existing observation evidence only:** [completed B*/C* GitHub Actions run 42348701379](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379), [Actions raw artifact 13564199074](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379/artifacts/13564199074), and [permanent evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07). The original Actions artifact ZIP was recovered for this inspection, with **SHA256 `0e92fa1b9221eb1fb3c36783bb7bffe9cfa20658dde15ddbef279cf0ef985d8c`**, matching GitHub's recorded artifact digest. It contains 47 original, canonical-input, run-output and derived-analysis member files. The original network member independently re-hashed to `e3ec1811290f39c1a8e6a2c81e24180c08c71e22e0fcdbeb14fcc740aa87d601`, and canonical B* route input to `601607ee36b4a8216defa6c090eb27c57672d5d307634cb50dbc8d7273885d8e`, both matching their recorded manifests. The separately published permanent tarball's recorded SHA256 is `c3541593131930101ba7237bf2460765c385de5dafa5eab07a986ef1178a396a`; this inspection read the verified **Actions ZIP**, not a fresh independent download/re-hash of that tarball.

**Actual input defaults:** New B*/C* route XML contains 1,000 explicit `<vehicle ... speedFactor="...">` entries and one `<vType id="passenger" vClass="passenger"/>`, without `flow`, device assignments, car-following overrides or manual `sigma`. The network has 2,032 unique XML lane elements, 100 `priority` junctions and 352 `internal` junctions. The invoked executable's command provides no changes to the pinned default `threads=1`, `thread-rngs=64`, `step-length=1s`, or `default.carfollowmodel=Krauss`, as defined by [`MSFrame.cpp` lines 379–389, 555–557 and 814–817](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L379-L389).

**Reconciled B*/C* anchors, not repeated experiments:** The previously completed result, +2,131 = +120 +8 +2,003, and all 1,000 matched IDs, original twelve timing changes, per-ID `speedFactor` parity and 500/500 eligibility labels are retained as measured evidence. Original T1 B/C results remain separate and confounded.

## 3. Source-verified RNG and scheduling pathways (R1)

### The decisive implementation fact: stochastic Krauss car-following uses **lane-assigned RNGs**, not an immutable driver-ID RNG

The matching SUMO 1.28.0 source establishes the following connected chain:

1. [`MSFrame.cpp` lines 814–817](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L814-L817) registers **`thread-rngs` default 64**; [`MSFrame.cpp` lines 379–389](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L379-L389) defaults to 1-second steps and one simulation thread. [`NLBuilder.cpp` lines 399–407](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/netload/NLBuilder.cpp#L399-L407) initializes a parsing RNG, device RNGs, and the lane RNG pool. [`MSLane.cpp` lines 4720–4730](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSLane.cpp#L4720-L4730) constructs **64 different `lanes_i` streams**, seeded in sequence with `seed+i` (for `--seed 2101`: `lanes_20` begins with seed **2121**).
2. [`NLEdgeControlBuilder.cpp` lines 45–48 and 90–100](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/netload/NLEdgeControlBuilder.cpp#L90-L100) initializes a sequential lane numerical counter at zero and increments it on each parsed lane. [`NLHandler.cpp` lines 536–593](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/netload/NLHandler.cpp#L536-L593) parses XML lane elements in order unless explicitly skipping internal/broken geometry. The archived network and the default `no-internal-links=false` configuration support including its 2,032 lanes. [`MSLane.cpp` lines 255–297](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSLane.cpp#L255-L297) assigns each lane **`RNG index = numericalID % number_of_rngs`**; [`MSLane.h` lines 240–248](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSLane.h#L240-L248) returns the shared stream at that index.
3. Critically, [`MSBaseVehicle.cpp` lines 2816–2823](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSBaseVehicle.cpp#L2816-L2823) defines **`vehicle.getRNG()` as the current lane's `getRNG()`**, or the first lane of the vehicle's edge before insertion. It does **not** return a separately seeded, identity-specific generator for ordinary car-following.
4. The T1 route vType has no car-following override. [`MSFrame.cpp` lines 555–557](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L555-L557) defaults to **Krauss**; [`MSCFModel_KraussOrig1.cpp` lines 41–45](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/cfmodels/MSCFModel_KraussOrig1.cpp#L41-L45) uses the vType's default imperfection parameter; [`SUMOVTypeParameter.cpp` lines 1026–1038](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/utils/vehicle/SUMOVTypeParameter.cpp#L1026-L1038) sets **`sigma = 0.5` for ordinary passenger vehicles**. [`MSCFModel_Krauss.cpp` lines 94–117 and 155–173](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/cfmodels/MSCFModel_Krauss.cpp#L94-L117) passes **`veh->getRNG()`** to the stochastic `dawdle2` calculation, which consumes **`RandHelper::rand(rng)`**.

**Meaning:** Vehicles on **different lanes sharing a modulo-64 pool index** can influence one another's *future random draw sequence*, without any direct road connection. A schedule change can change the number/order of vehicles consuming a pool, creating distant simulated-trajectory differences. This is an **active, source-supported coupling mechanism**. It does not prove the exact random draws or quantify their effect on cost, because the archived FCD does not record per-stream RNG states or draw counters.

**A per-vehicle hashed seed exists** in the [`MSBaseVehicle` constructor, lines 108–126](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSBaseVehicle.cpp#L108-L126), but it is **not the RNG that the cited Krauss path uses**. Therefore the existence of an ID hash alone cannot validate per-driver stochastic pairing in B*/C*.

### Finite audit of other active or potentially active sources

| Mechanism/source path in tagged SUMO 1.28.0 | Actual T1 evidence | Status for this comparison |
|---|---|---|
| **Passenger speedFactor loading**, [`MSVehicleControl.cpp` 109–114](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSVehicleControl.cpp#L109-L114), [`MSVehicleType.cpp` 92–95](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSVehicleType.cpp#L92-L95) | Original B/C factors were associated with input order; new B*/C* supplies same explicit factor for 1,000/1,000 IDs, bypassing sampling on this attribute | **CONTROLLED IN B*/C*** |
| **Krauss per-step stochastic dawdling**, `MSCFModel_Krauss.cpp`, `MSBaseVehicle::getRNG`, `MSLane::myRNGIndex` | Default active model, `sigma=0.5`; lane-pool alias observed in archived network | **ACTIVE AND CROSS-LANE ORDER-SENSITIVE** (stream use source-established; exact per-event draw counts not archived) |
| **Load/insertion queue**, [`MSInsertionControl.cpp` 127–151 and 194–214](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSInsertionControl.cpp#L127-L151) | Pending vehicles are queued/iterated; shifting a departure legitimately changes its insertion time, leader/follower and congestion | **ACTIVE; PHYSICAL AND ORDER-SENSITIVE**, but not a unique explanation for remote first divergence |
| **Movement/junction/lane updates**, [`MSNet.cpp` 878–936](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSNet.cpp#L878-L936), [`MSLane.cpp` 1595–1635](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSLane.cpp#L1595-L1635) | Sequential movement planning, junction approach checks, movement, lane changing and insertion; dynamics can propagate locally | **ACTIVE; ENDOGENOUS PHYSICAL RESPONSE POSSIBLE** |
| **Random loading/type/route selection**, `MSRouteHandler` and parsing RNG | One explicit type and one fixed route per ID; explicit speedFactor; no distributions or stochastic flows | Parsing pipeline **ACTIVE**, but no evidence that its random type/route/flow branches were exercised here; **not established as the remaining cause** |
| **Probabilistic flow RNG**, [`MSInsertionControl.cpp` 77–88 and 231–283](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSInsertionControl.cpp#L231-L283) | T1 XML contains **zero `<flow>`** elements; explicit 1,000 vehicles | **INACTIVE FOR THIS INPUT'S FLOWS** |
| **Random departure offsets and random depart speed/position/lane options**, [`MSFrame.cpp` 497 and 546–550](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L497-L550), [`MSLane.cpp` 607–727](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSLane.cpp#L607-L727) | `random-depart-offset=0` by default; no requested random departure options; original external lanes have one traffic lane per road; `default.departspeed=avg` | Specific random branches **not evidenced active** |
| **Junction random all-way-stop tie breaker**, [`MSVehicle.cpp` 5497–5505](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSVehicle.cpp#L5497-L5505) | Archived network has only 100 `priority` and 352 `internal` junctions; no all-way-stop junction type | **No evidence that this conditional branch was activated** |
| **Equipment and device RNGs**, [`NLBuilder.cpp` 399–407](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/netload/NLBuilder.cpp#L399-L407) | Standard output devices produce tripinfo/vehroute/FCD; no explicit stochastic traffic-affecting devices in route XML | RNGs initialized, but **no direct evidence of behavior-changing device draws**; keep **UNRESOLVED** rather than asserting absence |
| **Multiple simulation threads** | Pinned command did not override tagged default `--threads=1`; options and log reflect ordinary single-thread run | **No evidence of parallel nondeterministic scheduling** |
| **Output precision / one-second sampling** | FCD records one state/step and positions/speeds at 0.01 precision; vehroute records per-edge exits | **ACTIVE MEASUREMENT LIMIT**; does not explain all repeated movement differences |

### Competing mechanisms can coexist

The lane-shared PRNG is not a falsification of **real traffic physics**. If the changed departure alters which car follows which vehicle on the *same* lane, physical leader effects and subsequent stochastic driving can both differ. That is a legitimate endogenous response under one simulator realization. But a change in random draw at a remote lane sharing `lanes_20`, **before any physically reachable interaction from the shifted driver**, is a distinct *exogenous common-random-number pairing failure* for a matched counterfactual. Neither mechanism's numerical share in +2,131 network-seconds can be inferred from the existing run.

## 4. Original lane geometry + first-divergence chronology (R2)

**Archive method:** Independently parse the original network `network.net.xml` lane elements in order (2,032 unique lanes) and index from zero, as [`NLHandler`/ `NLEdgeControlBuilder` sequential construction](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/netload/NLEdgeControlBuilder.cpp#L90-L100) specifies. Map **`index mod 64`** to the tagged source's RNG pool. Read **both raw B*/C* FCD** XMLs at the original step and compare identical vehicle IDs and lane/position/speed records. The exact tag/bin mapping is derived from source plus archived network, not invented from the earlier final report.

### All twelve actual proposed departure shifts (the only timing intervention)

| Driver ID | Original B* requested (s) | C* requested (s) | Starting edge |
|---|---:|---:|---|
| veh0113 | 22.6 | 32.6 | C2D2 |
| veh0191 | 38.2 | 48.2 | C6C7 |
| veh0458 | 91.6 | 101.6 | D2D1 |
| veh0626 | 125.2 | 135.2 | C4B4 |
| veh0644 | 128.8 | 138.8 | D9E9 |
| veh0699 | 139.8 | 149.8 | H5I5 |
| veh0760 | 152.0 | 162.0 | B4C4 |
| veh0841 | 168.2 | 178.2 | F8F9 |
| veh0846 | 169.2 | 179.2 | G9F9 |
| veh0848 | 169.6 | 179.6 | D1C1 |
| veh0850 | 170.0 | 180.0 | J7J6 |
| veh0991 | 198.2 | 208.2 | J5I5 |

At t=27 seconds **only the first of these shifts had reached its originally requested departure window**. The next is at 38.2s; later shifts cannot explain a t=27 difference.

### Earliest B*/C* FCD differences and their source-implied RNG alias

| First divergent step | Vehicle (shift status) | Observed lane | Archived lane XML index | Source-implied lane RNG |
|---|---|---|---:|---|
| **25s** | **veh0113 (shifted)**, present B*, absent C* | C2D2_0 | 1748 | **lanes_20** |
| **27s** | veh0022 (unshifted) | F6F5_0 | 1876 | **lanes_20** |
| **27s** | veh0111 (unshifted) | C2D2_0 | 1748 | **lanes_20** |
| **28s** | veh0067 (unshifted) | D9D8_0 | 1812 | **lanes_20** |
| 31s | veh0078 (unshifted) | :D8_5_0 | 627 | lanes_51 |
| 39s | veh0035 (unshifted) | H3H2_0 | 1940 | lanes_20 |
| 39s | veh0191 (second shifted) | C6C7_0 | 1763 | lanes_35 |
| 40s | veh0037 (unshifted) | A4A5_0 | 1684 | lanes_20 |
| 40s | veh0192 (unshifted) | E3E4_0 | 1827 | lanes_35 |

**The lane-index evidence is unusually discriminating:** The first shifted lane, the first two unshifted lanes at t=27, and the next changed lane at t=28 **all share `lanes_20`** even though the roads are geographically separated. The numerical indices 1748, 1812 and 1876 differ by exact multiples of 64. The t=40 unshifted `E3E4_0` observation shares pool **35** with the second shifted vehicle's `C6C7_0` observed from t=39. Such alignment is **strong evidence for the availability and relevance of cross-lane random-stream coupling**; random draws were **not captured**, so it is not a unique proof of the actual path of every event.

**Exact earliest remote record:** `veh0022`, with **unchanged actual departure 5s in both B*/C*** and matched `speedFactor=0.93`, was on `F6F5_0` at t=27. Its B* lane position/speed was **74.58m / 12.53m/s** versus C* **73.79m / 11.75m/s** — differences of **0.79m** and **0.78m/s**, far above the 0.02 source-analysis comparison tolerance. At t=26 its B*/C* position/speed were identical at recorded precision. Its road location was approximately **914m** in straight-line simulation coordinates from the first shifted vehicle on `C2D2_0` at t=27. That distance makes a *direct local physical interaction* from the first shift over two seconds implausible; it does not rule out all global simulator coupling, rounding, or unmeasured paths.

**Same-lane first response:** `veh0111`, already on `C2D2_0` ahead of `veh0113`, had actual departure **23s in both arms** and same `speedFactor=0.92`. At t=27 its B*/C* lane positions were **53.32m / 53.50m** and speeds **12.22 / 12.39m/s**. The newly present shifted driver was **behind** it in B*. A direct follower-braking explanation of this *leader's* early speed difference is insufficient, while same-lane random-stream consumption is plausible. This does not exclude junction/lane-update or other subtle dynamics.

**Later differences and chronology:** `veh0067` diverges on distant `D9D8_0` at t=28, also `lanes_20`; `veh0078` first differs on an internal D8 lane at t=31, compatible with subsequent local propagation but not uniquely explanatory. By t=39–40 the *second* shift begins and additional `lanes_20` and `lanes_35` matches occur. No unshifted divergence was recorded **before t=25**. Subsequent wide network differences (997 of 1,000 IDs eventually differ in at least one saved FCD sample) combine possible physical response and PRNG coupling, not 997 independent causal observations.

**Measurement limit:** FCD samples at one-second intervals; precise random-number draw order, substep queue movements, vehicle acceleration decisions, RNG counters and causal edge/junction mediation are not in the archive. Timestamp proximity and matching pool index support a specific hypothesis, not an independently isolated causal effect.

## 5. Formal separation of remaining uncertainties (R3)

| Category | What is established | Unresolved |
|---|---|---|
| **A. Exogenous shared-RNG coupling** | **SOURCE-SUPPORTED and ARCHIVE-CONSISTENT**: default Krauss uses lane RNG pool 64; observed early distant lanes alias to the same stream as the extra B* shifted vehicle. An extra active vehicle can change the sequence consumed elsewhere independent of direct road contact. | Actual per-step draw/counter traces were not saved. Cannot prove which precise draws changed, or how many of the +2,131 network-s arise through this pathway. |
| **B. Endogenous stochastic traffic response** | **POSSIBLE**: the intervention genuinely changes which vehicles are physically present in the network at particular times, and SUMO computes car-following/junction movement and insertion sequentially. Later localized interactions are plausible. | No controlled per-vehicle random innovations or counterfactual physical mediator intervention to separate them from shared-stream changes. |
| **C. Deterministic insertion/queue/junction propagation** | **SOURCE-VERIFIED AS A GENERAL MECHANISM**: planned movement, junction approaches, execution, lane changes and insertion depend on the current physical state; no run can simply hold these invariant under different departure times. | The archived single-seed FCD cannot uniquely attribute observed local queues, bottlenecks or aggregate harm to this deterministic mechanism. |
| **D. Numerical/observation issue** | One-second FCD and printed precision limit exact ordering, but the earliest remote differences exceed the numerical comparison threshold and continue. | No substep trace / build reproducibility record to certify the exact earliest random update. |

**Answer to the plan's identification question:** The existing comparison is **not cleanly paired with respect to all exogenous random innovations**. Explicit speedFactor parity repaired one failure but did not make the stochastic Krauss driver experience ID-invariant under rescheduling, because its RNG is shared by lanes and even distant lanes can alias. A fixed global seed and preserved driving parameters do not guarantee a vehicle receives the same random innovation absent a physically reachable intervention effect.

### Direct source correspondence versus unique causation

The match between **changed shifted-car presence on `lanes_20` at t=25** and the first unshifted differences on **`lanes_20` at t=27–28** supplies an unusually strong, preregistration-relevant control hypothesis. It is **not** a numerical partition of +2,131s; no source-inspection exercise can reassign the observed network outcome to a stream without a separate controlled counterfactual. The original T1 negative policy decision remains defensible; general cooperative-timing efficacy remains untested.

## 6. Scientific decision (R4): one bounded next control, or stop

**Current decision: `CONTROL_CANDIDATE_IDENTIFIED` for cross-lane RNG-pool alias; `STOP CURRENT T1 PROXY` unchanged.** The archive/source investigation succeeded without any new SUMO run. A new forecast model or reoptimization would be scientifically premature.

**One narrow future discriminating comparison, if separately approved:** The official v1.28.0 option **`--thread-rngs`** sets the number of lane RNG streams ([`MSFrame.cpp` 814–817](https://github.com/eclipse-sumo/sumo/blob/daf91b5578901d599ac9af53f49d26eeb9aefc3b/src/microsim/MSFrame.cpp#L814-L817)). The inspected network contains **2,032** lanes. A prospective **two-arm B*/C*** replay on the already inspected 2101 demand, using the identical pinned binary, original ID-locked vehicle characteristics and original departure schedules, but with **`--thread-rngs 2048` fixed in both arms**, is a source-supported way to remove **cross-lane modulo alias**: each original lane numeric index 0–2031 would map to a distinct stream. Predefine the primary discriminating early readout as whether the **remote `veh0022` / `F6F5_0` difference at t=27** persists when `C2D2_0` and `F6F5_0` no longer share a random stream; monitor same-lane `veh0111` separately.

**Critical qualifications for that candidate:** This changes the random realizations for the entire network and is **not a rerun with identical stochastic noise**. Even `2048` pools would still share draws between multiple vehicles on the **same** lane, and other RNG/global-order effects could remain. Disappearance of the early remote difference would support (not prove) the alias mechanism; persistence would weaken a simple alias-only explanation while leaving other coupling/physical processes. Compare **new B*/C* within the same new RNG configuration**, not a numerical difference between the old +2,131 and new outcomes as though it isolated random-cost contributions. Preserve the all-driver primary cost and participant/nonparticipant harm. Design a new prospective preflight, source hash, hard controls and two-arm ceiling before requesting execution permission.

If that control cannot be specified or fails to answer a distinct physical question, **recommend NO MORE T1 simulations and investigate a different cooperation mechanism**, not repeated RNG pool or forecast tuning. An eventual robust causal timing analysis might require per-driver/per-step counter-based innovations or transparent RNG-state instrumentation, which would entail a **different simulator/source modification protocol** and is **not** authorized or implemented here.

## 7. Final conclusion and research governance

This source-first investigation establishes a concrete architecture-level explanation for one otherwise surprising finding: **vehicles at distant traffic locations can receive different stochastic car-following innovations when a shared lane RNG pool is advanced by a small timing intervention elsewhere**, despite identical per-ID speed factors and `--seed`. The exact tagged source plus original lane ordering and earliest FCD times make this a strong candidate; **the missing RNG event trace prevents declaring it a proven sole cause**.

This brings the project closer to answering whether voluntary coordination can improve traffic because it identifies a critical **experimental-identification prerequisite**: one cannot judge the network externalities of a collective decision until the control accounts for both deliberate changes in traffic and unintended pairing differences in exogenous stochastic behavior. A negative or inconclusive result remains useful.

**No SUMO executions were run, no policy/estimator or source was modified, no reserved/held-out cohort accessed, and no LinkedIn/X publication initiated.** Publish this one consolidated findings report with source-linked evidence. Retain original T1, E1-v2 and Experiment 007 negative decisions. Any follow-on controlled test requires a **separate authorization**.
