#!/usr/bin/env python3
"""Development-only execution supervisor with durable per-attempt failure evidence.

This supervisor cannot dispatch reserved seeds. It wraps the already-qualified
frozen development rehearsal rather than modifying scientific source.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import shutil
from datetime import datetime, timezone

FROZEN = "be2e8d27c78c8b6de4891115d6d951edc877ac6e"
WINDOWS = (200, 600, 1200)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def execute(out, seed, window, frozen_root, source, runner=None):
    # Fail before creating output or invoking subprocess.
    if type(seed) is not int or seed != 2101 or type(window) is not int or window not in WINDOWS:
        raise ValueError("Development supervisor permits seed 2101 and frozen windows only")
    if not (Path(frozen_root) / "experiments/experiment_002/time_aware.py").is_file():
        raise ValueError("Frozen source missing")
    if Path(out).resolve() == Path.cwd().resolve() or Path.cwd().resolve() in Path(out).resolve().parents and Path(out).resolve().name in ("results", "source", "frozen"):
        raise ValueError("Attempt output cannot overwrite runner inputs")
    if not (Path(source) / "scenario.json").is_file():
        raise ValueError("Development input missing")
    s = json.loads((Path(source) / "scenario.json").read_text())
    if s.get("seed") != 2101 or s.get("window_seconds") != window or s.get("no_holdout") is not True:
        raise ValueError("Development input provenance mismatch")
    out = Path(out)
    if out.exists():
        raise ValueError("Attempt directory must be new: no overwrites or silent retries")
    out.mkdir(parents=True)
    attempt = {"seed": seed, "window_seconds": window, "status": "FAILED",
               "scientific_commit": FROZEN, "heldout_authorized": False,
               "started_at_utc": datetime.now(timezone.utc).isoformat(),
               "stage": "runner", "files": {}}
    try:
        script = runner or "experiments/experiment_002/m3_qualification/run_development_v01.sh"
        env = os.environ.copy()
        env.update(SEED=str(seed), WINDOW=str(window))
        # Runner expects source/ and frozen/ in cwd; do not modify those inputs.
        with (out / "runner.log").open("wb") as log:
            result = subprocess.run(["sh", script], cwd=Path.cwd(), env=env,
                                    stdout=log, stderr=subprocess.STDOUT, check=False)
        for dirname in ("results", "postprocess"):
            folder = Path.cwd() / dirname
            if folder.is_dir():
                shutil.copytree(folder, out / dirname)
        attempt["returncode"] = result.returncode
        if result.returncode:
            attempt["error"] = "Development runner exited nonzero"
        else:
            attempt["status"] = "COMPLETE"
    except Exception as exc:
        attempt["error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        for p in out.rglob("*"):
            if p.is_file() and p.name != "attempt.json":
                attempt["files"][str(p.relative_to(out))] = sha256(p)
        attempt["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        (out / "attempt.json").write_text(json.dumps(attempt, indent=2, sort_keys=True) + "\n")
    return attempt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--seed", required=True, type=int)
    p.add_argument("--window", required=True, type=int)
    p.add_argument("--frozen-root", required=True)
    p.add_argument("--source", required=True)
    args = p.parse_args()
    a = execute(args.out, args.seed, args.window, args.frozen_root, args.source)
    print(json.dumps(a))
    if a["status"] != "COMPLETE":
        sys.exit(1)

if __name__ == "__main__":
    main()
