"""Parse STATIC SUMO network/routes/demand XML as predecision announced input.

Uses only Python's standard XML parser, not SUMO simulation or observed labels.
The conservative per-junction conflict-group approximation is explicitly
labeled and must be reviewed before development simulations.
"""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path
from .schema import InvalidScenario, Link, Scenario, Turn, Vehicle


def from_sumo_static_xml(net_file: str | Path, trips_file: str | Path,
                         routes_file: str | Path, partition: str = "HISTORICAL_DIAG_ONLY") -> Scenario:
    net=ET.parse(net_file).getroot()
    links=[]
    link_junction={}
    for edge in net.findall('edge'):
        if edge.get('function')=='internal' or edge.get('id','').startswith(':'):
            continue
        lanes=edge.findall('lane')
        if not lanes:
            continue
        lengths=[float(l.get('length')) for l in lanes]
        speeds=[float(l.get('speed')) for l in lanes]
        if max(lengths)-min(lengths)>0.02 or max(speeds)-min(speeds)>0.02:
            raise InvalidScenario('Heterogeneous lane length/speed unsupported in E1 static intake')
        eid=edge.get('id')
        links.append(Link(eid,lengths[0],speeds[0],lanes=len(lanes)))
        link_junction[eid]=edge.get('to')
    legal={}
    for connection in net.findall('connection'):
        a=connection.get('from');b=connection.get('to')
        if a not in link_junction or b not in link_junction:
            continue
        if not link_junction[a]:
            raise InvalidScenario('Missing junction mapping for edge connection')
        key=(a,b)
        # Count unique from-lane to-lane pairs conservatively; effective
        # lanes limited to source edge lane count. This is not a signal model.
        legal.setdefault(key,set()).add((connection.get('fromLane'),connection.get('toLane')))
    lanes_by={x.edge_id:x.lanes for x in links}
    turns=tuple(Turn(a,b,link_junction[a],conflict_class='all',
                     effective_lanes=min(lanes_by[a],len(lane_pairs)))
                for (a,b),lane_pairs in sorted(legal.items()))
    demands={}
    for trip in ET.parse(trips_file).getroot().findall('trip'):
        vid=trip.get('id')
        if not vid or vid in demands:
            raise InvalidScenario('Duplicate/missing announced demand driver ID')
        demands[vid]=(float(trip.get('depart')),trip.get('from'),trip.get('to'))
    vehicles=[]
    for row in ET.parse(routes_file).getroot().findall('vehicle'):
        vid=row.get('id')
        route=row.find('route')
        if vid not in demands or route is None or not route.get('edges'):
            raise InvalidScenario('Vehicle route and demand cannot reconcile')
        scheduled,source,destination=demands[vid]
        declared=float(row.get('depart'))
        if abs(declared-scheduled)>.001:
            raise InvalidScenario('Original route departure differs from frozen announced demand')
        seq=tuple(route.get('edges').split())
        if seq[0]!=source or seq[-1]!=destination:
            raise InvalidScenario('Route OD endpoints do not match frozen demand')
        if not (vid.startswith('veh') and vid[3:].isdigit()):
            raise InvalidScenario('Unknown eligibility roster; no invented opt-in')
        eligible=int(vid[3:])%2==0
        # Explicit *prior* rather than pretending individual SUMO's actual
        # stochastic speed factor was a predecision observation.
        speed_factor=float(row.get('speedFactor','1'))
        vehicles.append(Vehicle(vid,scheduled,seq,eligible,speed_factor))
    if set(demands)!={v.vehicle_id for v in vehicles}:
        raise InvalidScenario('Announced demand/vehicle route IDs mismatch')
    return Scenario(tuple(links),turns,tuple(vehicles),label_partition=partition)
