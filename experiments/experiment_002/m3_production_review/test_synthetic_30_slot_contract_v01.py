#!/usr/bin/env python3
"""Synthetic-only 30-slot registry contract; never imports scientific or seed generators."""
import json
import unittest

WINDOWS = (200, 600, 1200)
# Deliberately synthetic IDs: not evaluation seeds.
IDS = tuple(f"mock-{i:02d}" for i in range(10))

def validate(records):
    expected = {(s, w) for s in IDS for w in WINDOWS}
    observed = set()
    errors = []
    for r in records:
        key = (r.get("scenario"), r.get("window"))
        if key not in expected:
            errors.append("unknown scenario/window")
        if key in observed:
            errors.append("duplicate scenario/window")
        observed.add(key)
        if r.get("state") != "complete":
            errors.append("incomplete attempt")
        if not r.get("artifact_sha256") or len(r["artifact_sha256"]) != 64:
            errors.append("missing artifact digest")
        if r.get("source") != "synthetic":
            errors.append("non-synthetic source")
    if observed != expected:
        errors.append("missing expected scenarios")
    return not errors, errors

def fixture():
    return [{"scenario": s, "window": w, "state": "complete",
             "artifact_sha256": "a" * 64, "source": "synthetic"}
            for s in IDS for w in WINDOWS]

class TestRegistry(unittest.TestCase):
    def test_complete(self):
        self.assertTrue(validate(fixture())[0])
    def test_missing(self):
        self.assertFalse(validate(fixture()[:-1])[0])
    def test_duplicate(self):
        self.assertFalse(validate(fixture() + fixture()[:1])[0])
    def test_failure(self):
        a = fixture(); a[2]["state"] = "failed"
        self.assertFalse(validate(a)[0])
    def test_tamper(self):
        a = fixture(); a[0]["artifact_sha256"] = ""
        self.assertFalse(validate(a)[0])
    def test_unrecognized(self):
        a = fixture(); a[0]["scenario"] = "unapproved"
        self.assertFalse(validate(a)[0])
    def test_source(self):
        a = fixture(); a[0]["source"] = "real"
        self.assertFalse(validate(a)[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)
