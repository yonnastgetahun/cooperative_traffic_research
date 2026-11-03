"""Strict named-unit outputs, no rescaling of ego cost as third-party cost."""
from __future__ import annotations
from typing import Mapping


def effects(base: Mapping[str,float], other: Mapping[str,float], selected: set[str], nonparticipants: set[str]):
    if set(base) != set(other) or not selected <= set(base) or not nonparticipants <= set(base):
        raise ValueError("Counterfactual identity sets differ")
    delta = {k: other[k]-v for k,v in base.items()}
    own = sum(v for k,v in delta.items() if k in selected)
    outside = sum(v for k,v in delta.items() if k not in selected)
    nonopt = sum(delta[k] for k in nonparticipants)
    return {"self_delta_s": own, "external_delta_network_s":outside,
            "nonparticipant_delta_network_s": nonopt,
            "total_delta_network_s": own+outside}
