# Cooperative Traffic Research — T1 ID-locked B*/C* controlled development study: final scientific report

**Date:** November 7, 2026 UTC (authorized November 6 Pacific)  
**Study classification:** **DEVELOPMENT-ONLY; ONE PREVIOUSLY INSPECTED SEED (2101); TWO NEW SIMULATION ARMS; NOT CONFIRMATORY**  
**Scientific decision:** **STOP the current T1 10-second timing forecast and policy.** Original **T1 DEVELOPMENT NO-GO**, Experiment 007 Test A NO-GO, and E1-v2 NO-GO **remain unchanged**. New controlled evidence does **not** establish general timing-coordination efficacy or unique physical causal mediation.

## 1. Why this experiment was necessary

The foundational question is whether **voluntary collective traffic decisions can produce lower all-driver network travel cost than equally informed independent decisions without unacceptable participant or nonparticipant harm**. Earlier T1 seed-2101 feasibility predicted that cooperative C, after moving just 12 eligible departure times by +10 seconds, would save 50.626 network-seconds compared with equally informed independent B, yet SUMO produced +618 network-seconds. The original signed difference was computed correctly but was **not a clean timing-only comparison**: a [later original-archive audit](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md) found that **380 of 1,000 same vehicle IDs, including 368 unchanged-departure IDs, received different `speedFactor` values** because the new requested departures changed SUMO input presentation order.

The prospectively approved [ID-locked timing control plan](POST_T1_ID_LOCKED_VEHICLE_ATTRIBUTES_CONTROLLED_TIMING_RETEST_PLAN_2026-11-06.md) therefore specified a **new B*/C*** comparison on the **same previously inspected development seed**, using the exact original fixed routes and original B/C departure choices but explicitly assigning each vehicle's **original B tripinfo `speedFactor` to that same ID in both arms**. The purpose was not to rescue the old result or retune the model; it was to determine what, if anything, we could infer about broader traffic responses after eliminating this known vehicle-attribute confound.

**Primary question:** Does the original twelve-driver timing schedule change all-driver preferred-departure-to-arrival cost and unshifted-driver outcomes when each driver's recorded desired-speed multiplier is held fixed across the matched B*/C* inputs?

**Secondary question:** Do passive vehicle and road-exit observations locate the earliest differing traffic interactions, and do they justify a new falsifiable externality-forecast hypothesis?

## 2. Design, source integrity and exact provenance

- Synthetic original 10×10 SUMO road network, **1,000** vehicle IDs, originally preferred departures over 200 seconds, original independent traffic-aware fixed routes; 500 designated eligible participants and 500 nonparticipants.
- **B***: original independent B departure schedule, no shifts. **C***: original cooperative C schedule, the **same 12 +10-second requested departures**, 988 unchanged. No policy resampling, route reassignment, new opt-in assumptions, model/pressure coefficients, bins or phase changes.
- Canonical source is [original T1 run 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), [artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), original ZIP digest `sha256:b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`.
- Original source revision `bbc0fadefcaa11d499e394d648526358d97358ee`. Pinned **SUMO 1.28.0** container image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. [New single-use implementation at execution commit `f943db3`](https://github.com/yonnastgetahun/cooperative_traffic_research/tree/f943db3d2e9decd14ed17f8b374fbb3c4f9b4429/research/t1_timing) is research code, not the original forecast.
- Preflight independently verified SHA-256 of source network, original B/C routes, original B/C tripinfo, original preferred demand; exact 1,000 IDs, 500 eligible, 12 shifted, original B/C route equality and all remaining input vehicle attributes.
- Per-ID speed factors were **extracted from original B tripinfo** (recorded to 2 decimal places), then inserted explicitly and identically in every B*/C* vehicle XML record. The new static manifest and resulting tripinfo confirmed **1,000/1,000 matched per-ID speed factors** across the two executed arms. These rounded explicit factors are **not identical to the original unrounded stochastic draws**, so B* is not a byte-for-byte replay of historical B.
- Original network/route choices, vehicle types, behavioral input settings and SUMO physics were unchanged except the explicit common per-ID speed-factor control and C*'s twelve recorded departure changes. Both input XML files were sorted by requested departures. Identical SUMO seed **does not guarantee all other random event streams remain vehicle-ID-paired**.
- Exactly **two** newly authorized SUMO runs executed, B* and C*. Passive FCD (lane, position, speed at the existing simulator step) and complete vehicle-route edge exit times were collected with tripinfo, statistics, collision records, command and hash manifests.

### Verified run outcome and preservation

[GitHub Actions execution 42348701379](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379) passed **all scientific stages**: offline preflight; B* simulation and control gate; C* simulation and control gate; matched-driver/physical diagnostic analysis; [raw artifact 13564199074](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379/artifacts/13564199074). The overall Actions job is marked **failure solely because the post-analysis release step attempted to invoke `gh` inside the pinned SUMO container, where `gh` was absent** (exit 127). No scientific step failed and no extra simulation was launched.

A separate [preservation-only Actions run 42348947234](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348947234) then **succeeded without any SUMO execution**. It verified the complete archived evidence and published the permanent [T1 B*/C* original-plus-controlled evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07).

**Permanent archive:** `t1-idlocked-dev2101-complete-evidence.tar.gz`, 7,895,065 bytes, SHA256 `c3541593131930101ba7237bf2460765c385de5dafa5eab07a986ef1178a396a`. The release also includes SHA256 manifests for the archive and every member. It contains original T1 files, the identity-locked B*/C* input files and canonical 1,000-driver manifest, full new raw SUMO outputs and FCD/vehroute observations, and the machine-computed findings JSON/Markdown.

## 3. Independently reconciled network cost and fairness

Primary network cost is **sum across all 1,000 drivers of (actual arrival − original preferred departure)**. Requested wait and insertion are included; in-network stopped waiting is a subcomponent of duration and **must not be added twice**. The totals below were checked both by the execution output and independent re-reading of the original and new archived tripinfo and input route files.

| Cost, network-seconds | B* | C* | C*−B* |
|---|---:|---:|---:|
| Intentional predeparture shift | 0 | 120 | **+120** |
| SUMO departure insertion delay | 858 | 866 | **+8** |
| Actual in-network trip duration | 211,317 | 213,320 | **+2,003** |
| **Total preferred-departure-to-arrival cost** | **212,175** | **214,306** | **+2,131** |
| Mean per driver (all-driver cost / 1,000) | 212.175 | 214.306 | **+2.131** |

**All 1,000 trips completed in both arms.** B*/C* control checks were `CONTROL_PASS`: ID identity, unchanged routes, explicit speed factor by ID and per-driver clock reconciliation. Both arms reported **zero collisions, emergency braking, emergency stops and teleports**. This does not establish real-road safety. SUMO `waitingTime` (already included within in-network duration) **increased +1,527 vehicle-seconds** in C*; `timeLoss` increased +1,994.73 seconds. Both differ from the original confounded B/C outcomes; their differences cannot be isolated as "the speed-factor contribution" because B* and C* are newly changed conditions.

| Matched group | n | Aggregate C*−B*, network-s | Helped | Harmed | Unchanged | Additional cost >30s |
|---|---:|---:|---:|---:|---:|---:|
| **All drivers** | 1,000 | **+2,131** | 438 | 479 | 83 | **187** |
| 12 requested-departure shifts | 12 | −46 | 6 | 6 | 0 | 1 |
| 988 unchanged requested departures | 988 | **+2,177** | 432 | 473 | 83 | **186** |
| Eligible participants | 500 | +1,837 | 212 | 243 | 45 | 96 |
| Nonparticipants | 500 | **+294** | 226 | 236 | 38 | **91** |

For all drivers, median individual cost change = 0s; 90th percentile = +46s, 95th percentile = +71s, maximum additional cost = **+197s**, maximum benefit = **−153s**. The fixed-shift group is not synonymous with all eligible participants, and the nonparticipants are separately preserved.

The 810 unshifted drivers sharing **some** fixed route edge with any shifted driver accumulated +2,314 network-seconds; 178 without such route edge overlap accumulated −137. This **is not time-aligned edge interaction or random assignment** and cannot establish mechanism or causal exposure.

**Interpretation:** Even after fixing the identified per-driver speed-factor mismatch, this **one new, better-controlled development schedule** produced network harm and material nonparticipant delays. It does not prove timing coordination always harms the network; it also does not demonstrate that the observed +2,131s is exclusively caused by timing changes, because other event-order-dependent simulator randomness remains possible.

## 4. Physical chronology and why it does not establish unique causation

Passive FCD and vehroute output passed archive and identity checks. The **earliest shifted driver's planned B* departure was 22.6s** (`veh0113`, delayed to 32.6s in C*). Its earliest measured FCD divergence occurred at **t=25s**, when it had entered road `C2D2_0` in B* but was absent from C*.

The first recorded **unshifted-driver** FCD deviations occurred **at t=27s**, approximately two simulation seconds later, including:

- **`veh0111` on `C2D2_0`**, the same lane as `veh0113`: B* lane position 53.32m versus C* 53.50m. A local shared-edge interaction is plausible, but the trace does not establish which movement or constraint caused the change.
- **`veh0022` on `F6F5_0`**, at B* lane position 74.58m versus C* 73.79m. At that same step, the first shifted driver was **about 914m away in straight-line network coordinates**. This near-simultaneous remote divergence is not readily explained by a direct *local* roadway interaction propagating from that vehicle over two seconds. It **raises** the possibility of additional event-order/RNG coupling or another unmeasured scheduling interaction, but **does not prove its exact cause**.

No unshifted-driver FCD discrepancy was detected **before the first changed B* requested departure**, a useful negative control. Once movement differences began, 997 of 1,000 driver identities eventually had at least one different FCD snapshot. This is evidence of widespread divergence between two simulator realizations, **not** 997 independent estimates of the timing intervention.

Lane-level stopped-vehicle sample counts changed in both directions (using stopped-speed threshold ≤0.1m/s): examples were `D5C5_0` −1,187, `C2D2_0` −1,138, `H2G2_0` +970, `C6D6_0` +941, `F2G2_0` +894. These describe spatial redistribution in the instrumented runs, **not** causal bottlenecks. Neither FCD steps nor edge exit timestamps recover substep yielding rules, exact causal junction priority or a unique queue mediator.

**Frozen nominal-clock mismatch remains substantial:** on 123 shifted-driver edge traversals, mean observed-minus-nominal road-entry times were approximately **+74.80s in B*** and **+69.89s in C***. These are correlated edge samples on one development cohort and do not constitute independent validation. The original **−50.626 network-second predicted benefit** was based on the frozen nominal-edge/10-second-bin proxy and **ranked neither the original confounded B/C result nor the new B*/C* outcome correctly**. The predicted-to-new-realized signed contrast is approximately **+2,181.626 network-seconds**, an *in-sample diagnostic*, not a calibrated model accuracy statistic.

## 5. What the evidence establishes, and what remains unanswerable

| Question | Evidence status |
|---|---|
| Did the new study correct the known random per-ID `speedFactor` reassignment? | **Yes, verified 1,000/1,000 per-ID parity in both inputs and output, original fixed route and timing choices retained.** |
| Were there exactly two newly simulated development arms and no new seeds? | **Yes.** B* and C* only; preservation run had no SUMO execution. |
| Did cooperative C* outperform equally informed independent B* on all-driver cost? | **No in this one development case:** C* cost +2,131 network-s, with severe individual/nonparticipant harms. |
| Did C* affect vehicle traces and drivers without requested departure changes? | **Yes descriptively**; extensive observed divergence among unshifted drivers. |
| Can we attribute all of +2,131s to physical congestion generated by precisely the 12 departure shifts? | **No.** Locking speed factors does not prove equality of remaining random streams or global scheduling operations; early remote divergence is a specific warning. |
| Does this identify a unique junction/queue bottleneck suitable for a new externality predictor? | **No.** Same-edge physical effects are plausible, but early remote differences and distributed response leave causation underidentified. |
| Has model predictive skill, statistical generality, voluntary human acceptance or real-world cooperative advantage been proven? | **No.** One already inspected seed, no new predictor, no independent data, no real human compliance. |

### Methodological distinction

A same-seed B*/C* paired comparison with equal recorded per-ID speed factors is meaningfully **better controlled** than the original B/C. But because the simulator's other event-order-sensitive stochastic processes have **not** been held constant or independently characterized, it should not be labeled a complete isolated timing-only **causal** effect. Likewise, aggregate unshifted harm is not the effect of an independently randomized treatment applied to unshifted drivers.

## 6. Final scientific decision

**Decision: current T1 10-second proxy/policy DEVELOPMENT NO-GO remains in place; stop at the approved two-run limit.** We did not rerun the original flawed B/C arms, use fresh or reserved cohorts, tune parameters, reoptimize schedules or produce a new model. The original Experiment 007/E1-v2 failures and never-executed reserved evaluations are untouched.

**What was learned:** The primary original control-integrity failure can be repaired in a new matched development comparison, yet harmful aggregate and nonparticipant outcomes persist *in that better-controlled case*. The physical record confirms real differences in vehicle movements, including a temporally early, spatially remote divergence that warns against naively assigning all aggregate effects to road queue propagation. Thus there is **not yet sufficient uniquely identified physical evidence to justify fitting another externality estimator**.

**Single next scientific decision if T1 is revisited:** First define, without new runs, how SUMO's **remaining vehicle-event stochastic streams and insertion/update ordering** can be paired or diagnosed across changed departure schedules. Only after establishing a genuinely isolating control would a separately approved prospective timing-only physical/causal experiment be justified. Do **not** silently make the simulator deterministic, remove realistic driver heterogeneity or use additional seeds to rescue C*. A scientifically defensible alternative is to suspend the T1 mechanism and compare fundamentally different forms of coordination.

**Connection to the founding question:** A voluntary cooperative system must reliably predict and bound effects on **drivers who never change their decisions**. This study reinforces why observed externalities and serious nonparticipant harms matter, but it does not establish that voluntary timing can create fair, repeatable collective benefit over equally informed independent behavior.

**Publication and governance:** Consolidated scientific report and permanent GitHub evidence only. No external LinkedIn/X publication authorized or initiated.
