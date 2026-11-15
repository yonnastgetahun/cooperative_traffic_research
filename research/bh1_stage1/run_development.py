#!/usr/bin/env python3
"""Frozen B-H1 development-only physical probe. Not an efficacy experiment.

Must be run ONLY after the Stage-1 static and source gates succeed.
Exactly four frozen cells, original preferred/actual clocks, one seed, no
adaptation or retries for favorable outcomes. No reserved cohorts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import contract
import make_arms
import measurement_contract
import spillback_observation


SEED = 9101
END_S = 2400
ENGINE = "sumo"
ARMS = ("S_I", "S_V", "N_I", "N_V")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args: list[str], cwd: Path, log_path: Path):
    with log_path.open("w") as fd:
        proc = subprocess.run(args, cwd=cwd, stdout=fd, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError(
            f"Command failed with code {proc.returncode}, log {log_path.name}"
        )


def prepare(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    contract.generate(outdir)
    for mode in ("S", "N"):
        run_command([
            "netconvert",
            "--node-files", outdir.joinpath("bh1.nod.xml").name,
            "--edge-files", outdir.joinpath("bh1.edg.xml").name,
            "--connection-files", outdir.joinpath(f"bh1_{mode}.con.xml").name,
            "--tllogic-files", outdir.joinpath("bh1.tll.xml").name,
            "--output-file", outdir.joinpath(f"bh1_{mode}.net.xml").name,
            "--no-internal-links", "false",
        ], cwd=outdir, log_path=outdir / f"network-{mode}.log")
    contract.check_net(outdir)
    contract.check_policy(outdir)
    make_arms.make(outdir)
    measurement_contract.test_contract()
    spillback_observation.test()
    manifest = {
        "classification": "ONE FIXED DEVELOPMENT ONLY PHYSICAL TEMPLATE",
        "seed": SEED, "end_seconds": END_S, "step_seconds": 1,
        "arms": list(ARMS),
        "networks": {m: sha256(outdir / f"bh1_{m}.net.xml") for m in ("S", "N")},
        "input_sha256": {
            f"{m}_{p}": sha256(outdir / f"bh1_{m}_{p}.rou.xml")
            for m in ("S", "N") for p in ("I", "V")
        },
        "trial_is_not_confirmatory": True,
    }
    (outdir / "development-execution-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")


def one_arm(outdir: Path, tag: str):
    physical, policy = tag.split("_")
    base_add = ET.parse(outdir / "bh1-observation.add.xml").getroot()
    detector = base_add.find("laneAreaDetector")
    if detector is None:
        raise AssertionError("Source-defined pocket detector missing")
    detector.attrib["file"] = f"bh1_{tag}.pocket-e2.xml"
    addname = f"bh1_{tag}.add.xml"
    contract.xml_write(outdir / addname, base_add)
    cmd = [
        ENGINE,
        "--net-file", f"bh1_{physical}.net.xml",
        "--route-files", f"bh1_{tag}.rou.xml",
        "--additional-files", addname,
        "--tripinfo-output", f"bh1_{tag}.tripinfo.xml",
        "--fcd-output", f"bh1_{tag}.fcd.xml",
        "--fcd-output.attributes", "id,lane,pos,speed",
        "--step-length", "1",
        "--seed", str(SEED),
        "--threads", "1",
        "--time-to-teleport", "-1",
        "--end", str(END_S),
        "--no-step-log", "true",
    ]
    run_command(cmd, cwd=outdir, log_path=outdir / f"bh1_{tag}.sumo.log")
    print(f"Development-only physical arm {tag}: SUMO exit 0; completeness NOT YET CLAIMED.")


def complete(outdir: Path):
    measurement_contract.evaluate(outdir)
    spillback_observation.evaluate(outdir)
    physical = json.loads((outdir / "fcd-cooccurrence-diagnostics.json").read_text())
    trip = json.loads((outdir / "physical-tripinfo-only-evaluation.json").read_text())
    # Only descriptive gate labels. An observed candidate blockage is not
    # identification of causal mediation.
    block = physical["S_I"]["stopped_main_on_internal_J_steps"]
    cross = physical["S_I"]["simultaneous_stalled_J_main_and_upstream_cross_steps"]
    result = {
        "status": ("DEVELOPMENT_MECHANISM_CANDIDATE_OBSERVED"
                   if block > 0 and cross > 0 else
                   "DEVELOPMENT_MECHANISM_NOT_OBSERVED"),
        "no_confirmatory_inference": True,
        "stopped_internal_J_samples_S_I": block,
        "cooccurring_main_stalled_and_cross_waiting_S_I": cross,
        "stopped_internal_J_samples_N_I":
            physical["N_I"]["stopped_main_on_internal_J_steps"],
        "delta_S_all_driver_s": trip["S"]["all_driver_delta"],
        "delta_N_all_driver_s": trip["N"]["all_driver_delta"],
        "psi_s": trip["psi"],
        "limitation": "one synthetic development template; co-occurrence is not causality; no verified human acceptance",
    }
    (outdir / "development-scientific-disposition.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("all",))
    ap.add_argument("--out", type=Path, default=Path("bh1-dev-only"))
    a = ap.parse_args()
    outdir = a.out.resolve()
    state = {"status": "STARTED", "completed_physical_arms": [],
             "no_confirmatory_inference": True}
    try:
        prepare(outdir)
        state["status"] = "STATIC_VALIDATED"
        for tag in ARMS:
            one_arm(outdir, tag)
            state["completed_physical_arms"].append(tag)
        complete(outdir)
        state["status"] = "COMPLETE_DEVELOPMENT_ONLY"
    except Exception as ex:
        state["status"] = "FAILED_STOP_NO_RETUNE"
        state["error_type"] = type(ex).__name__
        state["error"] = str(ex)
        raise
    finally:
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "attempt.json").write_text(json.dumps(state, indent=2) + "\n")


if __name__ == "__main__":
    main()
