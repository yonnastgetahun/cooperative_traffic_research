"""Prospective paired counterfactual estimates, by driver identity.

Never imports label_builder or SUMO; cannot see future simulation outcomes.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Mapping, Tuple
from time import perf_counter

from .audit import sha256
from .link_turn_queue import NonCompletion, evolve
from .schema import InvalidScenario, Parameters, Scenario, Vehicle
from .candidate_routes import check_candidate


@dataclass(frozen=True)
class Prediction:
    status: str
    pred_self_delta_s: float | None
    pred_external_delta_network_s: float | None
    pred_nonparticipant_delta_network_s: float | None
    pred_all_delta_network_s: float | None
    per_driver_baseline_s: dict[str, float]
    per_driver_swap_s: dict[str, float]
    model_version: str
    scenario_sha: str
    parameters_sha: str
    prediction_hash: str
    elapsed_wall_s: float
    uncertainty_status: str = "UNCALIBRATED_POINT_ESTIMATE"
    detail: str = ""


def _scenario_with_changes(scenario: Scenario, replacement: Mapping[str, Tuple[str, ...]]) -> Scenario:
    known = {v.vehicle_id for v in scenario.vehicles}
    if not set(replacement) <= known:
        raise InvalidScenario("Unknown target IDs")
    for vid, alternative in replacement.items():
        check_candidate(scenario, vid, alternative)
    vehicles = tuple(replace(v, route_edges=tuple(replacement[v.vehicle_id]))
                     if v.vehicle_id in replacement else v for v in scenario.vehicles)
    new = replace(scenario, vehicles=vehicles)
    for vid in replacement:
        v = next(v for v in scenario.vehicles if v.vehicle_id == vid)
        if not v.eligible:
            raise InvalidScenario("Route changes require opt-in/eligibility")
    return new


def _predict(scenario: Scenario, replacement: Mapping[str, Tuple[str, ...]],
             params: Parameters, model_version: str, uncertainty_seed: int) -> Prediction:
    if not model_version or not isinstance(uncertainty_seed, int):
        raise InvalidScenario("Frozen model version and integer uncertainty seed required")
    if len(scenario.vehicles) != len({v.vehicle_id for v in scenario.vehicles}):
        raise InvalidScenario("Duplicate driver identities")
    changes = {k: tuple(v) for k, v in replacement.items()}
    after = _scenario_with_changes(scenario, changes)
    t = perf_counter()
    base = evolve(scenario, params)
    modified = evolve(after, params)
    wall = perf_counter() - t
    original = {v.vehicle_id: v for v in scenario.vehicles}
    if set(base.elapsed_s) != set(original) or set(modified.elapsed_s) != set(original):
        raise InvalidScenario("Counterfactual incomplete driver coverage")
    self_delta = sum(modified.elapsed_s[vid] - base.elapsed_s[vid] for vid in changes)
    ext_delta = sum(modified.elapsed_s[vid] - base.elapsed_s[vid]
                    for vid in original if vid not in changes)
    nonparticipants = sum(modified.elapsed_s[vid] - base.elapsed_s[vid]
                          for vid, v in original.items() if not v.eligible)
    total = self_delta + ext_delta
    if abs(total - sum(modified.elapsed_s[vid] - base.elapsed_s[vid] for vid in original)) > 1e-6:
        raise AssertionError("Counterfactual total cannot reconcile to driver-level results")
    # At only one changed driver this is the required own-time scalar. For
    # bundles self_delta means summed change among both changed drivers.
    fields = {"self":self_delta,"external":ext_delta,"nonparticipants":nonparticipants,
              "total":total,"baseline":base.elapsed_s,"swap":modified.elapsed_s,
              "scenario_sha":sha256(scenario),"params_sha":sha256(params),
              "model":model_version,"target_ids":sorted(changes),"uncertainty_seed":uncertainty_seed}
    return Prediction("OK", float(self_delta), float(ext_delta), float(nonparticipants), float(total),
                      {k:float(v) for k,v in base.elapsed_s.items()},
                      {k:float(v) for k,v in modified.elapsed_s.items()},model_version,
                      sha256(scenario),sha256(params),sha256(fields),wall)


def predict_counterfactual(scenario: Scenario, target_vehicle_id: str,
                           alternate_route: Tuple[str, ...],
                           params: Parameters = Parameters(), model_version: str = "E1-PROTOTYPE-v1",
                           uncertainty_seed: int = 0, *, abstain_on_noncompletion: bool = True) -> Prediction:
    try:
        return _predict(scenario, {target_vehicle_id: alternate_route}, params, model_version, uncertainty_seed)
    except NonCompletion as e:
        if not abstain_on_noncompletion:
            raise
        return Prediction("ABSTAIN_NONCOMPLETION",None,None,None,None,{}, {},model_version,
                          sha256(scenario), sha256(params),"",0.0,detail=str(e))


def predict_bundle(scenario: Scenario, replacements: Mapping[str, Tuple[str,...]],
                   params: Parameters = Parameters(), model_version: str = "E1-PROTOTYPE-v1",
                   uncertainty_seed: int = 0, *, abstain_on_noncompletion: bool = True) -> Prediction:
    if len(replacements) != 2:
        raise InvalidScenario("Stage 1B allows exactly two targets in a bundle")
    try:
        return _predict(scenario, replacements, params, model_version, uncertainty_seed)
    except NonCompletion as e:
        if not abstain_on_noncompletion:
            raise
        return Prediction("ABSTAIN_NONCOMPLETION",None,None,None,None,{}, {},model_version,
                          sha256(scenario), sha256(params),"",0.0,detail=str(e))
