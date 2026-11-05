# E1 After Stage 1D — SUMO 1.28.0 Priority-Junction Rules vs E1 Conflict Model
## Dedicated verification specification and prospective read-only research plan

**Date:** November 4, 2026  
**Status:** SPECIFICATION WRITTEN; dedicated verification NOT YET EXECUTED.  
**Scope of approval:** Author and publish the plan; **no new SUMO simulations, frozen E1 edits, calibration, E1-v2 implementation, fresh-seed validation or Test B** under this writing milestone. An additional approval is required before executing this plan.

## 1. Decision context and exact unanswered question

The [completed P0–P4 E1 investigation](POST_EXP007_E1_P0_P4_PHYSICAL_MECHANISM_FAILURE_FINAL_REPORT_2026-11-03.md) verified that the frozen E1 input adapter assigns every permissible turn at a priority intersection the same group, **conflict_class = all**. The frozen queue engine then accepts at most **one such movement per junction per one-second tick**. That is a documented, conservative model behavior.

The original 10×10 synthetic network contains **360 external one-lane directed roads, 100 priority junctions, 352 internal junctions, 1,320 distinct legal external edge-to-edge turns, 2,992 raw connection XML rows, and 1,320 priority-junction request rows**. The P0–P4 audit found nonzero foe bitsets at 96 of 100 priority junctions. However, **it did not independently establish the exact mapping from request indices to source/target lane connections or quantify which E1-forbidden movement pairs SUMO's encoded junction rules could permit**.

**Primary question:** For the identical frozen network, which *specific lane-to-lane movements* are marked as foes, subject to yield obligations, or not marked as foes in SUMO's encoded priority logic, and how does that static relation differ from E1's same-group one-per-tick restriction?

**Secondary question:** Does the verified static mismatch create a plausible **capacity/availability limitation** in E1 worth specifying as an E1-v2 hypothesis? This stage **does not** determine what share of the observed +2,567/+3,945 network-second wrong-sign effects was *caused* by any junction; that would require a separate, controlled dynamic study.

**Scientific decisions held fixed:**
- Original Experiment 007 Test A = **NO-GO** (8/20 signs correct; Test B withheld).
- E1 Stage 1D = **DEVELOPMENT NOT QUALIFIED** (E1 MAE 1,555.125 network-seconds versus best benchmark B1 1,555.26755, only 0.00917% gain against frozen 5% requirement; two adverse false-benefit cases).
- Independent estimator validation = **NOT STARTED**.
- Cooperative policy Test B = **NOT RUN**.
- Historic 4101–4105 and E1 development 5101–5114 scenarios are already inspected; they cannot become fresh independent model-validation evidence.

## 2. Frozen references, official interpretation, and version discipline

**Project-specific authoritative evidence:**
1. [Prospective P0–P4 investigation plan](POST_EXP007_E1_PHYSICAL_MECHANISM_FAILURE_INVESTIGATION_SPEC_AND_PLAN_2026-11-03.md) and its [published final report](POST_EXP007_E1_P0_P4_PHYSICAL_MECHANISM_FAILURE_FINAL_REPORT_2026-11-03.md).
2. [Full original E1 Stage 1D scientific report](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md).
3. [Permanent raw Stage 1D evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03) with archived 706-member SHA-256 ledger; select ONE archived network input as primary and verify SHA consistency across selected development seed families before generalizing.
4. **Frozen E1 source at Stage 1D execution commit 05b770cf000f84677524e0a1e89bea06ec0e703b**: [input adapter](../research/externality_estimator/scenario_io.py), exact Git blob SHA 4ddc2034944354a1605bc798c8df1850e51ea897; [junction/queue engine](../research/externality_estimator/link_turn_queue.py), blob SHA 0d446e2c52efd2b75adf351ad5d577f442a4ac29.
5. Pinned original SUMO **1.28.0** container image: ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb. Use its matching **sumolib code and junction semantics** for adjudication; later online documentation is explanatory only until reconciled to this image.

**Official SUMO documentation for the planned parser:**
- [SUMO Road Networks — Requests and Junction Indices](https://eclipse.dev/sumo/docs/Networks/SUMO_Road_Networks.html): request index describes a junction movement; **foes** marks conflicts, **response** identifies streams with priority over the subject movement, and **cont** identifies a possible intermediate stop. The **rightmost bit is index 0**. The junction index is **not** necessarily the traffic-light linkIndex. Verify these semantics against 1.28.0 itself.
- [SUMO Networks — PlainXML / Right of Way](https://eclipse.dev/sumo/docs/Networks/PlainXML.html): priority and yielding rules, as well as a caution against manually altering generated network internals.
- [SUMO Intersections](https://eclipse.dev/sumo/docs/Simulation/Intersections.html): internal junctions/links and their role in driving behavior and intersection waiting.
- [SUMO sumolib network Node source](https://github.com/eclipse-sumo/sumo/blob/main/tools/sumolib/net/node.py): a useful independent code-path cross-check for request-bit access and junction connection indexing, but **pin to 1.28.0** before treating it as a normative oracle.

**Do not use an unpinned current sumolib interpretation as the final verdict.** The execution preflight must record exact image digest, Python/sumolib version/source hash and original net.xml hash. Do not mutate network.net.xml or regenerate connections with a newer netconvert.

## 3. Verification layers (do not conflate them)

This is primarily a **static network-rule verification**, not traffic calibration:

| Layer | What can be established | What cannot be assumed |
|---|---|---|
| **A. Legal connection** | Source lane/edge may lead to destination lane/edge in network XML | Legal does not mean vehicle can cross right now |
| **B. Junction request matrix** | Requests encode foe relationships, yielding priority, cont/intermediate handling, and movement index | A zero foe bit does not guarantee two vehicles can cross simultaneously |
| **C. Physical feasibility** | Source lane ordering, same downstream storage/receiving slot, internal lanes, blocking, speed, and available service may limit crossing | Static "non-foes" is not equivalent to unrestricted capacity |
| **D. E1 deterministic abstraction** | Same-junction all-class exclusion restricts the second class user in a one-second tick | This is a simplified discrete-time service rule, not SUMO's true lane-level dynamics |
| **E. Observed simulator outcome** | Archived five-second aggregate flows/waiting and trip outcomes can describe where divergence occurred | They cannot uniquely prove which movement was prevented at the stop line; Stage 1D has no 1-second FCD |

**Strongest valid outcome of this plan:** A **version-checked movement-level static compatibility and yield matrix**, compared to E1's allowed simultaneous movement sets, with explicit *unknown and dynamically constrained* categories. It is not by itself a causal attribution of Stage 1D predictor error.

## 4. Preregistered narrow hypotheses and counterexamples

**H-J1 — Overrestriction of non-foes:** At least one junction has two independently mapped legal movements on **different inbound and outbound external links** for which the corresponding request bits do not mark a foe relationship, but E1 would still reject their joint one-tick crossing because both turns share conflict_class=all.

- **Supports:** A version-validated movement-index mapping, mutually zero foe bits, independent source/destination, and explicit E1 one-per-tick rejection.
- **Contradicts:** No such pair after complete mapping and physical source/receiving filters, or the apparent pairs result from wrong request indexing.
- **Qualification:** Say "potentially compatible under encoded static foe logic", **not** "SUMO would definitely discharge both simultaneously."

**H-J2 — Priority asymmetry lost:** A movement's response bits distinguish must-yield-to-higher-priority connections from lower-priority foes; E1 discards these distinctions and instead chooses among same-group turns with its own round-robin ordering.

- **Supports:** Verified directional response matrix and at least one asymmetric priority relation for mapped legal movements that E1 cannot represent.
- **Contradicts:** No asymmetry after source-level mapping, or a mistaken bit orientation/connection index creates the apparent directional relation.
- **Qualification:** The source-priority mismatch is not a measured collision, fairness or travel-time error.

**H-J3 — E1 restriction can be less/more severe than physical constraints depending on vehicle context:** Even a mapped static non-foe pair may be unable to pass together because the arrivals share a single incoming FIFO queue, merge to a single receiving lane, lack available gap/storage, or depend on an internal wait. Conversely, static high-priority/low-priority relation can produce time-separated flow without a one-per-junction hard cap.

- **Supports:** An explicit eligibility filter and a table of "non-foes but physically coupled" examples.
- **Contradicts:** No surviving candidate pair after topology/source/destination restrictions.
- **Qualification:** Do not equate request compatibility with a computed capacity in vehicles/second.

**H-J4 — Junction abstraction plausibly contributes to calibration insensitivity:** The original E1 q_sat=0.50 and 0.65 settings produced identical full 1,000-driver predicted trajectories for 30/30 development-build interventions. Shared all-conflict scheduling may dominate some service decisions, but this is **not established** by the tie alone.

- **Supports:** No-SUMO binding-constraint instrumentation of the unchanged E1 on independent toy fixtures showing an active conflict limit when q_sat changes do not alter flow.
- **Cannot establish in this stage:** How much original Stage 1D externality error this caused, without an authorized controlled model and/or physical intervention.

## 5. Staged read-only plan, decision gates and smallest footprint

### J0 — Evidence and pinned-semantics gate: NO SUMO runs

**Input:** Existing immutable Stage 1D original-release ZIP, per-member SHA ledger, exact historical source commit and pinned SUMO 1.28.0 **documentation/parser inspection only**.

- Verify **archive hashes** and all selected original network files; record if network topology/version differs by seed. No new netgenerate or netconvert calls. If networks differ, classify and process each unique hash rather than quietly treating one as universal.
- Pin and inspect the original version's connection ordering, request-index mapping, foes/response bit operations and cont behavior. Record which semantics are confirmed by 1.28.0 code, which are stated only in current public docs, and any unresolved difference.
- Audit original XML element inventory: external edges/lanes, priority/internal junctions, junction incoming/internal lane identifiers, per-request indices/bitstring lengths, original lane-to-lane connections and via attributes.
- Confirm that junctions under study are priority controlled; do not introduce traffic-light timing or TLS assumptions where no traffic light exists.

**J0 PASS:** All source bytes and intended 1.28.0 parsing semantics pinned; any unmatched/missing field documented. **J0 STOP:** Wrong/unverifiable artifact source, ambiguous bit orientation, incompatible version metadata or incomplete network. Publish blocker; **do not invent a movement matrix**.

### J1 — Lane-connection ↔ request-index mapping: key epistemic gate

Create a deterministic mapping at the **junction-link (lane-connection)** level, retaining external edge/road identifiers for explanation:

- Map each priority junction's request[index] to the exact from-edge/from-lane → to-edge/to-lane movement and any via/internal-lane identity, taking **the pinned SUMO implementation's connection order** as reference.
- Preserve raw junction incoming lanes, internal lanes, request indices, response and foes bitstrings, cont flag and raw connection metadata, including source/target, fromLane/toLane, direction and state where present.
- Parse **foes and response from right to left** (rightmost bit is connection index 0). Validate integer indexes and bitset widths, response subset of foes where applicable, uniqueness, index coverage and cross-reference to every mapped connection.
- Treat traffic-light linkIndex as a **distinct index namespace**, not an alias for junction request index. Because these are priority intersections, TLS linkIndex may be absent entirely.
- Independent cross-check: two separately implemented decoders or pinned 1.28.0 sumolib getLinkIndex/areFoes/forbids or equivalent APIs, **subject to verifying that API and signature exist in the pinned version**. Resolve discrepancies against actual pinned source, not sample guesses. Record raw byte offsets/IDs for ambiguous connections.
- Handle duplicated/raw internal connection rows carefully: the previously counted **2,992 raw XML connection rows** include internal junction and via-related structure, whereas **1,320 distinct legal external edge-to-edge turns** and **1,320 priority request rows** happen to have equal counts in the audited topology. **Do not assume that numerical equality proves a one-to-one index assignment.**

**J1 PASS:** All request indices in the studied network uniquely resolve to the intended lane connections and pass independent cross-checks, with zero unknown or contradictory mappings. **J1 PARTIAL:** Publish mapped fraction and the full unresolved IDs; restrict conclusions to uniquely matched junctions. **J1 STOP:** If ordering or bit interpretation cannot be verified, do not infer concurrent-turn compatibility.

### J2 — Static compatibility and directional yield audit: NO SUMO runs

For each verified priority junction, enumerate **unordered pairs of distinct legal movements**; preserve both directional request records:

- Extract foe(i,j), foe(j,i), response(i,j), response(j,i), cont(i), cont(j) with original bit orientation and mapped physical movements.
- Classify each pair as **mutual non-foes**, **foes with asymmetric yield**, **foes with symmetric or undetermined yielding**, or **unknown/inconsistent mapping**. Do not force symmetry if the versioned representation does not justify it.
- Separately flag **same incoming external lane**, **same downstream receiving external lane**, **shared internal lane/via**, **possible merge**, **cont/intermediate waiting** and unknown geometric constraints. These are *independent reasons why static non-foes may not be physically simultaneously passable*.
- Derive a conservative subset: **mutual non-foes, separate incoming and outgoing lanes, no documented shared internal lane, and unique verified mapping**. Label "potentially concurrently eligible if actual presence, gaps and space permit", not "actual simultaneous capacity".
- Inventory response asymmetries and cases where a lower-priority movement has to yield; retain directed movement IDs rather than collapsing everything to edge-to-edge turns.
- For all 100 priority junctions, report pair counts and coverage. Highlight unknowns rather than dropping difficult junctions from the denominator.

**J2 PASS:** Classification reproducible for all uniquely mapped movements. **J2 CAUTION:** Non-foe pairs with shared receiving or upstream FIFO are explicitly excluded from the clean concurrent-eligibility count. **J2 STOP:** If bitset semantics or index-map failures invalidate the pair status, report only inventory/unknowns.

### J3 — Exact frozen E1 comparison and no-SUMO fixtures

Without editing the estimator, read its exact source blob and inspect the initial-state, queue and junction rule:

- E1 input adapter creates one external-edge turn entry per unique legal edge-to-edge path, each marked conflict_class=all.
- E1 simulator marks (junction, conflict class) as used on the first chosen crossing in a 1s tick. Subsequent movements of the same group are rejected, even if SUMO's static request matrix classifies them as potential non-foes.
- E1 also restricts throughput by link/turn capacity tokens, input-edge FIFO head readiness, downstream receiving slots and source admission. These additional constraints must be enumerated explicitly.
- Compare **sets of potentially concurrent turns** under the verified SUMO static matrix with **what E1's one-tick group rule admits**; quantify per-junction counts and examples, without modeling actual SUMO vehicle simultaneous movements.
- Reproduce four small **no-SUMO fixture classes** with the frozen engine, varying fixture conflict labels only for explanatory comparisons: (a) separate inbound/outbound non-foe turns; (b) real foes with response asymmetry; (c) same-source FIFO or shared downstream slot; (d) cont/intermediate wait assumption or unknown compatibility.
- Independently verify E1 physical invariants and no-future-data rules. Do not turn fixture outcomes into a recalibrated E1 version or use original development labels as acceptance evidence.

**J3 PASS:** Discrepancy table and exact frozen-engine behavior reproduced with zero source modifications. **J3 CAUTION:** Changing fixture conflict labels is a structural hypothetical illustration, not an evaluated corrected estimator or an estimate of real SUMO gain.

### J4 — Mechanism decision, outcome classification and next authorization boundary

Produce a single **P0–P4 follow-on scientific report** with this decision taxonomy:

1. **VERIFIED STATIC MISMATCH:** At least one well-mapped, externally independent, mutual-non-foe turn pair is excluded by E1's all-class rule; evidence only for a difference in static rules, not a proven cause of E1's MAE.
2. **NO DEMONSTRATED ELIGIBLE MISMATCH:** Complete and valid mapping found no qualifying independent non-foe pair; restrict claims, reconsider whether this is the highest-value E1-v2 target.
3. **PARTIAL / INSUFFICIENT RULE MAPPING:** Unverified 1.28.0 source semantics, ambiguities or missing request/connection links prevent a general verdict; retain exact problematic IDs.
4. **DYNAMIC EFFECT UNKNOWN:** This is the default even after finding a mismatch; archived 5-second SUMO detector files cannot establish whether specific vehicles crossed in the same one-second interval or how much E1 error this produced.

Rank any **E1-v2 junction-fidelity hypothesis** based on verified static discrepancy and physically plausible constraints. Never claim the Stage 1D failed gate is rescued; it remains **DEVELOPMENT NOT QUALIFIED**. No new estimator is built or validated in this step.

## 6. Quantitative outputs and machine-readable audit contract

Deliver these original-source-linked, deterministic artifacts:

- **e1_junction_rule_source_manifest.json:** pinned image and sumolib/source hashes, original network and report SHA, source code paths, original evidence release URLs, version and parsing contract.
- **sumo_request_to_connection_map.csv:** junction ID/type, request index, fromEdge/fromLane, toEdge/toLane, via/internal lane, raw foe/response/cont, decoded index subsets, parser/version ID, confidence status and reason for uncertainty.
- **sumo_priority_pairwise_rules.csv:** junction ID, movement IDs i/j, directional foe/response flags, static classification, shared-source/destination/internal flags, independent-lane eligibility class and unresolved reason.
- **e1_vs_sumo_junction_rule_differences.csv:** junction, original turn pair, inferred static non-foe status, exact E1 conflict class, separate physical constraint flags, E1 allowed simultaneity, verdict/unknown source.
- **junction_rule_summary.csv:** all 100 priority junctions including mapped/unknown movements, requests, pair counts, mutual non-foes, clean independent candidates and E1-excluded pairs. Include zero rows/junctions.
- **fixture_rule_comparisons.json:** frozen model input/version, toy movement IDs, stipulated compatibility, exact ticks/arrivals under original E1 class and explanatory fixture-only alternate class, all unchanged physics parameters.
- **independent_crosscheck.json:** two decoders or pinned sumolib cross-check results, differing IDs, and independently verified bit interpretation.
- **scientific_readout.md:** PASS/PARTIAL/STOP for each stage, evidence limits, source of discrepancy and controlled next-test recommendation.

**Nonnegotiable accounting:** Report all **request-index, movement and junction denominators**. Never count a request bit as a separate driver or interpret a legal connection as a trip outcome. Keep static conflict, priority yield, physical space and vehicle flow in separate columns.

## 7. Prespecified negative controls, checks and scientific risks

- **Bit-direction trap:** use the official example where request index 2, response 001 and foes 011 must reference movement 0 as a higher-priority blocker and movements 0/1 as foes; reverse the bits deliberately in a unit test and require failure.
- **Index-namespace trap:** a junction request index and TLS linkIndex are **not automatically interchangeable**; force negative test with arbitrary TLS numbering.
- **Count coincidence trap:** 1,320 legal external edge-to-edge pairs and 1,320 request elements could have different connection multiplicities; test exact physical lane/turn matching, not count equality.
- **Single source lane:** on this one-lane external grid, two turns from the same inbound road cannot be assumed jointly available simply because static request bits are zero.
- **Shared receiving lane:** two non-foe turns merging into one downstream lane may still be limited by receiving storage or gaps.
- **Internal lane/cont:** vehicle can potentially wait inside a junction; requests alone do not provide an observed crossing-time distribution.
- **Foes versus response:** presence of a foe is not identical to "has the right of way" and a lower-priority foe need not impose the same stop on both directions.
- **No traffic-light invention:** all audited main intersections are priority-controlled; absence of signal phases is not a model error in this synthetic topology.
- **Historical data contamination:** any use of Stage 1D 5111/5114 false-benefit cases to prioritize examples is **retrospective**, never holdout validation.
- **No causal inflation:** an E1-excluded static non-foe pair does not imply positive network improvement if the E1 rule were changed; physical-model counterfactual would require new separately frozen experiments.

## 8. What is not authorized under this plan

**No new SUMO simulation**. Do not invoke SUMO (including tiny intersection micro-tests) in this planning milestone. **No edits to E1** and no reranking, calibration or training. The future execution of **J0–J4 archive/source analysis** must be separately authorized; it may use the pinned SUMO 1.28.0 *source/parser* as a read-only reference without launching traffic simulations.

If static encoding remains ambiguous, a **separate new micro-simulation protocol** may be proposed later, specifying exact selected junction, lawful conflicting and nonconflicting turn movements, pinned SUMO 1.28.0 configuration, one or two vehicles with controlled arrivals, explicit expected behavior, observational outputs, negative controls, and a strict maximum run budget. Such runs would require a distinct approval and would test physical feasibility, **not** E1's network-scale accuracy.

If static mismatch is verified, **E1-v2 remains a separate prospective design**, with new source-freeze, data-generation budget and disjoint development/validation seeds. Existing E1 Stage 1D 5111–5114 and original 4101–4105 can never be made unseen again.

## 9. Success and downstream decision

**Verification success** means *we accurately know what the frozen SUMO network encodes and which of those encoded relations E1 ignores or overrestricts*, with the uncertainty of dynamic capacity explicitly preserved. **Failure/partial** also counts as a scientific deliverable if mapping cannot be verified; do not guess.

Upon separately approved J0–J4 completion, the next decision is:
- If verified mismatches exist and are physically relevant, **specify** a candidate connection-aware E1-v2 junction model and a **new prospective** development-check design, without retroactive success claims.
- If no material mapping discrepancy is found, favor investigation of timing/queue/receiving/insertion mechanisms rather than presuming junction conflict is the main culprit.
- If ambiguous, require source/tooling or specifically controlled micro-simulation work before claiming verified compatibility.

**The scientific objective remains unchanged:** Understand and predict network externalities → independently validate a *new, frozen* estimator on unseen simulations → only if qualified, Test B compares cooperative versus equally informed independent routing subject to individual and nonparticipant fairness. No Stage 2 or Test B approval is implied by this plan.

**Publication boundary:** GitHub scientific-plan documentation only. No LinkedIn or X posting without separate review and explicit user approval.
