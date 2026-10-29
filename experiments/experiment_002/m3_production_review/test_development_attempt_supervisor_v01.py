#!/usr/bin/env python3
"""Offline integration tests of real subprocess failure archival, no SUMO."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from development_attempt_supervisor_v01 import execute

class TestSupervisor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.old = Path.cwd()
        os.chdir(self.tmp.name)
        self.addCleanup(os.chdir, self.old)
        Path("frozen/experiments/experiment_002").mkdir(parents=True)
        Path("frozen/experiments/experiment_002/time_aware.py").write_text("# fixture")
        Path("source").mkdir()
        Path("source/scenario.json").write_text(json.dumps({
            "seed": 2101, "window_seconds": 200, "no_holdout": True}))
    def test_failure_archives_real_partial_file_and_log(self):
        Path("failure.sh").write_text("#!/bin/sh\nmkdir -p results\necho partial > results/partial.txt\necho simulated-failure\nexit 42\n")
        a = execute("attempt", 2101, 200, "frozen", "source", "failure.sh")
        self.assertEqual(a["status"], "FAILED")
        self.assertEqual(a["returncode"], 42)
        self.assertTrue(Path("attempt/results/partial.txt").exists())
        self.assertIn("results/partial.txt", a["files"])
        self.assertIn("simulated-failure", Path("attempt/runner.log").read_text())
        self.assertEqual(json.loads(Path("attempt/attempt.json").read_text())["status"], "FAILED")
    def test_success_records_outputs(self):
        Path("success.sh").write_text("#!/bin/sh\nmkdir -p results\necho done > results/output.txt\n")
        a = execute("attempt", 2101, 200, "frozen", "source", "success.sh")
        self.assertEqual(a["status"], "COMPLETE")
        self.assertIn("results/output.txt", a["files"])
    def test_reserved_seed_blocked_before_filesystem_changes(self):
        with self.assertRaises(ValueError):
            execute("attempt", 3101, 200, "frozen", "source")
        self.assertFalse(Path("attempt").exists())
    def test_no_retry_overwrite(self):
        Path("failure.sh").write_text("#!/bin/sh\nexit 1\n")
        execute("attempt", 2101, 200, "frozen", "source", "failure.sh")
        with self.assertRaises(ValueError):
            execute("attempt", 2101, 200, "frozen", "source", "failure.sh")
    def test_wrong_provenance_blocked(self):
        with self.assertRaises(ValueError):
            execute("attempt", 2101, 600, "frozen", "source")
        self.assertFalse(Path("attempt").exists())

if __name__ == "__main__":
    unittest.main(verbosity=2)
