#!/usr/bin/env python3
"""Publish the approved full Experiment 007 investigation update to X with four verified graphics.
Fail closed: never publish text alone, never retry a post with ambiguous status.
"""
import io, os, hashlib
from pathlib import Path
import requests
from PIL import Image
from requests_oauthlib import OAuth1Session

CAPTION=Path("social/experiment007/complete-investigation-x-draft.txt")
LANDING="https://github.com/yonnastgetahun/cooperative_traffic_research/blob/main/docs/RESEARCH_UPDATE_EXP007_COMPLETE_INVESTIGATION_2026-11-02.md"
SOURCES=[
 ("https://at.adobe.com/Kyp904qCv28brsq1","5e52e7a14308d209b5651658e95100eba070835c751b2c5f2d3f4b0ec62628e4"),
 ("https://at.adobe.com/5rTHskKV0MyIaUGc","94f8e465b27277f34ba27e737b1f3edf1e28cd28cf1297d0f4b41ebb66fab297"),
 ("https://at.adobe.com/dFKoLlRwUCaCuq0P","4e1e1f3601abb1f1978498114f05b228a9bb4901ddcee6b9cfb4760f146a1ee6"),
 ("https://at.adobe.com/lKb9VdASofazoW9d","8b2297bde78c530e16e54c9f5eba9f8b4326989007f4bf8ad1333673fc07cb94"),
]
TAGS="#AI #BuildInPublic #AIResearch #AIStartups #MultiAgentSystems #ProductManagement #OpenSource"

def approved_caption():
    text=CAPTION.read_text(encoding="utf-8").strip()
    assert text.count(LANDING)==1,"Single landing page must be preserved"
    assert TAGS in text,"All seven approved hashtags must remain"
    assert text.count("https://")==1,"No extra URLs or threads"
    # X shortens the only link, counted as 23 characters on standard accounts.
    effective=len(text)-len(LANDING)+23
    if effective>280:raise RuntimeError("Effective X post length exceeds standard limit: "+str(effective))
    print("Approved caption: %d raw, ~%d effective characters"%(len(text),effective))
    return text

def fetch_images():
    blobs=[]
    for i,(url,sha) in enumerate(SOURCES,1):
        response=requests.get(url,timeout=55,allow_redirects=True)
        response.raise_for_status()
        data=response.content
        if hashlib.sha256(data).hexdigest()!=sha:
            raise RuntimeError("Slide %d bytes differ from user-approved media; NO POST"%i)
        with Image.open(io.BytesIO(data)) as im:
            if im.format!="PNG" or im.size!=(1200,675):
                raise RuntimeError("Slide %d is not approved 1200x675 PNG"%i)
            im.verify()
        blobs.append(data)
        print("Verified approved image %d/4, %d bytes"%(i,len(data)))
    if len(blobs)!=4:raise RuntimeError("Exactly four images required")
    return blobs

def main():
    text=approved_caption()
    images=fetch_images()
    secret_names=("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    if any(not os.getenv(n) for n in secret_names):
        raise SystemExit("Existing X API credentials unavailable; no post attempted")
    session=OAuth1Session(os.environ["X_API_KEY"],client_secret=os.environ["X_API_SECRET"],
       resource_owner_key=os.environ["X_ACCESS_TOKEN"],
       resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    media=[]
    for i,blob in enumerate(images,1):
        resp=session.post("https://upload.twitter.com/1.1/media/upload.json",
          files={"media":("experiment007-%02d.png"%i,blob,"image/png")},timeout=60)
        if not resp.ok:raise SystemExit("Image upload %d HTTP %s; NO POST"%(i,resp.status_code))
        mid=resp.json().get("media_id_string")
        if not mid:raise SystemExit("No media ID for slide %d; NO POST"%i)
        media.append(mid)
        print("Uploaded image %d/4 to X media endpoint"%i)
    if len(media)!=4:raise SystemExit("Refusing text-only or incomplete-media post")
    resp=session.post("https://api.x.com/2/tweets",json={"text":text,"media":{"media_ids":media}},timeout=60)
    if not resp.ok:raise SystemExit("X post API HTTP %s: %s"%(resp.status_code,resp.text[:500]))
    data=resp.json().get("data",{})
    tweet_id=data.get("id")
    if not tweet_id:raise SystemExit("X returned no ID. Publication ambiguous, DO NOT RETRY blindly")
    print("CREATED_POST_ID="+str(tweet_id))
    print("POST_URL=https://x.com/yonnastgetahun/status/"+str(tweet_id))
    try:
        check=session.get("https://api.x.com/2/tweets/"+str(tweet_id),
           params={"tweet.fields":"attachments","expansions":"attachments.media_keys","media.fields":"type"},timeout=45)
        if not check.ok:raise RuntimeError("GET HTTP "+str(check.status_code))
        attached=check.json().get("data",{}).get("attachments",{}).get("media_keys",[])
        if len(attached)!=4:
            raise RuntimeError("Expected 4 media keys, returned "+str(len(attached)))
        print("VERIFIED_PUBLISHED_WITH_ALL_4_MEDIA_KEYS="+str(tweet_id))
    except Exception as ex:
        # Post already exists; report unverified without duplicate.
        raise SystemExit("POST CREATED but media readback NOT VERIFIED: "+str(ex)+". Do not auto-retry.")
if __name__=="__main__":main()
