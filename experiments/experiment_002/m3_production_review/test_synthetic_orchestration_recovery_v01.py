#!/usr/bin/env python3
"""Offline failure-recovery rehearsal. Synthetic IDs only; no SUMO or scientific imports."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

IDS = tuple(f"mock-{n:02d}" for n in range(10))
WINDOWS = (200, 600, 1200)
STAGES = ("retrieve", "generate", "simulate", "postprocess", "archive")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def execute(root, inject=None):
    """Preserve an attempt record even when a stage fails; never retry or replace."""
    root = Path(root)
    records = []
    for scenario in IDS:
        for window in WINDOWS:
            key = (scenario, window)
            folder = root / f"{scenario}-{window}"
            folder.mkdir(parents=True, exist_ok=False)
            attempt = {"scenario": scenario, "window": window, "source": "synthetic",
                       "state": "failed", "stage": "initializing"}
            try:
                for stage in STAGES:
                    attempt["stage"] = stage
                    if inject == (scenario, window, stage):
                        raise RuntimeError("injected failure at " + stage)
                    if stage == "simulate":
                        payload = json.dumps({"scenario": scenario, "window": window,
                                              "synthetic": True}, sort_keys=True).encode()
                        (folder / "synthetic-evidence.json").write_bytes(payload)
                        attempt["artifact_sha256"] = digest(payload)
                attempt["state"] = "complete"
            except Exception as exc:
                attempt["error"] = str(exc)
            finally:
                (folder / "attempt.json").write_text(json.dumps(attempt, sort_keys=True) + "\n")
                records.append(attempt)
    return records

def verify(root):
    root = Path(root)
    expected = {(s, w) for s in IDS for w in WINDOWS}
    found = set()
    errors = []
    for path in root.glob("*/attempt.json"):
        try:
            a = json.loads(path.read_text())
            key = (a["scenario"], a["window"])
            if key not in expected or key in found or path.parent.name != f"{key[0]}-{key[1]}":
                errors.append("invalid or duplicate identity")
            found.add(key)
            if a["source"] != "synthetic" or a["state"] != "complete":
                errors.append("ineligible attempt")
            evidence = path.parent / "synthetic-evidence.json"
            if not evidence.is_file() or digest(evidence.read_bytes()) != a.get("artifact_sha256"):
                errors.append("missing or corrupt evidence")
        except (KeyError, ValueError, OSError) as exc:
            errors.append("unreadable attempt: " + str(exc))
    if found != expected:
        errors.append("missing scenarios")
    if len(list(root.iterdir())) != 30:
        errors.append("unexpected scenario directories")
    return not errors, errors

class TestRecovery(unittest.TestCase):
    def test_clean_run(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(len(execute(d)), 30)
            self.assertTrue(verify(d)[0])
    def test_each_stage_failure_retains_attempt_and_blocks_aggregate(self):
        for stage in STAGES:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as d:
                records = execute(d, ("mock-03", 600, stage))
                self.assertEqual(len(records), 30)
                a = json.loads((Path(d) / "mock-03-600" / "attempt.json").read_text())
                self.assertEqual(a["state"], "failed")
                self.assertEqual(a["stage"], stage)
                self.assertFalse(verify(d)[0])
    def test_missing_attempt(self):
        with tempfile.TemporaryDirectory() as d:
            execute(d)
            (Path(d) / "mock-00-200" / "attempt.json").unlink()
            self.assertFalse(verify(d)[0])
    def test_corrupted_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            execute(d)
            (Path(d) / "mock-01-1200" / "synthetic-evidence.json").write_text("tampered")
            self.assertFalse(verify(d)[0])
    def test_no_silent_replacement(self):
        with tempfile.TemporaryDirectory() as d:
            execute(d, ("mock-02", 200, "simulate"))
            self.assertTrue((Path(d) / "mock-02-200" / "attempt.json").exists())
            self.assertFalse(verify(d)[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)
