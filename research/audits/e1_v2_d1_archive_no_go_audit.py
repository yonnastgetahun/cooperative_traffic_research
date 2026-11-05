#!/usr/bin/env python3
"""Read-only E1-v2 D1 frozen-archive re-audit. No SUMO, no source edits.

Run from a repository checkout:
  python3 research/audits/e1_v2_d1_archive_no_go_audit.py \
    --zip exp007-e1v2-d1-original-frozen-60arm-evidence.zip --out audit

Input: GitHub Actions run 41966516110 artifact 13387764476.
"""
import argparse,csv,hashlib,io,json,pathlib,statistics,zipfile
import xml.etree.ElementTree as ET

SEEDS=tuple(range(6101,6107))+tuple(range(6111,6115))
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
KEYS={"B0":"B0_external_network_s","B1":"B1_external_network_s",
      "E1v1":"E1v1_external_network_s","E1v2":"E1v2_external_network_s"}

def sha(data):return hashlib.sha256(data).hexdigest()
def j(z,key):return json.loads(z.read(key))
def rows(z,key):return list(csv.DictReader(io.StringIO(z.read(key).decode("utf-8"))))
def main(z,out):
    names=z.namelist()
    assert len(names)==695, "Original archive member count differs"
    verdict=j(z,"development-verdict.json")
    locks=j(z,"all-prediction-locks.json")
    assert locks["status"]=="FROZEN_BEFORE_ANY_SUMO_OUTCOME"
    assert locks["locked_seeds"]==list(SEEDS)
    assert verdict["scientific_status"]=="DEVELOPMENT_NOT_QUALIFIED"
    assert verdict["new_validation"]=="NOT_STARTED" and verdict["Test_B"]=="NOT_RUN"
    source=[];records=0;predrows=0
    for seed in SEEDS:
        pre=f"seed-{seed}/"
        man=j(z,pre+"scenario-manifest.json")
        lock=j(z,pre+"prediction-lock.json")
        obs=j(z,pre+"observations-summary.json")["observations"]
        assert man["seed"]==seed==lock["seed"]
        assert man["partition"]==("DEV_BUILD" if seed<6110 else "DEV_CHECK")
        assert sha(z.read(pre+"network.net.xml"))==man["network_sha256"]
        assert sha(z.read(pre+"trips.xml"))==man["demand_sha256"]
        pred=z.read(pre+"predictions/predictions.json")
        assert sha(pred)==lock["prediction_sha256"]
        predj=json.loads(pred)
        assert predj["observed_outcomes_used"] is False
        assert len(predj["rows"])==5
        predrows+=len(predj["rows"])
        for arm in ARMS:
            assert sha(z.read(pre+f"routes/{arm}.rou.xml"))==man["arm_route_sha256"][arm]
            xml=z.read(pre+f"observations/{arm}/tripinfo.xml")
            assert sha(xml)==obs[arm]["tripinfo_sha256"]
            ids=[x.get("id") for x in ET.fromstring(xml).findall("tripinfo")]
            assert len(ids)==len(set(ids))==1000
            records+=1000
        source.append(dict(seed=seed,partition=man["partition"],
             network_sha256=man["network_sha256"],demand_sha256=man["demand_sha256"],
             prediction_sha256=lock["prediction_sha256"],SUMO_arms=6,matched_tripinfo_ids=6000))
    assert records==60000 and predrows==50
    check=rows(z,"check-singleton-effects.csv")
    assert len(check)==16
    result={}
    for name,key in KEYS.items():
        byseed={seed:statistics.mean(abs(float(row[key])-float(row["observed_external_network_s"]))
                    for row in check if int(row["seed"])==seed)
                for seed in range(6111,6115)}
        result[name]=statistics.mean(byseed.values())
        assert all(abs(byseed[seed]-verdict["check_seed_MAE"][str(seed)][name])<1e-8
                   for seed in byseed)
        assert abs(result[name]-verdict["mean_seed_externality_MAE_network_s"][name])<1e-8
    assert sum(int(r["E1v2_sign_match_material"]) for r in check)==5
    assert sum(int(r["E1v2_predicted_benefit_realized_harm_gt30_network_s"]) for r in check)==0
    assert result["E1v2"]>min(result[n] for n in ("B0","B1","E1v1"))
    out.mkdir(parents=True,exist_ok=True)
    with (out/"source_sha_checks.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(source[0]));w.writeheader();w.writerows(source)
    with (out/"devcheck_seed_mae.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["seed"]+list(KEYS))
        for seed in range(6111,6115):
            w.writerow([seed]+[verdict["check_seed_MAE"][str(seed)][k] for k in KEYS])
        w.writerow(["MEAN"]+[result[k] for k in KEYS])
    (out/"archive_audit_summary.json").write_text(json.dumps({
        "verdict":"DEVELOPMENT_NOT_QUALIFIED","zip_members":695,"SUMO_arms":60,
        "tripinfo_records":records,"prediction_locks":10,"prediction_rows":predrows,
        "MAE_network_seconds":result,"correct_signs":5,"material_probes":16,
        "severe_false_benefits":0,"independent_validation":"NOT_STARTED","Test_B":"NOT_RUN"
    },indent=2)+"\n")
    print("PASS: 60 archived SUMO arms, 60000 matched IDs, 10 locks, 50 predictions; scientific NO-GO retained")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True);p.add_argument("--out",required=True)
    args=p.parse_args()
    with zipfile.ZipFile(args.zip) as z:main(z,pathlib.Path(args.out))
