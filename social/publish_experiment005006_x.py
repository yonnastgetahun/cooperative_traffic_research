#!/usr/bin/env python3
"""One-time vetted Experiment 005/006 X publication via existing OAuth connection."""
import os
from pathlib import Path
from requests_oauthlib import OAuth1Session

POST=Path("social/experiment005006-x-post.txt")

def main():
    text=POST.read_text(encoding="utf-8").strip()
    if not text or len(text)>280:
        raise SystemExit(f"Invalid X post length: {len(text)}")
    required=("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    if any(not os.environ.get(k) for k in required):
        raise SystemExit("Existing X OAuth secrets unavailable; post not attempted")
    sess=OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response=sess.post("https://api.x.com/2/tweets",json={"text":text},timeout=45)
    if not response.ok:
        raise SystemExit(f"X publication failed HTTP {response.status_code}: {response.text[:260]}")
    post_id=response.json().get("data",{}).get("id")
    if not post_id:
        raise SystemExit("Response had no X post ID")
    print("Published: https://x.com/yonnastgetahun/status/"+str(post_id))

if __name__=="__main__":
    main()
