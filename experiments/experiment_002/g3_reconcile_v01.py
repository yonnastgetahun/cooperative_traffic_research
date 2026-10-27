#!/usr/bin/env python3
"""Offline G3 reconciliation: existing M2 development artifacts only; never SUMO or holdouts."""
import argparse,csv,io,json,math,statistics,zipfile,collections
import xml.etree.ElementTree as ET
from pathlib import Path

WINDOWS=(200,600,1200)
SEEDS=(2101,2102,2103)
EXPECTED={(s,w) for s in SEEDS for w in WINDOWS}

class Artifact:
    def __init__(self,path):self.path=Path(path)
    def read(self,name):
        if self.path.is_dir():return (self.path/name).read_bytes()
        with zipfile.ZipFile(self.path) as z:return z.read(name)
    def has(self,name):
        if self.path.is_dir():return (self.path/name).is_file()
        with zipfile.ZipFile(self.path) as z:return name in z.namelist()
    def csv(self,name):return list(csv.DictReader(io.StringIO(self.read(name).decode())))
    def json(self,name):return json.loads(self.read(name))

def discover(root):
    selected={}
    for path in sorted(Path(root).iterdir()):
        if not path.is_dir() and path.suffix!='.zip':continue
        src=Artifact(path)
        if not (src.has('scenario.json') and src.has('observed-edge-bins.csv')):continue
        data=src.json('scenario.json')
        key=(int(data['seed']),int(data['window_seconds']))
        if key not in EXPECTED:continue
        if key in selected:raise RuntimeError('Duplicate scenario '+str(key))
        if not data.get('no_holdout'):raise RuntimeError('Unexpected non-development seed')
        selected[key]=src
    if set(selected)!=EXPECTED:raise RuntimeError('Incomplete 3x3 artifacts '+str(sorted(EXPECTED-set(selected))))
    return selected

def parse_native_external(src):
    raw=ET.fromstring(src.read('native-external.xml'))
    vals={}
    for interval in raw.findall('interval'):
        begin=float(interval.get('begin'));end=float(interval.get('end'))
        for e in interval.findall('edge'):
            key=(e.get('id'),begin,end)
            if key in vals:raise RuntimeError('Repeated native road bin')
            vals[key]=float(e.get('sampledSeconds'))
    return vals

def phase_bounds(internal_sample_seconds,segment_seconds,cadence_verified=True):
    if internal_sample_seconds<0 or segment_seconds<0:raise ValueError('Negative phase duration')
    if not cadence_verified:return None,None,'cadence_gap'
    lower=max(0.,internal_sample_seconds-1.)
    upper=min(segment_seconds,internal_sample_seconds+1.)
    if lower>upper+1e-8:return None,None,'invalid_interval'
    return lower,upper,'bounded_sample_time_not_causal_delay'

def metrics(rows):
    if not rows:return dict(n=0,native_total=0,fcd_total=0,signed_difference=0,mae=None,p95_abs=None,max_abs=None,wape=None)
    diffs=sorted(abs(r['delta']) for r in rows)
    native_sum=sum(r['native'] for r in rows)
    return dict(n=len(rows),native_total=round(native_sum,4),
      fcd_total=round(sum(r['fcd'] for r in rows),4),
      signed_difference=round(sum(r['delta'] for r in rows),4),
      mae=round(statistics.mean(diffs),5),
      p95_abs=round(diffs[math.ceil(.95*len(diffs))-1],5),
      max_abs=round(diffs[-1],5),
      wape=round(sum(diffs)/native_sum,6) if native_sum else None)

def groups(r):
    n=r['native'];f=r['fcd'];names=['all']
    if n>0:names.append('native_positive')
    if n>=30:names.append('busy_native_ge30')
    if n>0 and f==0:names.append('native_positive_fcd_zero')
    if n==0 and f>0:names.append('native_zero_fcd_positive')
    if n==0 and f==0:names.append('both_zero')
    if 0<n<1:names.append('native_0_to_1')
    if 1<=n<5:names.append('native_1_to_5')
    if 5<=n<30:names.append('native_5_to_30')
    return names

def output_csv(path,items,fields):
    with open(path,'w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(items)

def analyze(root,out):
    inputs=discover(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    strata=[];outliers=[];junctions=[];integrity=[];images=set()
    groupnames=['all','native_positive','busy_native_ge30','native_positive_fcd_zero',
       'native_zero_fcd_positive','both_zero','native_0_to_1','native_1_to_5','native_5_to_30']
    for seed,window in sorted(inputs):
        src=inputs[(seed,window)]
        report=src.json('measurement-report.json')
        if report['completed_vehicles']!=1000 or report['matched_route_vehicles']!=1000:
            raise RuntimeError('Expected 1000 completed matched vehicles')
        if report['planned_edges']!=report['matched_external_segments']:
            raise RuntimeError('Unmatched planned route traversal')
        if 'Exact route and audit equality' not in src.read('policy-invariance.txt').decode():
            raise RuntimeError('No unmodified routing policy guarantee')
        image=src.read('container-image.txt').decode().strip()
        if not image.startswith('ghcr.io/eclipse-sumo/sumo@sha256:'):
            raise RuntimeError('Unpinned calibration image')
        images.add(image)
        decisions=src.csv('route-decisions.csv')
        proxy=src.csv('decision-count-proxy.csv')
        if len(decisions)!=1000 or len(proxy)!=report['planned_edges']:
            raise RuntimeError('Decision trace mismatch')
        cost_max=max(abs(float(r['replay_minus_heap_s'])) for r in decisions)
        if cost_max>.001:raise RuntimeError('Search heap vs path replay differ')
        if sum(r['method']=='origin_not_searched' for r in proxy)!=1000:
            raise RuntimeError('Origin is a replay sentinel, not a live search lookup')
        if any(float(r['model_capacity_proxy'])<=0 or int(r['prior_route_assignment_count'])<0 for r in proxy):
            raise RuntimeError('Invalid model count or capacity')
        native=parse_native_external(src);unseen=set(native)
        comparable=[];partial=0;partial_positive=0
        for row in src.csv('observed-edge-bins.csv'):
            if row['edge_type']!='external':continue
            key=(row['edge'],float(row['interval_begin_s']),float(row['interval_end_s']))
            if key not in native:raise RuntimeError('Unmatched native key '+str(key))
            unseen.discard(key)
            n=float(row['native_sampledSeconds'])
            if n<0:raise RuntimeError('Negative native sampledSeconds')
            if abs(n-native[key])>1e-4:
                raise RuntimeError('External-only and withInternal native outputs disagree')
            if row['bin_alignment']=='unmatched_bin':
                if key[2]-key[1]>=30:raise RuntimeError('Full-period bin missing FCD comparison')
                partial+=1
                if n>0:partial_positive+=1
                continue
            if row['bin_alignment']!='aligned':raise RuntimeError('Unknown bin status')
            f=float(row['fcd_vehicle_sample_seconds'])
            if f<0:raise RuntimeError('Negative observed sample vehicle seconds')
            comparable.append(dict(seed=seed,window=window,edge=row['edge'],
                begin=key[1],end=key[2],native=n,fcd=f,delta=round(f-n,5)))
        if unseen:raise RuntimeError('Unreported native external road bin')
        for g in groupnames:
            part=[r for r in comparable if g in groups(r)]
            strata.append(dict(seed=seed,window_seconds=window,stratum=g,**metrics(part)))
        for label,part in [('all_external',comparable),
              ('busy_native_ge30',[r for r in comparable if r['native']>=30])]:
            for rank,r in enumerate(sorted(part,key=lambda x:(-abs(x['delta']),x['edge'],x['begin']))[:20],1):
                outliers.append(dict(seed=seed,window_seconds=window,selection=label,
                    rank=rank,edge=r['edge'],interval_begin_s=r['begin'],interval_end_s=r['end'],
                    native_sampledSeconds=r['native'],fcd_sample_seconds=r['fcd'],
                    difference_fcd_minus_native_s=r['delta'],
                    classification='UNRESOLVED_NO_VERIFIED_VEHICLE_LEVEL_EXPLANATION',
                    artifact_source=src.path.name))
        phase_rows=src.csv('transition-phases.csv')
        max_idx=collections.defaultdict(lambda:-1)
        for row in phase_rows:
            vid=row['vehicle'];max_idx[vid]=max(max_idx[vid],int(row['route_index']))
        transitions=[r for r in phase_rows if int(r['route_index'])<max_idx[r['vehicle']]]
        if len(max_idx)!=1000 or len(phase_rows)!=report['planned_edges'] or len(transitions)!=len(phase_rows)-1000:
            raise RuntimeError('Route-index/phase join mismatch')
        lower=upper=stopped=internal=0.
        visible=absent=0
        for row in transitions:
            n=float(row['internal_sample_s']);span=float(row['external_to_next_s'])
            lo,hi,status=phase_bounds(n,span)
            if status!='bounded_sample_time_not_causal_delay':
                raise RuntimeError('Unbounded junction-phase uncertainty')
            lower+=lo;upper+=hi;internal+=n
            stopped+=float(row['external_stop_under_0_1_s'])
            visible+=int(n>0);absent+=int(n==0)
        junctions.append(dict(seed=seed,window_seconds=window,route_transitions=len(transitions),
            with_internal_samples=visible,without_internal_samples=absent,
            unsampled_internal_fraction=round(absent/len(transitions),6),
            sampled_internal_seconds=round(internal,3),
            stopped_external_sample_seconds=round(stopped,3),
            internal_lower_bound_seconds=round(lower,3),
            internal_upper_bound_seconds=round(upper,3),
            boundary_uncertainty_width_seconds=round(upper-lower,3),
            original_bookkeeping_unresolved_seconds=report['unresolved_transition_seconds']))
        integrity.append(dict(seed=seed,window_seconds=window,artifact_source=src.path.name,
            completed_vehicles=1000,matched_external_traversals=report['matched_external_segments'],
            native_external_bins=len(native),partial_native_uncompared_bins=partial,
            partial_native_positive_bins=partial_positive,
            live_original_search_expansions_recorded='NO_replay_only',
            replay_heap_max_absolute_seconds=round(cost_max,9),sumo_image=image))
    if len(images)!=1:raise RuntimeError('Image digest drift across 9 calibrations')
    output_csv(out/'g3-occupancy-strata.csv',strata,
      ['seed','window_seconds','stratum','n','native_total','fcd_total','signed_difference','mae','p95_abs','max_abs','wape'])
    output_csv(out/'g3-top-edge-bin-outliers.csv',outliers,
      ['seed','window_seconds','selection','rank','edge','interval_begin_s','interval_end_s','native_sampledSeconds','fcd_sample_seconds','difference_fcd_minus_native_s','classification','artifact_source'])
    output_csv(out/'g3-junction-uncertainty.csv',junctions,list(junctions[0]))
    output_csv(out/'g3-per-scenario.csv',integrity,list(integrity[0]))
    busy=collections.defaultdict(list)
    for r in strata:
        if r['stratum']=='busy_native_ge30':busy[r['window_seconds']].append(r)
    busy_summary={str(w):dict(n=sum(x['n'] for x in rows),
       wape=round(sum(x['wape']*x['native_total'] for x in rows)/sum(x['native_total'] for x in rows),6),
       maximum_absolute_bin_difference_s=max(x['max_abs'] for x in rows))
       for w,rows in sorted(busy.items())}
    result={
       'status':'G3_FIRST_PASS_COMPLETE_G3_STILL_OPEN',
       'original_actions_run':40446073958,'scenarios':9,'vehicles_completed':9000,
       'immutable_sumo_image':next(iter(images)),
       'seed_scope':list(SEEDS),'regimes':list(WINDOWS),
       'busy_road_discrepancies':busy_summary,
       'internal_sampled_transitions':sum(x['with_internal_samples'] for x in junctions),
       'transitions_missing_internal_samples':sum(x['without_internal_samples'] for x in junctions),
       'total_internal_lower_bound_s':round(sum(x['internal_lower_bound_seconds'] for x in junctions),3),
       'total_internal_upper_bound_s':round(sum(x['internal_upper_bound_seconds'] for x in junctions),3),
       'outliers_need_individual_vehicle_attribution':True,
       'native_partial_final_bins_not_silently_counted_as_zeros':True,
       'heldout_3101_to_3110_untouched':True,
       'decision_gates':{
         'G3-0_source_integrity':'PASS',
         'G3-1_occupancy_mechanisms':'OPEN',
         'G3-2_junction_sampling_bounds':'PARTIAL',
         'G3-3_live_search_time_lookup_capture':'OPEN',
         'G3-4_freeze_ready':'NO'}}
    (out/'g3-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# G3 — Offline reconciliation first-pass report','',
      '**Status: measurement diagnosis advanced, G3 remains OPEN; NO held-out validation.**','',
      '[Source M2 artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958#artifacts).',
      'Nine previously completed development-seed scenarios were processed. No new SUMO runs or route changes.','',
      '## Busy external roads (native sampledSeconds >= 30 per full 30-second bin)','',
      '| Window | Bins | Absolute disagreement / native sum | Largest edge-bin discrepancy |',
      '|---|---:|---:|---:|']
    for w,values in busy_summary.items():
        lines.append(f"| {w}s | {values['n']:,} | {values['wape']:.1%} | {values['maximum_absolute_bin_difference_s']:.1f} vehicle-seconds |")
    lines +=['','This is an **observational measurement mismatch**, not a proven SUMO error.',
      'Empty bins are reported separately; native partial last bins with unavailable aligned FCD are counted as incomparable, not set to zero.',
      '', '## Junction evidence','',
      f"{result['internal_sampled_transitions']:,} route transitions show internal-lane samples, and {result['transitions_missing_internal_samples']:,} do not.",
      f"Conservative 1-second **sample-based** internal dwell limits total {result['total_internal_lower_bound_s']:,.0f}–{result['total_internal_upper_bound_s']:,.0f} seconds.",
      'They do not isolate junction-caused delay; external approaches can contain queues. A previous zero unresolved-seconds value was bookkeeping, not perfect timing certainty.',
      '', '## Decision gates','',
      '| Gate | Status |','|---|---|']
    lines.extend(f"| {k} | {v} |" for k,v in result['decision_gates'].items())
    lines+=['','## Required next diagnostic work','',
      '1. Inspect outlier edge-bins against raw FCD vehicle IDs, lane positions, speed and network geometry before assigning a physical explanation.',
      '2. Investigate time-boundary/cross-edge vehicle-extent effects and compare occupied-bin errors; classify unresolved cases explicitly.',
      '3. To claim actual search-time occupancy lookup provenance, add non-policy-changing event capture or narrow the research claim to chosen-path replay.',
      '4. Revisit G3 only after a reconciled case ledger; **do not freeze M3 or touch evaluation seeds 3101–3110**.','',
      'Better forecast MAE on chosen routes does not imply better cooperative-routing outcomes.','']
    (out/'G3_RECONCILIATION_REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();analyze(args.root,args.out)

if __name__=='__main__':main()
