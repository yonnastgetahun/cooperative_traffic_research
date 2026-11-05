# E1 J0–J4 — Final SUMO 1.28.0 Priority-Junction Rules Verification

**Date:** November 4, 2026 (GitHub execution November 5 UTC).  
**Scientific verdict:** **VERIFIED STATIC JUNCTION-RULE MISMATCH; DYNAMIC EFFECT AND CAUSAL CONTRIBUTION TO E1 ERRORS UNKNOWN.**  
**Study type:** Read-only analysis of the frozen original Stage 1D traffic network and the *actual tagged SUMO 1.28.0* Python network-source implementation; immutable original E1 source; no-SUMO model fixtures. **Zero new SUMO traffic simulations, zero E1 model edits, zero new training or validation.**

**Controlling prospective specification:** [J0–J4 SUMO–E1 priority-junction verification plan](POST_EXP007_E1_SUMO_PRIORITY_JUNCTION_RULES_VERIFICATION_SPEC_AND_PLAN_2026-11-04.md).  
**Exact source audit code:** [read-only verifier](../research/audits/e1_sumo_priority_junction_j0_j4.py) and [GitHub Actions pre-merge audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41948036136).  
**Original data:** [permanent Stage 1D release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03); original execution [run 41737336992](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992).

## Executive result

The archived 10×10 synthetic SUMO grid encodes **many lane movements which are not foes**, including movements from *different incoming roads to different outgoing roads*. The frozen E1 network adapter instead assigns **every possible turn at each priority junction the same \`conflict_class='all'\`**. Its one-second queue engine therefore accepts **at most one movement in that class per junction and time tick**.

The discrepancy is not merely suggested by documentation: **all 1,320 request indices were independently mapped to their exact lane-to-lane connections using the actual pinned SUMO 1.28.0 \`sumolib\` source**, and the original foe and directional yielding bits were verified by SUMO's own network APIs against a separate XML decoder. **No request index remained unresolved**.

| Frozen-network measurement | Result |
|---|---:|
| Original priority junctions | **100** |
| Incoming-to-outgoing external lane movements / request indices | **1,320 / 1,320** |
| Distinct unordered within-junction movement pairs | **8,836** |
| Mutually non-foe pairs under SUMO's static requests | **5,764** |
| Non-foe pairs with distinct incoming, outgoing and initial internal-via lanes | **3,940** |
| More conservative above subset with both \`cont=0\` | **2,212** |
| Foe pairs | **3,072** |
| Foe pairs with directional yield asymmetry | **3,072** |
| Priority junctions with at least one independent non-foe pair | **100 of 100** |
| Original E1 all-conflict rule allows either such pair in one tick | **0** |

**Interpreting these numbers:** The **3,940** static candidate pairs (and the narrower **2,212** no-intermediate-wait pairs) do **not** represent 3,940 observed pairs of vehicles or a measured throughput shortfall. The pairs might not have arriving vehicles at the same time, might compete for upstream/downstream space under other conditions, or might be constrained by internal-junction dynamics. They establish that E1's *static exclusion* is stricter than the original encoded **foe** relationships. Nothing in this study establishes the *magnitude* or *direction* of a change to network travel time if E1 were redesigned.

**Prior scientific disposition preserved:** Original Experiment 007 Test A **NO-GO** (8/20 directional agreement); E1 Stage 1D **DEVELOPMENT NOT QUALIFIED** (mean E1 externality MAE 1,555.125 network-seconds on four development-check seeds, 0.00917% below the best historical baseline instead of required 5%; two severe wrong-sign predicted-benefit cases). Independent estimator validation **NOT STARTED**; cooperative routing Test B **NOT RUN**.

## J0 — Original bytes, common network semantics and exact SUMO source: PASS

The verification ran only on existing archived data; it rechecked **all 706 original Stage 1D members** against the per-file SHA-256 ledger in the permanent evidence release and checked each development seed's network bytes against its original scenario manifest.

**Subtle but material provenance point:** All ten original network XML files have **different raw SHA-256 hashes**, because each \`netgenerate\` execution recorded its own timestamp and output file path. Their **canonicalized road-edge, junction and connection definitions are identical** across all ten seeds. Canonical traffic-structure SHA-256:

\`69c5c32e13987646944cbc7b072d586732402c5b8f3651c379c06fecee65ee14\`.

This is **one common traffic-rule structure with ten distinct metadata-bearing network files**, not ten different networks and not ten byte-identical files.

**Pinned independent implementation:** The tagged [SUMO v1_28_0 source](https://github.com/eclipse-sumo/sumo/tree/daf91b5578901d599ac9af53f49d26eeb9aefc3b/tools/sumolib) at commit \`daf91b5578901d599ac9af53f49d26eeb9aefc3b\`; the original pinned simulator had SUMO executable version 1.28.0. The audit checked the pinned code paths in \`net/node.py\` and \`net/__init__.py\` (not unversioned latest code). The \`net.xml\` schema's internal \`version='1.20'\` is the generated file-format version **not** a mismatch with the SUMO 1.28.0 executable.

For E1, the exact original development source commit is \`05b770cf000f84677524e0a1e89bea06ec0e703b\`. Audited source Git blob SHAs:
- \`research/externality_estimator/scenario_io.py\`: \`4ddc2034944354a1605bc798c8df1850e51ea897\`;
- \`research/externality_estimator/link_turn_queue.py\`: \`0d446e2c52efd2b75adf351ad5d577f442a4ac29\`.

**Archive integrity PASS does not imply new scientific validation.** The development-check seeds (5111–5114) are already inspected; no new data were generated here.

## J1 — Every junction request mapped to the correct lane connection: PASS

**Three independent agreement paths for all 1,320 movements:**

1. Follow \`junction.incLanes\` order, then its listed outgoing lane connections, matching the pinned \`sumolib.net.Node.getLinkIndex\` code path.
2. Independently decode the \`via\` internal lane identifier \`:junction_requestIndex_laneIndex\` embedded in the original generated connection XML. The two methods agree **1,320/1,320**.
3. Import the **original pinned SUMO v1_28_0 \`sumolib\`** with \`withFoes=True\`, invoke its \`Node.getConnections\` and \`Connection.getJunctionIndex\` methods, and match from-lane, to-lane and via-lane IDs to the two independently reconstructed mappings. They agree **1,320/1,320**.

For each unordered pair, the audit also independently compared the right-to-left request-bit interpretation with SUMO's actual \`Node.areFoes\` in both directions and \`Node.forbids\` in both directions: **35,344 individual directional checks**, zero mismatches.

**Critical indexing distinction:** The request index is **not** automatically the traffic-light linkIndex. SUMO request bitstrings read **rightmost bit = index 0**. The \`foes\` bit marks crossing/merging conflicts, whereas the \`response\` bit separately represents the movement(s) that have priority over the subject movement. The static verifier preserves both directions, rather than assuming that a foe bit means the same priority obligation in each direction. <https://eclipse.dev/sumo/docs/Networks/SUMO_Road_Networks.html>.

**J1 exit:** No unknown or ambiguous request mappings in this exact synthetic network. Does not establish observed simultaneous crossings.

## J2 — Static conflict, priority and independent-lane pair matrix: VERIFIED

The pinned network has **360 external directed roads, each with one lane**, **100 priority junctions**, **352 internal junctions**, **1,320 unique external turns** and **2,992 raw XML connection entries** (including internal connection rows). The 100 priority junctions divide into four with 2 turns, 32 with 9 turns and 64 with 16 turns.

| Priority junction group | Junctions | Unique movement pairs | Non-foes | Independent non-foes | Independent non-foes with \`cont=0\` for both |
|---|---:|---:|---:|---:|---:|
| 2 movement requests | 4 | 4 | 4 | 4 | 4 |
| 9 movement requests | 32 | 1,152 | 768 | 480 | 224 |
| 16 movement requests | 64 | 7,680 | 4,992 | 3,456 | 1,984 |
| **Total** | **100** | **8,836** | **5,764** | **3,940** | **2,212** |

There are **3,072 foe pairs**, all of which exhibit directional yield asymmetry in the frozen request matrices. Another **1,824 mutual-non-foe pairs** are excluded from the independent-lane candidate count because they share an incoming or receiving external lane or the same initial via lane.

**Concrete verified example, priority junction A0:**
- Request **0:** \`A1A0_0 → A0B0_0\`, via \`:A0_0_0\`.
- Request **1:** \`B0A0_0 → A0A1_0\`, via \`:A0_1_0\`.
- Both request rows mark \`foes=00\`, \`response=00\`, and \`cont=0\`.
- Their incoming and outgoing road lanes are distinct. **E1 assigns both \`conflict_class='all'\`**, preventing two such modeled crossings in one 1-second tick even if both are eligible and all separate receiving constraints are satisfied.

The pair is **potentially nonconflicting according to encoded static foe logic**. No measured fact is asserted about two actual vehicles arriving at A0 simultaneously, safe passing speed, acceleration, gap acceptance, or a sustained vehicle/hour discharge rate.

The full 8,836-row pair matrix and all 3,940 static candidate-rule differences are machine-readable and included in the accompanying archived verification evidence; the compact per-junction summary includes all 100 junctions, including corners.

## J3 — Original frozen E1 behavioral comparison and no-SUMO fixtures: PASS

The original E1 adapter builds a turn table with one \`conflict_class='all'\` for all legal movements at a given junction. In the unchanged queue engine, once a movement consumes \`(junction, conflict_class)\` in a tick, subsequent members of that class are refused for the rest of that tick. This applies **regardless of whether SUMO's static request bits mark two independent moves as foes**.

The verifier reran the existing no-SUMO E1 test suite successfully and ran paired explanatory *toy E1 model fixtures*, varying only the conflict-class labels of the two A0 movements. All vehicle data, synthetic edge lengths and capacity parameters remained the same within a pair.

| Global \`q_sat\` (veh/s/lane) | Original all-class movement crossing ticks | Two deliberately separately labeled toy conflict classes |
|---|---|---|
| 0.35 | **5, 6** | **5, 5** |
| 0.50 | **4, 5** | **4, 4** |
| 0.65 | **4, 5** | **4, 4** |

**Scientific interpretation:** The original E1 all-class abstraction deterministically defers one of these stipulated compatible turns by one model tick, whereas a *hypothetical fixture with different class labels* can represent them crossing together. **These are tests of E1's modeled rule with deliberately simple synthetic link geometry, NOT SUMO executions, and NOT evaluation of a redesigned estimator on Stage 1D labels.** There is no evidence that changing E1 to the fixture's rule would reduce its externality MAE.

## J4 — Scientific verdict and evidence limits

### Verified

- The archived static junction request-index mapping is complete and matches exact pinned SUMO 1.28.0 source/API semantics.
- SUMO's frozen priority network encodes large numbers of **mutually non-foe, source/receiving-distinct movement pairs**, all of which E1's same-junction single class excludes from a *single one-second tick*.
- E1's frozen deterministic behavior is reproducible. Its capacity model is structurally coarser than SUMO's rule-level representation.
- A high-level connection-aware junction model is a **scientifically motivated candidate** for a new, versioned E1-v2 research hypothesis.

### Not established

- That any specific pair of vehicles was physically able and ready to cross at the same time in the original Stage 1D SUMO simulations.
- How frequently, or where, SUMO actually discharged two such non-foe vehicles within the same simulation second.
- A causal contribution of E1's junction group rule to the large **+2,567 / +3,945 network-second** wrong-sign cases or the overall Stage 1D development error.
- That relaxing E1's conflict-class rule would necessarily increase predicted congestion fidelity or improve out-of-sample externality accuracy. Other E1 approximations (source timing, link-wide FIFO, downstream receiving, speed and queue propagation) remain.
- That all such non-foe pairs should be treated as freely concurrent in an E1-v2 algorithm; priority, shared internal lanes, receiving capacity, gap acceptance and intermediate waits still need explicit modeling.

**Final classification: VERIFIED STATIC MISMATCH; DYNAMIC EFFECT UNKNOWN.** This is an important, bounded **physical-model comparison** result; it is **not** scientific GO for E1, a validated E1-v2, or a collective-coordination result.

## Recommended next research decision — new authorization required

The original scientific sequence is unchanged. A reasonable next **separate** milestone is to draft a **prospective E1-v2 junction and movement-capacity design** that uses pinned, source-validated per-movement foe/priority information but still enforces lawful FIFO, turn and downstream storage constraints, with an uncertainty/abstention strategy. Model source and fixtures must be frozen before seeing any *new* development outputs. **Used seeds 4101–4105 and 5101–5114 are contaminated for untouched validation** and must remain retrospective diagnostics only.

Alternatively, if proving actual dynamic conflict discharge is the immediate scientific goal, a separately frozen and authorized pinned-SUMO micro-simulation or passive instrumentation replay could test observed simultaneous crossings and isolate physical mediators. That is **new research**, not a feature of this static source audit. Such a protocol must bound seeds, simulator arms, input changes, equivalence checks and causal inference limits before any execution.

**Neither approach is automatically authorized by this J0–J4 completion.** No changes to E1, new SUMO simulation runs, Stage 2 independent validation, policy Test B or LinkedIn/X publication occurred here.

## Reproducibility and durable evidence

- [J0–J4 prospective source-verification specification](POST_EXP007_E1_SUMO_PRIORITY_JUNCTION_RULES_VERIFICATION_SPEC_AND_PLAN_2026-11-04.md).
- [Original Stage 1D raw evidence release, 706 original member bytes and SHA ledger](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03).
- [Exact SUMO v1_28_0 pinned sumolib implementation](https://github.com/eclipse-sumo/sumo/tree/daf91b5578901d599ac9af53f49d26eeb9aefc3b/tools/sumolib), and [official network-format/request documentation](https://eclipse.dev/sumo/docs/Networks/SUMO_Road_Networks.html).
- [E1 frozen source inspection and J0–J4 reproducible no-SUMO audit program](../research/audits/e1_sumo_priority_junction_j0_j4.py); its GitHub workflow reads existing original evidence with a sparse checkout of exactly the tagged SUMO source.
- [Pre-merge independent GitHub audit pass](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41948036136) with uploaded tables. The complete movement map, 8,836-row pair matrix, all 3,940 rule differences, per-junction table, fixture traces, cross-check metadata, checksum source manifest and readout are planned for **one permanent J0–J4 release on the main-branch audited workflow**. That release must be checked before claiming durable publication.
- [Compact verified rule-class summary](results/exp007_e1_j0_j4_junction_rule_summary.csv) and [one-lane priority junction examples](results/exp007_e1_j0_j4_examples.csv).

**Research integrity:** Historical Experiment 007 Test A **NO-GO** and E1 Stage 1D **DEVELOPMENT NOT QUALIFIED** remain unchanged; independent estimator validation and Test B still **not executed**.
