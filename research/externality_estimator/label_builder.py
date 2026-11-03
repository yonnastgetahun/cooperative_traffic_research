"""OFFLINE ONLY. SUMO tripinfo labels, deliberately not importable by predictor."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path


def label_from_tripinfo(path: str | Path, scheduled: dict[str,int]) -> dict[str,float]:
    values={}
    for node in ET.parse(path).getroot().findall('tripinfo'):
        vid=node.attrib['id']
        actual_depart=float(node.attrib['depart'])
        duration=float(node.attrib['duration'])
        arrival=float(node.attrib.get('arrival',str(actual_depart+duration)))
        if abs(actual_depart+duration-arrival)>.021:
            raise ValueError("SUMO tripinfo departure/arrival inconsistency")
        if vid not in scheduled or vid in values:
            raise ValueError("Unknown or duplicated SUMO ID")
        values[vid]=arrival-scheduled[vid]
    if set(values)!=set(scheduled):
        raise ValueError("Missing completed trip IDs: cannot claim all-network outcome")
    return values
