#!/usr/bin/env python3
"""One-time approved Vision & FAQ X post; fail closed if the exact image cannot be verified."""
import hashlib
import os
from pathlib import Path
import requests
from requests_oauthlib import OAuth1Session

IMAGE_ID = "1HfJ-doLQ6Ery0yL3Ww5UJEGfDiP3nt1o"
IMAGE_SHA256 = "e443e405c233ebea29b9c0d7c61dcf4347e142d5808893341a58c94b5567fc44"
CAPTION = Path("social/vision-faq-x-2026-11-02.txt")

def approved_caption():
    text = CAPTION.read_text(encoding="utf-8").strip()
    assert text.startswith("“Doesn't Google Maps already do this?”")
    assert "#ProductDiscovery" in text
    link = "https://yonnastgetahun.github.io/cooperative_traffic_research/site/"
    effective_length = len(text) - len(link) + 23
    if text.count(link) != 1 or effective_length > 280:
        raise RuntimeError(f"X caption invalid or too long: {effective_length} effective characters")
    print(f"Approved X caption: {effective_length} effective characters")
    assert "cooperative_traffic_research/site/" in text
    return text

def verified_image():
    url = f"https://drive.google.com/uc?export=download&id={IMAGE_ID}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    payload = response.content
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Google Drive did not return PNG bytes; no post attempted")
    if hashlib.sha256(payload).hexdigest() != IMAGE_SHA256:
        raise RuntimeError("Approved image SHA256 mismatch; no post attempted")
    return payload

def main():
    text = approved_caption()
    image = verified_image()
    keys = ["X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"]
    if any(not os.environ.get(k) for k in keys):
        raise RuntimeError("Missing X OAuth credentials; no post attempted")
    session = OAuth1Session(
        os.environ["X_API_KEY"], client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    uploaded = session.post("https://upload.twitter.com/1.1/media/upload.json",
        files={"media":("vision-faq-x.png",image,"image/png")},timeout=60)
    if not uploaded.ok:
        raise RuntimeError(f"Image upload failed ({uploaded.status_code}); no post attempted: {uploaded.text[:250]}")
    media_id = uploaded.json().get("media_id_string")
    if not media_id:
        raise RuntimeError("Missing uploaded media ID; no post attempted")
    published = session.post("https://api.x.com/2/tweets",
        json={"text":text,"media":{"media_ids":[media_id]}},timeout=45)
    if not published.ok:
        raise RuntimeError(f"X rejected post ({published.status_code}): {published.text[:400]}")
    tweet_id = published.json().get("data",{}).get("id")
    if not tweet_id:
        raise RuntimeError("X did not return a tweet ID")
    print("Published with verified image: https://x.com/yonnastgetahun/status/"+str(tweet_id))

if __name__ == "__main__":
    main()
