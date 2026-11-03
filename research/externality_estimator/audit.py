"""Stable predecision manifests, partition guards, and prediction-first provenance."""
from __future__ import annotations
import dataclasses
import hashlib
import json
from pathlib import Path
from typing import Any

from .schema import InvalidScenario

BUILD_SEEDS = frozenset(range(5101, 5107))
CHECK_SEEDS = frozenset(range(5111, 5115))
HISTORIC_SEEDS = frozenset(range(4101, 4106))
BLOCKED_POLICY_SEEDS = frozenset(range(4201, 4211))


def canonical(value: Any) -> bytes:
    if dataclasses.is_dataclass(value):
        value = dataclasses.asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False, default=_serialize).encode("utf-8")


def _serialize(value):
    if dataclasses.is_dataclass(value):
        return dataclasses.asdict(value)
    raise TypeError(f"Cannot serialize {type(value)!r}")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def check_partition(seed: int, partition: str, *, for_calibration: bool = False) -> None:
    if seed in BLOCKED_POLICY_SEEDS:
        raise InvalidScenario("Frozen historical Test B seeds unavailable to development")
    groups = {"DEV_BUILD": BUILD_SEEDS, "DEV_CHECK": CHECK_SEEDS,
              "HISTORICAL_DIAG_ONLY": HISTORIC_SEEDS}
    if partition not in groups or seed not in groups[partition]:
        raise InvalidScenario("Seed does not belong to requested E1 partition")
    if for_calibration and partition != "DEV_BUILD":
        raise InvalidScenario("Model calibration may only use DEV_BUILD")


def save_prediction_once(path: str | Path, record: dict) -> str:
    """No rewrite, append, or label contamination after first prediction."""
    path = Path(path)
    if any(k in record for k in ("observed_external", "observed_all", "tripinfo", "label")):
        raise InvalidScenario("Realized labels cannot share prediction record")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = canonical(record) + b"\n"
    with path.open("xb") as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()


def enforce_no_oracle_imports(package_path: str | Path) -> None:
    """Guard the prospective dependency boundary, not a complete security sandbox."""
    import ast
    for path in Path(package_path).glob("*.py"):
        if path.name in ("label_builder.py", "audit.py"):
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [item.name for item in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            else:
                continue
            if any("label_builder" in mod or mod in ("traci", "sumolib", "libsumo") for mod in modules):
                raise InvalidScenario(f"Oracle/label import in predictor: {path.name}")
