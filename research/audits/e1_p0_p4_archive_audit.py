#!/usr/bin/env python3
"""Read-only P0-P4 E1 source and original Stage 1D SUMO-archive audit.

Input: extracted original Actions artifact 13280496865 / original preserved release.
Run from repo root, after pip install lxml:
  python3 research/audits/e1_p0_p4_archive_audit.py --root evidence --out audit
No SUMO calls, no inference/training, no model edits or validation claims.
"""
import argparse,csv,gzip,hashlib,json,pathlib,statistics,subprocess,sys
from collections import Counter,defaultdict
from lxml import etree as ET

BUILD=tuple(range(5101,5107))
CHECK=tuple(range(5111,5115))
ARMS=('I','probe0','probe1','probe2','probe3','bundle')
PHYSICS_BLOB='0d446e2c52efd2b75adf351ad5d577f442a4ac29'
ADAPTER_BLOB='4ddc2034944354a1605bc798c8df1850e51ea897'

def hash_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def git_blob(path):
    data=pathlib.Path(path).read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def read_json(path):return json.loads(pathlib.Path(path).read_text())

def write_csv(path,rows):
    if not rows:return
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def read_edges(path,valid):
    out={}
    first=None;last=None;intervals=0
    with gzip.open(path,'rb') as g:
        for _,interval in ET.iterparse(g,events=('end',),tag='interval'):
            t=float(interval.get('begin'))
            first=t if first is None else min(first,t)
            last=float(interval.get('end'))
            intervals+=1
            for edge in interval:
                eid=edge.get('id')
                if eid in valid and edge.get('waitingTime') is not None:
                    out[(round(t,3),eid)]=(
                        float(edge.get('waitingTime')),
                        float(edge.get('entered','0')),
                        float(edge.get('sampledSeconds','0')))
            interval.clear()
            while interval.getprevious() is not None:
                del interval.getparent()[0]
    return out,{'first_s':first,'last_s':last,'five_second_windows':intervals,
                'nonempty_external_edge_windows':len(out)}

def original_ids(path):
    root=ET.parse(str(path)).getroot()
    ids=[x.get('id') for x in root.findall('tripinfo')]
    assert len(ids)==len(set(ids))==1000, str(path)
    return ids

def toy_fixtures():
    from research.externality_estimator import Link,Turn,Vehicle,Scenario,Parameters
    from research.externality_estimator.link_turn_queue import evolve
    result={}
    edges=tuple(Link(e,15,15,1,storage_vehicles=10) for e in ('A','B','X','Y'))
    persons=(Vehicle('vA',0,('A','B')),Vehicle('vX',0,('X','Y')))
    for q in (.35,.50,.65):
        variants={}
        for mode in ('shared_all_class','separately_stipulated_compatible_classes'):
            kinds=('all','all') if mode=='shared_all_class' else ('north','south')
            s=Scenario(edges,(Turn('A','B','J',kinds[0]),
                              Turn('X','Y','J',kinds[1])),persons)
            v=evolve(s,Parameters(q_sat=q))
            crossings={event.vehicle_id:event.tick for event in v.events if event.action=='cross'}
            variants[mode]=crossings
        assert len(set(variants['shared_all_class'].values()))==2
        assert len(set(variants['separately_stipulated_compatible_classes'].values()))==1
        result[str(q)]=variants
    return result

def run(root,out):
    root=pathlib.Path(root)
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    assert git_blob('research/externality_estimator/link_turn_queue.py')==PHYSICS_BLOB
    assert git_blob('research/externality_estimator/scenario_io.py')==ADAPTER_BLOB
    seeds=BUILD+CHECK
    p0=[];locks={};manifests={}
    for seed in seeds:
        d=root/('seed-'+str(seed))
        man=read_json(d/'scenario-manifest.json')
        lock=read_json(d/'prediction-lock.json')
        obs=read_json(d/'observations-summary.json')
        assert man['seed']==lock['seed']==obs['seed']==seed
        assert man['partition']==('DEV_BUILD' if seed in BUILD else 'DEV_CHECK')
        assert hash_file(d/'network.net.xml')==man['network_sha256']
        assert hash_file(d/'trips.xml')==man['demand_sha256']
        pred_files=lock['prediction_shas']
        assert len(pred_files)==(3 if seed in BUILD else 1)
        for name,expected in pred_files.items():
            assert hash_file(d/'predictions'/name)==expected
        ids_by_arm={}
        for arm in ARMS:
            assert hash_file(d/'routes'/(arm+'.rou.xml'))==man['arm_route_sha256'][arm]
            trip=d/'observations'/arm/'tripinfo.xml'
            assert hash_file(trip)==obs['observations'][arm]['tripinfo_sha256']
            ids_by_arm[arm]=set(original_ids(trip))
            for measure in ('edgeData','laneData'):
                assert (d/'observations'/arm/(measure+'.xml.gz')).is_file()
            p0.append({'seed':seed,'arm':arm,'partition':man['partition'],
                       'n_driver_ids':1000,'tripinfo_sha256':hash_file(trip)})
        assert all(ids_by_arm[a]==ids_by_arm['I'] for a in ARMS)
        locks[seed]=lock;manifests[seed]=man
    assert len(p0)==60
    net=ET.parse(str(root/'seed-5111'/'network.net.xml')).getroot()
    external={e.get('id'):e for e in net.findall('edge') if e.get('function')!='internal' and not e.get('id','').startswith(':')}
    junctions=[j for j in net.findall('junction') if j.get('type')=='priority']
    conns=net.findall('connection')
    legal={(c.get('from'),c.get('to')) for c in conns if c.get('from') in external and c.get('to') in external}
    p1={'external_edges':len(external),'external_lane_count_distribution':
        dict(Counter(len(e.findall('lane')) for e in external.values())),
        'priority_junctions':len(junctions),
        'internal_junctions':sum(j.get('type')=='internal' for j in net.findall('junction')),
        'legal_external_edge_turns':len(legal),
        'raw_connection_rows':len(conns),
        'request_records':sum(len(j.findall('request')) for j in junctions),
        'junctions_with_nonzero_foe_bits':
            sum(any('1' in r.get('foes','') for r in j.findall('request')) for j in junctions),
        'foe_index_to_turn_mapping':'not independently verified',
        'E1_conflict_group':'all turns share all at each priority junction'}
    assert p1['external_edges']==360 and p1['priority_junctions']==100
    assert p1['external_lane_count_distribution']=={1:360}

    coverage=[];contrasts=[];hotspots=[];bundles=[]
    for seed in CHECK:
        d=root/('seed-'+str(seed))/'observations'
        data={}
        for arm in ARMS:
            dat,cov=read_edges(d/arm/'edgeData.xml.gz',set(external))
            data[arm]=dat
            coverage.append(dict(seed=seed,arm=arm,**cov))
        baseline=data['I']
        byarm={}
        for arm in ARMS[1:]:
            edges=defaultdict(float)
            abs_time=defaultdict(float)
            for key in set(baseline)|set(data[arm]):
                delta=data[arm].get(key,(0,0,0))[0]-baseline.get(key,(0,0,0))[0]
                edges[key[1]]+=delta
                abs_time[key[1]]+=abs(delta)
            signed=sum(edges.values())
            byarm[arm]=signed
            contrasts.append(dict(seed=seed,arm=arm,
               external_edge_waiting_delta_vehicle_s=round(signed,3),
               edges_gt10_extra_waiting=sum(v>10 for v in edges.values()),
               edges_gt10_less_waiting=sum(v < -10 for v in edges.values())))
            for edge in sorted(edges,key=lambda e:abs(edges[e]),reverse=True)[:10]:
                hotspots.append(dict(seed=seed,arm=arm,edge=edge,
                   signed_waiting_delta_vehicle_s=round(edges[edge],3),
                   abs_timebin_waiting_delta_vehicle_s=round(abs_time[edge],3)))
        targets=set(manifests[seed]['bundle_target_ids'])
        matched=[('probe'+str(i)) for i,p in enumerate(manifests[seed]['probes']) if p['target_vehicle_id'] in targets]
        assert len(matched)==2
        a,b=matched
        interaction={}
        for key in set().union(data['I'],data[a],data[b],data['bundle']):
            interaction[key]=(
                data['bundle'].get(key,(0,0,0))[0]-data[a].get(key,(0,0,0))[0]
                -data[b].get(key,(0,0,0))[0]+baseline.get(key,(0,0,0))[0])
        labels=read_json(root/('seed-'+str(seed))/'observations-summary.json')['observations']
        totals={arm:labels[arm]['network_total_s'] for arm in ('I',a,b,'bundle')}
        bundles.append(dict(seed=seed,probe_a=a,probe_b=b,
          network_elapsed_interaction_s=round(totals['bundle']-totals[a]-totals[b]+totals['I'],3),
          external_edge_waiting_interaction_vehicle_s=round(sum(interaction.values()),3),
          absolute_edge_time_waiting_interaction_vehicle_s=round(sum(abs(v) for v in interaction.values()),3)))
    qcases=[]
    for seed in BUILD:
        d=root/('seed-'+str(seed))/'predictions'
        vals={q:read_json(d/('E1-q-'+format(q,'.2f')+'.json')) for q in (.35,.50,.65)}
        for i,arm in enumerate(ARMS[1:]):
            rows={q:vals[q]['rows'][i] for q in vals}
            assert all(rows[q]['arm']==arm for q in rows)
            qcases.append(dict(seed=seed,arm=arm,
              q035_external_network_s=rows[.35]['pred_external_delta_network_s'],
              q050_external_network_s=rows[.50]['pred_external_delta_network_s'],
              q065_external_network_s=rows[.65]['pred_external_delta_network_s'],
              q050_equals_q065_complete_1000_driver_vectors=(
                rows[.50]['per_driver_baseline_s']==rows[.65]['per_driver_baseline_s']
                and rows[.50]['per_driver_swap_s']==rows[.65]['per_driver_swap_s'])))
    assert len(qcases)==30
    assert all(x['q050_equals_q065_complete_1000_driver_vectors'] for x in qcases)
    fixtures=toy_fixtures()
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-q','research/externality_estimator/tests'],
                         capture_output=True,text=True)
    assert tests.returncode==0,tests.stdout+tests.stderr
    summary={'status':'P0-P4_READ_ONLY_MECHANISM_INVESTIGATION_COMPLETE',
      'original_Stage1D':'DEVELOPMENT_NOT_QUALIFIED','validation':'NOT_STARTED','Test_B':'NOT_RUN',
      'P0':{'scenario_arms':len(p0),'driver_records':len(p0)*1000,
            'prediction_locks':len(locks),'prediction_files':sum(len(x['prediction_shas']) for x in locks.values()),
            'edge_files':60,'lane_files':60,'FCD_files':0},
      'P1':p1,
      'P2':{'development_check_seeds':list(CHECK),'arms':len(coverage),
            'same_seed_comparisons':len(contrasts),'bundle_interactions':bundles},
      'P3':{'frozen_source_unit_tests':'21 PASS','toy_conflict_crossings':fixtures,
            'q050_q065_same_predicted_driver_vectors':sum(x['q050_equals_q065_complete_1000_driver_vectors'] for x in qcases),
            'n_comparisons':len(qcases)},
      'P4':{'H1':'SOURCE LIMITATION VERIFIED, causal effect not isolated',
             'H2':'ONE EXTERNAL LANE PER LINK, multilane mechanism inapplicable',
             'H3':'NO FCD, vehicle-level entry clocks insufficient',
             'H4':'NONADDITIVE BUNDLES AND WAITING REARRANGEMENT OBSERVED, unique cause not identified',
             'H5':'0.50/0.65 PREDICTION INSENSITIVITY VERIFIED, binding constraint not identified'}}
    for name,rows in [('integrity_60_arms.csv',p0),('edge_detector_24_arms.csv',coverage),
                      ('external_edge_waiting_contrasts.csv',contrasts),
                      ('top_external_waiting_edges.csv',hotspots),
                      ('bundle_detector_interactions.csv',bundles),
                      ('devbuild_parameter_sensitivity.csv',qcases)]:
        write_csv(out/name,rows)
    (out/'p0_p4_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'status':summary['status'],'P0':summary['P0'],
        'P1':summary['P1'],'P2_bundle':bundles,'P3':summary['P3']['n_comparisons']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',required=True)
    p.add_argument('--out',required=True)
    a=p.parse_args()
    run(a.root,a.out)
