#!/usr/bin/env python3
"""Fetch exactly the 120 prespecified archives from one immutable GitHub Actions run.

Paginate GitHub's REST API; verify inventory before downloading any archives.
Uses GITHUB_TOKEN; never regenerates or modifies scientific simulation data.
"""
import argparse,json,os,urllib.request,urllib.error,zipfile,io
from pathlib import Path
RUN_ID=41023721390
def request(url,token):
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=120) as response:return response.read()
def main():
    p=argparse.ArgumentParser();p.add_argument("--repository",required=True);p.add_argument("--out",required=True);p.add_argument("--run-id",type=int,default=RUN_ID)
    a=p.parse_args()
    if a.run_id!=RUN_ID:raise SystemExit("Source run must remain pinned")
    token=os.environ["GITHUB_TOKEN"];base=f"https://api.github.com/repos/{a.repository}/actions/runs/{RUN_ID}/artifacts"
    found=[];page=1
    while True:
        data=json.loads(request(f"{base}?per_page=100&page={page}",token))
        found.extend(data["artifacts"])
        if len(found)>=data["total_count"]:break
        if not data["artifacts"]:raise RuntimeError("Incomplete pagination")
        page+=1
    expected={f"exp004-seed-{seed}-window-{window}-arm-{arm}" for seed in range(3301,3311) for window in (200,600,1200) for arm in "ABCD"}
    selected=[x for x in found if x["name"] in expected]
    names=[x["name"] for x in selected]
    if len(found)!=len({x["id"] for x in found}) or len(selected)!=120 or set(names)!=expected or len(set(names))!=120:
        raise RuntimeError("Missing, duplicated or inconsistent artifact inventory")
    if any(x.get("expired") for x in selected):raise RuntimeError("Expired scenario artifact")
    root=Path(a.out);root.mkdir(parents=True,exist_ok=True)
    (root/"artifact-inventory.json").write_text(json.dumps({"source_run":RUN_ID,"total_artifacts":len(found),"scenarios":sorted(names)},indent=2)+"\n")
    for idx,art in enumerate(sorted(selected,key=lambda x:x["name"]),1):
        payload=request(f"https://api.github.com/repos/{a.repository}/actions/artifacts/{art['id']}/zip",token)
        folder=root/art["name"]
        folder.mkdir(exist_ok=False)
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            for member in archive.infolist():
                target=(folder/member.filename).resolve()
                if not target.is_relative_to(folder.resolve()):raise RuntimeError("Unsafe archive member")
            archive.extractall(folder)
        if not (folder/"attempt.json").is_file():raise RuntimeError("Missing attempt manifest "+art["name"])
        if idx%20==0:print(f"Downloaded {idx}/120 archives",flush=True)
    print("Verified and downloaded all 120 archived scenarios from run",RUN_ID)
if __name__=="__main__":main()
