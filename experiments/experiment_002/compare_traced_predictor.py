#!/usr/bin/env python3
"""Compare original time-aware predictor trace against SUMO observed chosen routes.

Only realized chosen traversals are compared, never unchosen candidate outcomes.
FCD samples are approximate edge entry and occupancy observations, not ground truth
for precise lane-to-lane junction or instantaneous occupancy measurements.
"""
import argparse, csv, json, math, statistics
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET

def stats(a):
    if not a:
        return dict(n=0, bias_s=None, mae_s=None, rmse_s=None, abs_p90_s=None, abs_p95_s=None)
    q=sorted(abs(x) for x in a)
    return dict(n=len(a),bias_s=round(statistics.mean(a),5),
                mae_s=round(statistics.mean(abs(x) for x in a),5),
                rmse_s=round(math.sqrt(statistics.mean(x*x for x in a)),5),
                abs_p90_s=round(q[math.ceil(.9*len(q))-1],5),
                abs_p95_s=round(q[math.ceil(.95*len(q))-1],5))

def load_csv(path):
    with open(path,newline='') as f: return list(csv.DictReader(f))

def fcd_tracks(path,bin_s):
    tracks=defaultdict(list);samples=Counter()
    excluded=total=0;gaps=Counter();prev=None
    for _,e in ET.iterparse(path,events=('end',)):
        if e.tag!='timestep':continue
        t=float(e.attrib['time'])
        if prev is not None:gaps[round(t-prev,3)]+=1
        prev=t
        for v in e.findall('vehicle'):
            lane=v.get('lane','')
            eid=lane.rsplit('_',1)[0]
            if not lane or eid.startswith(':'):
                excluded+=1;continue
            vid=v.attrib['id']
            if not tracks[vid] or tracks[vid][-1][0]!=eid:
                tracks[vid].append((eid,t))
            samples[(eid,int(t//bin_s))]+=1
            total+=1
        e.clear()
    return tracks,samples,dict(external_samples=total,internal_or_missing_lane_samples=excluded,timestep_gaps=dict(gaps))

def tripinfos(path):
    out={}
    for _,e in ET.iterparse(path,events=('end',)):
        if e.tag=='tripinfo':
            out[e.attrib['id']]=dict(arrival=float(e.attrib['arrival']),
              depart=float(e.attrib['depart']),duration=float(e.attrib['duration']),
              waiting=float(e.attrib.get('waitingTime',0)),
              depart_delay=float(e.attrib.get('departDelay',0)))
            e.clear()
    return out

def modeled_vehicle_seconds(rows,bin_s):
    out=defaultdict(float)
    for r in rows:
        start=float(r['predicted_entry_s']);end=float(r['predicted_exit_s'])
        if end<=start:raise RuntimeError('Nonpositive forecast interval for '+r['vehicle'])
        for b in range(int(start//bin_s),int((end-1e-9)//bin_s)+1):
            out[(r['edge'],b)]+=max(0.,min(end,(b+1)*bin_s)-max(start,b*bin_s))
    return out

def main():
    p=argparse.ArgumentParser()
    for name in ('trace','decision-trace','fcd','tripinfo','report','comparison','occupancy-comparison'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--bin-seconds',type=int,default=30)
    p.add_argument('--vehicles',type=int,default=1000)
    a=p.parse_args()
    if a.bin_seconds<=0:raise ValueError('bin_seconds must be positive')
    rows=load_csv(a.trace);decisions=load_csv(a.decision_trace)
    routes=defaultdict(list)
    for r in rows:routes[r['vehicle']].append(r)
    if len(decisions)!=a.vehicles or len(routes)!=a.vehicles:
        raise RuntimeError('Missing planned vehicles or decisions')
    for vid,items in routes.items():
        items.sort(key=lambda r:int(r['route_index']))
        if [int(r['route_index']) for r in items]!=list(range(len(items))):
            raise RuntimeError('Missing or duplicated edge indices: '+vid)
    tracks,observed_occupancy,fcd_meta=fcd_tracks(a.fcd,a.bin_seconds)
    arrivals=tripinfos(a.tripinfo)
    if len(arrivals)!=a.vehicles:raise RuntimeError('SUMO did not complete 1000 trips')
    errors=defaultdict(list);groups=defaultdict(lambda:defaultdict(list))
    results=[];bad_ids=[];matched=invalid_interval=0
    for vid,items in routes.items():
        observed=tracks.get(vid,[])
        if [r['edge'] for r in items]!=[e for e,t in observed]:
            bad_ids.append(vid)
            for r in items:
                results.append([vid,r['route_index'],r['edge'],'unmatched_route','','','','','','','','',''])
            continue
        scheduled=float(items[0]['predicted_entry_s'])
        depart_lag=arrivals[vid]['depart']-scheduled
        for i,r in enumerate(items):
            start=observed[i][1]
            finish=observed[i+1][1] if i+1<len(observed) else arrivals[vid]['arrival']
            if finish<start:
                invalid_interval+=1
                results.append([vid,i,r['edge'],'negative_observed_interval','','','','','','','','',''])
                continue
            model_entry=float(r['predicted_entry_s'])
            free_entry=float(r['freeflow_entry_s'])
            model_time=float(r['predicted_traversal_cost_s'])
            free_time=float(r['freeflow_s'])
            observed_time=finish-start
            ee=start-model_entry;ef=start-free_entry
            de=observed_time-model_time;df=observed_time-free_time
            for key,value in [('entry_timeaware',ee),('entry_freeflow',ef),
                              ('entry_timeaware_departure_aligned',ee-depart_lag),
                              ('entry_freeflow_departure_aligned',ef-depart_lag),
                              ('edge_to_next_edge_timeaware',de),
                              ('edge_to_next_edge_freeflow',df)]:
                errors[key].append(value)
            bucket='first_edge' if i==0 else 'edges_1_2' if i<=2 else 'edges_3_5' if i<=5 else 'edges_6_plus'
            groups[bucket]['timeaware_entry'].append(ee)
            groups[bucket]['freeflow_entry'].append(ef)
            n=int(r['prior_assigned_count'])
            load='assigned_0' if n==0 else 'assigned_1_2' if n<=2 else 'assigned_3_plus'
            groups[load]['timeaware_entry'].append(ee)
            results.append([vid,i,r['edge'],'matched',model_entry,start,finish,
                            model_time,observed_time,ee,ef,de,df])
            matched+=1
    with open(a.comparison,'w',newline='') as f:
        w=csv.writer(f);w.writerow(['vehicle','route_index','edge','match_status',
          'model_entry_s','observed_edge_first_sample_s','observed_next_edge_or_arrival_s',
          'model_edge_cost_s','observed_edge_to_next_edge_s',
          'entry_error_timeaware_s','entry_error_freeflow_s',
          'traversal_error_timeaware_s','traversal_error_freeflow_s']);w.writerows(results)
    forecast_occ=modeled_vehicle_seconds(rows,a.bin_seconds)
    keys=set(forecast_occ)|set(observed_occupancy)
    occ_errors=[]
    with open(a.occupancy_comparison,'w',newline='') as f:
        w=csv.writer(f);w.writerow(['edge','time_bin','model_path_interval_vehicle_seconds',
            'observed_external_fcd_sample_vehicle_seconds_approx','difference_observed_minus_model_s'])
        for key in sorted(keys):
            expected=forecast_occ.get(key,0.)
            actual=observed_occupancy.get(key,0)
            diff=actual-expected;occ_errors.append(diff)
            w.writerow([key[0],key[1],round(expected,5),actual,round(diff,5)])
    replay=[float(r['replay_minus_heap_s']) for r in decisions]
    report={
       'status':'diagnostic_smoke_not_validation_pass',
       'expected_vehicles':a.vehicles,'completed_vehicles':len(arrivals),
       'decisions':len(decisions),'route_changes':sum(int(r['route_changed']) for r in decisions),
       'guardrail_rejections':sum(r['decision_reason']=='detour_guardrail_rejected' for r in decisions),
       'predicted_traversals':len(rows),'matched_traversals':matched,
       'unmatched_route_vehicles':len(bad_ids),'unmatched_vehicle_ids_first20':bad_ids[:20],
       'invalid_observed_intervals':invalid_interval,
       'coverage_fraction':round(matched/len(rows),6) if rows else 0.,
       'forecast_error_seconds':{key:stats(val) for key,val in errors.items()},
       'search_heap_vs_route_replay_cost_seconds':stats(replay),
       'search_heap_vs_route_replay_nonzero_count':sum(abs(x)>1e-3 for x in replay),
       'breakdowns':{k:{name:stats(v) for name,v in metric.items()} for k,metric in sorted(groups.items())},
       'occupancy_diagnostic':{'bin_seconds':a.bin_seconds,'edge_bins':len(keys),
           'modeled_path_intervals_vs_fcd_sample_vehicle_seconds':stats(occ_errors),
           'this_is_not_original_search_occupancy_forecast':True},
       'fcd':fcd_meta,
       'mean_trip_duration_seconds':round(statistics.mean(v['duration'] for v in arrivals.values()),4),
       'mean_waiting_seconds':round(statistics.mean(v['waiting'] for v in arrivals.values()),4),
       'mean_departure_delay_seconds':round(statistics.mean(v['depart_delay'] for v in arrivals.values()),4),
       'limitations':[
        'Original routing occupancy counts prior assignments in a single free-flow entry bin per edge; this is NOT physical occupancy.',
        'Route edge-cost predictions are a replay of the ORIGINAL search equations along the chosen route with the pre-assignment counter. Search heap cost is reported separately because time-dependent bin decisions can make replay differ.',
        'FCD edge entry is first 1-second sample and observed edge-to-next-edge intervals include intersection/junction delay; neither is an exact physical traversal measurement.',
        'External-edge FCD counts omit internal lanes; occupancy vehicle-seconds derived from model intervals are NOT the original decision-time occupancy query.',
        'Unchosen candidate routes have no observed counterfactual outcomes.',
        'Free-flow reference is along the SAME chosen routes, not a separately simulated independent-routing arm.',
        'Development seed 2001 is exploratory and NOT a held-out evaluation seed.',
        'Observed departure lag can affect entry error; departure-aligned diagnostics subtract the tripinfo actual minus planned depart.',
        'Synthetic simulations cannot establish real-world traffic benefits or safety.'
       ]}
    with open(a.report,'w') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('breakdowns','fcd','limitations')},indent=2))
    if not rows or not matched:raise RuntimeError('No prediction/observation matches')
    if matched/len(rows)<.95:raise RuntimeError('Prediction match rate below 95%')

if __name__=='__main__':main()
