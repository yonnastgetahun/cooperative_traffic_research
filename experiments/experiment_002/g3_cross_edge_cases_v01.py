#!/usr/bin/env python3
"""G3-C case-level FCD audit of native-vs-front-position road-bin discrepancies.

"Front on next internal link, near its start" supports a cross-edge vehicle
extent explanation. It is NOT a per-vehicle native sampledSeconds attribution.
This script never runs SUMO or changes routes. It consumes existing M2 data.
"""
import argparse,collections,csv,io,json,zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SEEDS=(2101,2102,2103)
WINDOWS=(200,600,1200)
EXPECTED={(s,w) for s in SEEDS for w in WINDOWS}

def sources(root):
    found={}
    for path in sorted(Path(root).iterdir()):
        if not path.is_dir() and path.suffix!='.zip':continue
        if path.is_dir():
            p=path/'scenario.json'
            if not p.is_file():continue
            data=json.loads(p.read_bytes())
        else:
            with zipfile.ZipFile(path) as z:
                if 'scenario.json' not in z.namelist():continue
                data=json.loads(z.read('scenario.json'))
        key=(int(data['seed']),int(data['window_seconds']))
        if key not in EXPECTED:continue
        if key in found:raise RuntimeError('Duplicate M2 source '+str(key))
        found[key]=path
    if set(found)!=EXPECTED:raise RuntimeError('Need all nine preexisting development scenarios')
    return found

def timestep_iter(path):
    z=None
    if path.is_dir():f=open(path/'observed-fcd.xml','rb')
    else:
        z=zipfile.ZipFile(path);f=z.open('observed-fcd.xml')
    try:
        for _,node in ET.iterparse(f,events=('end',)):
            if node.tag!='timestep':continue
            yield node
            node.clear()
    finally:
        f.close()
        if z:z.close()

def audit(root,ledger,output,near_m=5.):
    targets=collections.defaultdict(dict)
    with open(ledger,newline='') as f:
        for row in csv.DictReader(f):
            key=(int(row['seed']),int(row['window_seconds']))
            if key not in EXPECTED:raise RuntimeError('Unknown seed/window in ledger')
            diff=float(row['difference_fcd_minus_native_s'])
            if diff>=0:continue
            eid=row['edge'];begin=int(float(row['interval_begin_s']))
            targets[key][(eid,begin)]=row
    rows=[]
    for key,path in sorted(sources(root).items()):
        starts=collections.defaultdict(set)
        for edge,begin in targets[key]:starts[begin].add(edge)
        last_external={}
        candidates=collections.defaultdict(lambda:{
            'internal_samples':0,'near':0,'stationary':0,'vehicle_ids':set(),
            'internal_lanes':set(),'min_pos':float('inf'),'front_external':0})
        for node in timestep_iter(path):
            sim_time=float(node.get('time'))
            begin=int(sim_time//30)*30
            for v in node.findall('vehicle'):
                lane=v.get('lane','');vid=v.get('id','')
                if not lane or not vid:continue
                edge=lane.rsplit('_',1)[0]
                if lane.startswith(':'):
                    preceding=last_external.get(vid)
                    if preceding not in starts.get(begin,set()):continue
                    item=candidates[(preceding,begin)]
                    item['internal_samples']+=1
                    item['vehicle_ids'].add(vid);item['internal_lanes'].add(lane)
                    pos=float(v.get('pos','inf'))
                    item['min_pos']=min(item['min_pos'],pos)
                    if pos<=near_m:item['near']+=1
                    if float(v.get('speed',100))<0.1:item['stationary']+=1
                else:
                    last_external[vid]=edge
                    if edge in starts.get(begin,set()):
                        candidates[(edge,begin)]['front_external']+=1
            node.clear()
        for (edge,begin),src in sorted(targets[key].items()):
            e=candidates[(edge,begin)]
            deficit=-float(src['difference_fcd_minus_native_s'])
            nearby=e['near']
            rows.append(dict(
               seed=key[0],window_seconds=key[1],edge=edge,begin_s=begin,
               native_sampled_seconds=src['native_sampledSeconds'],
               observed_front_edge_sample_seconds=src.get('fcd_sample_seconds',src.get('fcd_sample_vehicle_seconds')),
               native_minus_FCD_front_seconds=round(deficit,4),
               internal_front_after_preceding_edge_seconds=e['internal_samples'],
               internal_front_within_5m_of_start_seconds=nearby,
               internal_front_stopped_seconds=e['stationary'],
               deficit_minus_near_boundary_samples_s=round(deficit-nearby,4),
               example_vehicle_ids='|'.join(sorted(e['vehicle_ids'])[:6]),
               internal_example_lanes='|'.join(sorted(e['internal_lanes'])[:6]),
               minimum_internal_front_position_m='' if e['min_pos']==float('inf') else round(e['min_pos'],3),
               status='CONSISTENT_WITH_EDGE_BOUNDARY_OCCUPANCY_NOT_PROVEN' if nearby>0 else 'UNRESOLVED',
               original_artifact=path.name))
    if not rows:raise RuntimeError('No negative-difference bins selected')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with open(output,'w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    total=len(rows)
    supported=sum(int(x['internal_front_within_5m_of_start_seconds'])>0 for x in rows)
    close1=sum(abs(x['deficit_minus_near_boundary_samples_s'])<=1 for x in rows)
    close3=sum(abs(x['deficit_minus_near_boundary_samples_s'])<=3 for x in rows)
    example=next((r for r in rows if r['seed']==2103 and r['window_seconds']==200 and r['edge']=='C6C7' and r['begin_s']==60),None)
    summary={
        'status':'G3_CROSS_EDGE_PLAUSIBILITY_SUPPORTED_NOT_EXACT_NATIVE_RECONCILIATION',
        'input_m2_run':40446073958,'input_g3_run':40448102464,
        'selected_unique_negative_difference_bins':total,
        'with_downstream_internal_front_near_start':supported,
        'within_1_vehicle_second':close1,'within_3_vehicle_seconds':close3,
        'distance_heuristic_m':near_m,
        'selection':'union of highest-absolute and busy-road highest-absolute 20 bins per seed/window',
        'no_holdout_seeds':True,'no_sumo_rerun':True,
        'causal_limits':'FCD front lane vs native edgeData sampledSeconds can differ due interpolation and vehicle extent. Near-boundary samples are indicative, not a reconstructed native per-vehicle accounting. Vehicles can be longer or shorter than the 5m heuristic.',
        'illustrative_case':example,
        'sumo_documentation':['https://eclipse.dev/sumo/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html',
                              'https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html',
                              'https://github.com/eclipse-sumo/sumo/issues/16241']
    }
    summary_path=output.with_name('g3-cross-edge-summary.json')
    summary_path.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('illustrative_case','sumo_documentation','causal_limits')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',required=True)
    p.add_argument('--ledger',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args();audit(a.root,a.ledger,a.output)
