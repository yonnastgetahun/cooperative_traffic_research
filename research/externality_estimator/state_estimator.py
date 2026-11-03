"""Prospective state intake; t0>0/unknown in-flight state must abstain."""
from __future__ import annotations
from dataclasses import dataclass
from .schema import Scenario, UncertainScenario


@dataclass(frozen=True)
class InitialState:
    t0_s: int
    total_initial_link_occupancy: int
    provenance: str


def estimate_state(scenario: Scenario) -> InitialState:
    if scenario.t0_s != 0 or scenario.initial_occupancy:
        raise UncertainScenario("Nonempty/late initial state is not supported in E1 v1")
    return InitialState(t0_s=0, total_initial_link_occupancy=0,
                        provenance="ANNOUNCED_ZERO_START_NOT_FUTURE_DETECTOR")
