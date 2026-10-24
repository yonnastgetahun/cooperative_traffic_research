import os, random, csv, statistics, subprocess, xml.etree.ElementTree as ET, sys
sys.path.insert(0,os.path.join(os.environ.get('SUMO_HOME','/usr/share/sumo'),'tools'))
import sumolib
net='results/network.net.xml'
random.seed(1001)
network=sumolib.net.readNet(net)
edges=[e for e in network.getEdges() if not e.isSpecial() and e.allows('passenger')]
root=ET.Element('trips')
for i in range(1000):
    for _ in range(1000):
        a,b=random.sample(edges,2)
        p,_=network.getShortestPath(a,b,vClass='passenger')
        if p and len(p)>=2:break
    else:raise RuntimeError('Disconnected trip')
    ET.SubElement(root,'trip',id=f'veh{i:04d}',depart=f'{i*.2:.3f}',**{'from':a.getID(),'to':b.getID()})
ET.ElementTree(root).write('results/trips.xml')
subprocess.run(['duarouter','-n',net,'-r','results/trips.xml','-o','results/independent.rou.xml','--seed','1001','--no-step-log','true'],check=True)
subprocess.run(['python3','experiments/experiment_002/cooperative.py','--net',net,'--trips','results/trips.xml','--out','results/cooperative.rou.xml','--metrics','results/algorithm.json','--penalty','0.02'],check=True)
routes={}
trips={}
for arm in ('independent','cooperative'):
    routes[arm]={v.get('id'):v.find('route').get('edges').split() for v in ET.parse(f'results/{arm}.rou.xml').getroot().findall('vehicle')}
    subprocess.run(['sumo','-n',net,'-r',f'results/{arm}.rou.xml','--tripinfo-output',f'results/{arm}-tripinfo.xml','--seed','1001','--no-step-log','true'],check=True)
    trips[arm]={t.get('id'):t for t in ET.parse(f'results/{arm}-tripinfo.xml').getroot().findall('tripinfo')}
with open('results/vehicle-diagnostics.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['vehicle','route_changed','duration_independent_s','duration_cooperative_s','duration_delta_s','waiting_delta_s','edge_count_delta'])
    for i in sorted(set(trips['independent'])&set(trips['cooperative'])):
        a,b=trips['independent'][i],trips['cooperative'][i]
        w.writerow([i,routes['independent'][i]!=routes['cooperative'][i],a.get('duration'),b.get('duration'),float(b.get('duration'))-float(a.get('duration')),float(b.get('waitingTime'))-float(a.get('waitingTime')),len(routes['cooperative'][i])-len(routes['independent'][i])])
from collections import Counter
a=Counter(e for p in routes['independent'].values() for e in p)
b=Counter(e for p in routes['cooperative'].values() for e in p)
with open('results/edge-assignment.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['edge','baseline_assignments','cooperative_assignments','difference'])
    for e in sorted(set(a)|set(b)):w.writerow([e,a[e],b[e],b[e]-a[e]])
