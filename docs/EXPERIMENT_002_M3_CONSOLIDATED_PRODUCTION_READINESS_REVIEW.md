# M3 consolidated production-runner and release-control qualification

**Status: IN PROGRESS — held-out execution NO-GO.** This is one combined engineering milestone, not authorization for reserved evaluation seeds.

## Scope and acceptance criteria

### A. Production runner
- General-seed execution path implemented without changing frozen scientific commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.
- Complete scenario manifest, frozen SHA, pinned SUMO digest, per-attempt identity, source hashes, and 30-scenario completeness.
- Frozen R3/R4 semantic equivalence established on permitted independent development evidence.
- Missing, failed, duplicate, and substituted attempts cause fail-closed aggregation.
- Evidence retained even when an actual simulation or postprocessor fails; no silent retries or seed substitution.
- All tests run with development inputs or synthetic fixtures only.

### B. Independent release controls
- Verify active main-branch ruleset and applicable branch restrictions.
- Independently inspect the live protected GitHub environment's wait timer, administrator bypass, and deployment branch policy through authorized settings access. Screenshot-only evidence is labeled as such.
- Demonstrate no active held-out workflow and no unauthorized dispatch path.
- Verify release-record provenance, immutable scientific/image pins, and an explicit later approval requirement.

### C. Consolidated decision
- Publish links to actual successful/failed test runs, machine-readable artifacts and review commit.
- Mark each gate PASS / FAIL / UNVERIFIED with direct evidence.
- Production-readiness GO requires every applicable gate to pass. An unverified environment gate is not a PASS.
- Held-out execution remains NO-GO until a separate explicit authorization after production qualification.

## Verified baseline
- Full supervised development SUMO run `40944291962`: three successful regimes and archived evidence.
- Offline orchestration and subprocess failure tests `40944022907`: successful.
- Environment API read is unavailable through the current GitHub connector; independent environment verification remains blocked.
- The development supervisor allows seed 2101 only. No reserved evaluation seeds may be generated or inspected.

## Current decision
**NO-GO for production execution and held-out evaluation.** The above criteria define the single consolidated completion gate; this document does not claim that unfinished work has passed.

## Latest independent repository settings evidence

GitHub ruleset ID `26009049` was read directly. It is active on the default branch and includes deletion prevention, non-fast-forward prevention, and a pull-request requirement with stale-review dismissal and review-thread resolution. It requires **zero** approving reviews and lists no bypass actors. This verifies the repository ruleset, **not** the protected Actions environment.

The environment administration endpoint remains unavailable to the connected GitHub client. Therefore the ten-minute timer, administrator bypass, and environment branch restrictions remain **UNVERIFIED**. Do not mark production release controls as passed.

## Implementation increment

`production_orchestration_preflight_v01.py` now expresses the exact 30 planned case identities, frozen source/image preflight, and fail-closed dispatch boundary. This is **non-executing planning code**, not a completed general-seed production runner. Its CI tests must pass before it is counted as verified. Actual general-seed generation, native observation, R3/R4 integration, failure recovery, and guarded deployment remain incomplete.
