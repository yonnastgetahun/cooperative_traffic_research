#!/usr/bin/env python3
"""Experiment 003–006 X update with four image uploads; fail closed on any media error."""
import io
import os
from pathlib import Path
import requests
from PIL import Image
from requests_oauthlib import OAuth1Session

POST = Path("social/experiment005006-x-post.txt")
IMAGE_URLS = [
    "https://at.adobe.com/DAybRueBKSJU3kn7",  # Experiment 003
    "https://at.adobe.com/iyyF0UMq7mDqCz7F", # Experiment 004
    "https://at.adobe.com/9nD7Y5VcNTGyH13N", # Experiment 005
    "https://at.adobe.com/UPD7UaACmedvjv7I",# Experiment 006
]

def fetch_images():
    images=[]
    for i, url in enumerate(IMAGE_URLS, 1):
        response=requests.get(url,timeout=45,allow_redirects=True)
        response.raise_for_status()
        data=response.content
        if len(data)<10000 or len(data)>5_000_000:
            raise RuntimeError("Image %d invalid content size: %d" % (i,len(data)))
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        with Image.open(io.BytesIO(data)) as im:
            if im.format!="PNG" or im.width<800 or im.height<600:
                raise RuntimeError("Image %d invalid format/dimensions" % i)
            print("Validated slide %d: %dx%d; %d bytes" % (i,im.width,im.height,len(data)))
        images.append(data)
    if len(images)!=4:
        raise RuntimeError("All four image assets required")
    return images

def main():
    text=POST.read_text(encoding="utf-8").strip()
    if not 1<=len(text)<=280 or "RESEARCH_UPDATE_EXPERIMENTS_003_TO_006.md" not in text:
        raise SystemExit("X copy or sole landing page does not match approved post")
    images=fetch_images()  # mandatory: do not create a tweet if any visual cannot be fetched
    names=("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    if any(not os.environ.get(n) for n in names):
        raise SystemExit("Existing X OAuth secrets unavailable; no post attempted")
    session=OAuth1Session(
        os.environ["X_API_KEY"],client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    media_ids=[]
    for i,data in enumerate(images,1):
        result=session.post("https://upload.twitter.com/1.1/media/upload.json",
            files={"media":("experiment-%03d.png" % (i+2),data,"image/png")},timeout=60)
        if not result.ok:
            raise SystemExit("Image %d upload failed, HTTP %s; NO POST" % (i,result.status_code))
        media_id=result.json().get("media_id_string")
        if not media_id:
            raise SystemExit("Image %d has no media_id; NO POST" % i)
        media_ids.append(media_id)
        print("Uploaded image %d/4" % i)
    if len(media_ids)!=4:
        raise SystemExit("Refusing X post without all four media IDs")
    result=session.post("https://api.x.com/2/tweets",
        json={"text":text,"media":{"media_ids":media_ids}},timeout=45)
    if not result.ok:
        raise SystemExit("X post failed HTTP %d: %s" %(result.status_code,result.text[:200]))
    tweet_id=result.json().get("data",{}).get("id")
    if not tweet_id:
        raise SystemExit("X API returned no tweet ID; verify remotely before retry")
    print("Published four-image post: https://x.com/yonnastgetahun/status/"+str(tweet_id))

if __name__=="__main__":
    main()
