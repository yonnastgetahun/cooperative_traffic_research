# UXsim — independent source-based T1 feasibility ledger (review draft)

**Date:** 2026-11-09 Pacific  
**Scope:** Read-only Python-engine source assessment; **no UXsim installation, model conversion, adapter, smoke test or traffic execution**.  
**Upstream pin:** [toruseo/UXsim `b7e27388757a0e4c64f303c9606a3d5a5ef40388`](https://github.com/toruseo/UXsim/tree/b7e27388757a0e4c64f303c9606a3d5a5ef40388). Primary file: [`uxsim/uxsim.py`](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py).  
**Governing protocol:** [Post-T1 dual-framework feasibility plan](POST_T1_DUAL_INDEPENDENT_SIMULATOR_FEASIBILITY_PLAN_2026-11-08.md). Companion [CityFlow ledger](POST_T1_CITYFLOW_SOURCE_FEASIBILITY_LEDGER_2026-11-09.md) is independently assessed. **SUMO is reference, not ground truth.**

## Frozen scientific contract

Preserve the exact original inspected development-seed-2101 set of **1,000 original IDs, 500 eligible/500 nonparticipant designations, 12 +10-second requested changes, 988 unchanged requests, original fractional preferred and B*/C* scheduled times, and each full ordered external-edge route**. Required per-driver clocks: original preferred `p_i`; requested `s_i`; actual entry `d_i`; completed arrival `a_i`. Required all-driver cost: `Σ(a_i − p_i)`, not a native in-network travel-time mean. The original B*/C* archive and checksum manifest remain read-only; do not import observed SUMO arrivals as targets.

## 1. Driver identities — SOURCE-SUPPORTED conditional representation; **dataset-level mapping UNRESOLVED**

- [Vehicle constructor, 1008–1057](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1008-L1057) accepts a `name`. [Registration, 1149–1159](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1149-L1159) rejects duplicates unless `auto_rename=True`; retains a name-keyed object in `W.VEHICLES` after it leaves the living/running maps.
- **Critical unit distinction:** [`Vehicle` is a vehicle *or platoon*](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1008-L1014); [`World(deltan=5)`](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1699-L1766) defaults to a **five-vehicle packet**, not one individual. [Link admission and capacity updates](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L269-L296) operate in units of `W.DELTAN`.
- **Lossless mapping candidate (NOT implemented):** use one explicit `addVehicle` invocation per original ID, `name=original_id`, `auto_rename=False`, `deltan=1`, `mode="single_trip"`, preserve `p_i`/eligibility as separate immutable fields, and reject any duplicate, missing, extra or grouped ID. A one-packet-per-driver default does **not** satisfy identity.
- **Unresolved:** verified 1:1 mapping against all archived IDs; any consequences of `deltan=1` for mesoscopic flow behavior; C++ engine parity (not examined and **not** a silently approved substitute).

## 2. Original requested departures — **BLOCKED under default timing; alternative parameterization UNRESOLVED**

- [World timing initialization, 1798–1810](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1798-L1810): `DELTAT = REACTION_TIME × DELTAN`; with defaults `reaction_time=1`, `deltan=5`, the time step is 5s. Even with `deltan=1` alone, it remains 1s.
- [Vehicle departure construction, 1065–1074](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1065-L1074) quantizes second-valued input by `int(departure_time / DELTAT)`; [home→wait release, 1179–1184](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1179-L1184) uses that integer. Thus 22.6s is **not** faithfully released with 1s or 5s steps.
- The separate `departure_time_in_second` assignment multiplies the supplied argument by `DELTAT`; its semantics must be audited before using it as a clock. `log_t_link` originates from the **quantized** timestep.
- **Possible but not qualified:** a fractional `REACTION_TIME` with `DELTAN=1` could yield an adequately fine step (e.g., 0.2s). However, this is a **physical reaction-time parameter**, not a pure I/O precision switch; all 1,000 original fractions, floating-point floor edges, algorithm behavior and the scientific meaning of the changed model require separate prospective assessment. Do not round inputs or claim exact preservation merely because the parameter accepts floats.
- **Evidence still needed:** full archive departure-grid inventory; explicit precision-error budget; proof every requested B*/C* time is on the chosen lattice without truncation; requested-versus-first-link admission accounting.

## 3. Fixed complete original routes — API SOURCE-SUPPORTED; original-route crosswalk **UNRESOLVED**

- [`enforce_route`, 1289–1307](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1289-L1307) records a specified link sequence; [origin admission, 249–258](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L249-L258) requires the specified first link; [downstream selection, 1379–1388](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1379-L1388) checks the next specified link or raises.
- **Paper crosswalk:** `SUMO external edge ID → UXsim directed Link name`, `SUMO junction → UXsim Node`, `r_i → ordered list of those Link names`. Require a bijection for *every used external edge*; assert each consecutive link meets at the same node; keep original origin/destination, no route search or replacement.
- **Caveat:** `enforce_route` itself includes a source TODO about full consistency checking; a valid whole-route map has not been established for the original 1,000 trips. Source capability is **not** a full-cohort route-preservation qualification.

## 4. Junction / queue / spillback representation — meaningful primitives SOURCE-SUPPORTED; **scientific comparability UNRESOLVED**

- [Node transfer logic, 303–358](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L303-L358) checks downstream space and in/out/node capacity, signal group and link merge priority; [origin generation, 269–298](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L269-L298) can withhold insertion; [Node flow-capacity setup, 118–131](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L118-L131) and [Link inflow/outflow limits, 569–582](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L569-L582) supply flow/queue constraints.
- **Non-equivalence risk:** these are mesoscopic capacity/signal/merge-priority mechanisms. They do not, from the inspected source, provide a one-to-one match for all SUMO microscopic turn-by-turn conflict, internal-lane, right-of-way and stochastic car-following semantics. The original synthetic network includes **priority junctions**, which makes that gap materially relevant, not cosmetic.
- **Required static gap register (unperformed):** per original junction: competing turns; movement right-of-way; internal connectors; lane count/capacity; signal policy; merge priorities; queue storage; spillback; and whether proposed UXsim rules represent the same mechanism at an appropriate level. Document any micro-conflict as **NOT REPRESENTATIONALLY COMPARABLE** rather than assuming equivalence.

## 5. All-driver original-preference-to-arrival cost — conditional clock capabilities SOURCE-SUPPORTED; **exact metric UNRESOLVED**

- [Home, wait and run states, 1179–1200](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1179-L1200), [first-link admission, 269–295](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L269-L295), [end/abort clocks, 1242–1267](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1242-L1267) and [`traveled_route` link-entry/departure/arrival log, 1447–1500](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L1447-L1500) provide a potential per-name trace.
- A completed vehicle leaves `VEHICLES_LIVING` and `VEHICLES_RUNNING` but remains in `W.VEHICLES` at the inspected source. Abort is explicitly flagged (`arrival_time=-1`); do not treat aborts as zero duration or omit them.
- **Paper ledger:** `original_id,eligible,p_i,s_i,release_tick,first_link_entry_tick,finish_tick,completion_status,route_hash, cost=a_i−p_i`. Reconcile, per ID, `(s_i−p_i)+(d_i−s_i)+(a_i−d_i)=a_i−p_i` and require **1,000 valid completed rows** (else fail). Explicitly do **not** add on-road stopped time to the same cost.
- **Open:** exact arrival-clock convention at `W.T` versus log; quantization error; permanent logs under disabled logging modes; vehicle-abort handling; complete 1,000-ID crosswalk. Standard native `travel_time` is not by itself the original-preference metric.

## Separate stochastic and representational caution

[UXsim's node transfer, 326–346](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py#L326-L346) uses shared world random draws in normal operation; `hard_deterministic_mode` changes selection behavior. Do not claim UXsim eliminates stochastic stream-order confounding by construction or switch determinism to make results easier to interpret. Retain the pinned Python engine; C++ equivalence is uninvestigated.

## Provisional source-only disposition and evidence gaps

| Contract requirement | Current classification | What is missing for static qualification |
|---|---|---|
| 1. Original IDs and eligibility | SOURCE-SUPPORTED **only with deltan=1**; data parity UNRESOLVED | Complete per-original-ID record audit; one-person unit under altered DELTAN |
| 2. Exact subsecond requested departures | **BLOCKED by defaults; alternative UNRESOLVED** | Fractional lattice, numerical flooring and reaction-time-model consequences |
| 3. Every original fixed external-edge route | SOURCE-SUPPORTED API; original mapping UNRESOLVED | Full network/link bijection and all route-continuity checks |
| 4. Meaningful comparable junction constraints | UNRESOLVED; some micro-conflicts may be NOT REPRESENTATIONALLY COMPARABLE | Per-movement gap register and physical interpretation |
| 5. All-driver preferred-to-arrival accounting | UNRESOLVED (per-name lifecycle source exists) | Exact per-name release/admission/arrival audit and clock reconciliation |

**Not GO for simulation or cross-framework validation.** This independent read-only ledger does not establish outcome equivalence, a qualified predictive proxy or favorable coordination. A negative representation finding is publishable science and must not be bypassed by a silently simplified network.
