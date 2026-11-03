"""E1 v1 point forecasts are not independently calibrated intervals."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Reliability:
    status: str
    calibrated: bool
    reason: str


def reliability(*, complete:bool, known_turn_conflicts:bool, known_initial_state:bool=True) -> Reliability:
    if not complete or not known_initial_state:
        return Reliability("ABSTAIN",False,"Incomplete network/initial information")
    if not known_turn_conflicts:
        return Reliability("LOW_CONFIDENCE",False,"Conservative unknown-conflict junction approximation")
    return Reliability("UNCALIBRATED_POINT",False,"No new independent validation completed")
