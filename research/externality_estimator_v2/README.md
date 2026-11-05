# E1-v2-J1: connection-aware junction scheduling (research prototype)

Implements the [frozen V2-I1 executable contract](../../docs/POST_EXP007_E1_V2_I1_EXECUTABLE_IMPLEMENTATION_PROTOCOL_V1_2026-11-04.md) in a **new** package without replacing frozen E1-v1.

## Scientific limitations

- This is a deterministic **synthetic model** of finite-capacity link travel and
  priority-junction movements, not a SUMO emulator or real-road navigation system.
- `foes` and directional `response` come from the **pinned SUMO 1.28.0 static
  movement contract**, not from observed traffic conditions after the decision.
- Multiple static non-foe movements may be *eligible* in one modeled tick when
  both are present, ready, have separate resources and pass physical limits.
  This does not mean SUMO would necessarily discharge both simultaneously.
- The implementation uses a one-lane external road graph, 1-second ticks, FIFO,
  static priority DAG, conservative exclusive service for `cont=1`, the
  original 0.50 veh/s/lane E1 service prior, and zero initial occupancy.
- Priority cycles, noncompletion, or unsupported movement contracts cause
  explicit errors/abstentions instead of fabricated network-benefit claims.
- No future SUMO FCD, tripinfo, matched counterfactual labels, calibration or
  independent validation results are available to the estimator.
- The original Experiment 007 Test A remains NO-GO, E1 Stage 1D
  DEVELOPMENT_NOT_QUALIFIED; independent validation/Test B have not been run.

The next science step after engineering tests is a **separately frozen** new
development-build/check study; old 4101-4105 and 5101-5114 cannot be used as
genuinely unseen labels.
