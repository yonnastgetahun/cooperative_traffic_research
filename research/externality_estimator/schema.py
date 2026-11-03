"""E1 input contract. Only prospective information may enter this module.

No SUMO API, live simulator, oracle traffic outputs or labels are accessible here.
All inputs are deterministic, immutable, and independently validatable.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import ceil, floor, isfinite
from typing import Optional, Tuple


class InvalidScenario(ValueError):
    """Prospective scenario/route/feature contract is violated."""


class UncertainScenario(InvalidScenario):
    """Required predecision physical information is unavailable."""


@dataclass(frozen=True)
class Link:
    edge_id: str
    length_m: float
    speed_mps: float
    lanes: int = 1
    # Overrides used by disclosed synthetic test fixtures; must be predecision.
    storage_vehicles: Optional[int] = None

    def __post_init__(self):
        if not self.edge_id or not isfinite(self.length_m) or self.length_m <= 0:
            raise InvalidScenario("Invalid link ID/length")
        if not isfinite(self.speed_mps) or self.speed_mps <= 0 or self.lanes < 1:
            raise InvalidScenario("Invalid link speed/lane count")
        if self.storage_vehicles is not None and self.storage_vehicles < 1:
            raise InvalidScenario("Storage must be >=1")

    @property
    def capacity(self) -> int:
        return self.storage_vehicles if self.storage_vehicles is not None else max(
            1, floor(self.length_m * self.lanes / 7.5))

    def freeflow_ticks(self, speed_factor: float = 1.0) -> int:
        if not isfinite(speed_factor) or speed_factor <= 0:
            raise InvalidScenario("Invalid vehicle speed factor")
        return max(1, ceil(self.length_m / (self.speed_mps * speed_factor)))


@dataclass(frozen=True)
class Turn:
    from_edge: str
    to_edge: str
    junction: str
    conflict_class: str = "all"
    effective_lanes: int = 1

    def __post_init__(self):
        if not all((self.from_edge, self.to_edge, self.junction, self.conflict_class)):
            raise InvalidScenario("Missing turn or junction identifier")
        if self.effective_lanes < 1:
            raise InvalidScenario("Turn lanes must be positive")


@dataclass(frozen=True)
class Vehicle:
    vehicle_id: str
    scheduled_departure_s: float
    route_edges: Tuple[str, ...]
    eligible: bool = False
    speed_factor: float = 1.0

    def __post_init__(self):
        if not self.vehicle_id or not isfinite(self.scheduled_departure_s):
            raise InvalidScenario("Vehicle ID and finite schedule required")
        if not self.route_edges or len(set(self.route_edges)) != len(self.route_edges):
            raise InvalidScenario("Route empty or looped")
        if not isfinite(self.speed_factor) or self.speed_factor <= 0:
            raise InvalidScenario("Invalid speed factor")


@dataclass(frozen=True)
class Feature:
    """An actual observation, not a forecast of announced future demand.

    Observed_at is the time data became available.  For example, an announced
    future departure is a Vehicle scheduled_departure, not a Feature whose
    observed_at is its future departure time.
    """
    name: str
    observed_at_s: int
    source: str

    def __post_init__(self):
        if not self.name or not self.source:
            raise InvalidScenario("Feature metadata incomplete")
        if not isinstance(self.observed_at_s, int):
            raise InvalidScenario("Feature timestamp must be an integer tick")
        illegal = ("tripinfo", "fcd", "label", "counterfactual_truth", "future_queue",
                   "realized", "post_treatment", "oracle")
        if any(word in (self.name + ":" + self.source).lower() for word in illegal):
            raise InvalidScenario("Post-treatment label/future observation prohibited")


@dataclass(frozen=True)
class Scenario:
    links: Tuple[Link, ...]
    turns: Tuple[Turn, ...]
    vehicles: Tuple[Vehicle, ...]
    t0_s: int = 0
    features: Tuple[Feature, ...] = ()
    initial_occupancy: Tuple[Tuple[str, int], ...] = ()
    label_partition: str = "DEV_FIXTURE"

    def __post_init__(self):
        if not isinstance(self.t0_s, int) or self.t0_s != 0:
            # A future version could use a timestamped in-flight state, but
            # silently initializing that state to zero would be clairvoyant.
            raise UncertainScenario("E1 v1 only supports t0=0 with initial empty state")
        if self.initial_occupancy:
            raise UncertainScenario("Nonempty initial state not implemented; abstain")
        if len({l.edge_id for l in self.links}) != len(self.links) or not self.links:
            raise InvalidScenario("Duplicate/empty network edges")
        if len({v.vehicle_id for v in self.vehicles}) != len(self.vehicles) or not self.vehicles:
            raise InvalidScenario("Duplicate/empty driver identities")
        if len({(t.from_edge, t.to_edge) for t in self.turns}) != len(self.turns):
            raise InvalidScenario("Duplicate turn definitions")
        edges = {l.edge_id for l in self.links}
        legal = {(t.from_edge, t.to_edge) for t in self.turns}
        for turn in self.turns:
            if turn.from_edge not in edges or turn.to_edge not in edges:
                raise InvalidScenario("Turn references missing edge")
        for vehicle in self.vehicles:
            if vehicle.scheduled_departure_s < self.t0_s:
                raise UncertainScenario("Already active vehicle requires observed initial state")
            if any(e not in edges for e in vehicle.route_edges):
                raise InvalidScenario("Route references missing edge")
            if any((u, v) not in legal for u, v in zip(vehicle.route_edges, vehicle.route_edges[1:])):
                raise InvalidScenario("Disconnected/illegal route turn")
        if any(f.observed_at_s > self.t0_s for f in self.features):
            raise InvalidScenario("Future observation beyond decision cutoff")
        if self.label_partition not in ("DEV_FIXTURE", "DEV_BUILD", "DEV_CHECK", "HISTORICAL_DIAG_ONLY"):
            raise InvalidScenario("Future independent validation/Test B partition forbidden in E1 development")


@dataclass(frozen=True)
class Parameters:
    q_sat: float = 0.50
    horizon_s: int = 1800
    max_service_token_seconds: float = 2.0
    max_wall_s: Optional[float] = 120.0
    # One source admission per tick from a single approach if congestion permits.
    source_rate_per_lane: Optional[float] = None

    def __post_init__(self):
        if self.q_sat not in (0.35, 0.50, 0.65):
            raise InvalidScenario("Unfrozen q_sat; allowed 0.35/0.50/0.65")
        if self.horizon_s != 1800 or self.max_service_token_seconds != 2.0:
            raise InvalidScenario("E1 temporal/token protocol may not change silently")
        if self.source_rate_per_lane is not None and (not isfinite(self.source_rate_per_lane) or self.source_rate_per_lane <= 0):
            raise InvalidScenario("Invalid source capacity")
        if self.max_wall_s is not None and (not isfinite(self.max_wall_s) or self.max_wall_s <= 0):
            raise InvalidScenario("Invalid wall time budget")
