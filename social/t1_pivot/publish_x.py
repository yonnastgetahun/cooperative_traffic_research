#!/usr/bin/env python3
"""One-shot approved T1 pivot single X post and exactly four verified images.

No retries and no thread. The user approved this single-post draft with the
seven continuity research hashtags plus #TrafficResearch. The four images are
the result, controls, RNG, pivot panels; LinkedIn carries all five.
"""
import os
from requests_oauthlib import OAuth1Session
from publish_assets import check_captions, fetch_x_images

def main():
    caption=check_captions()
    images=fetch_x_images() # Must pass every asset before authenticating/publishing
    keys=("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")
    if any(not os.environ.get(k) for k in keys):
        raise SystemExit("Missing X OAuth credentials; NO POST.")
    session=OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"]
    )
    media=[]
    for i,(name,blob) in enumerate(images,1):
        response=session.post(
            "https://upload.twitter.com/1.1/media/upload.json",
            files={"media":(name+".png",blob,"image/png")},timeout=60)
        if not response.ok:
            raise SystemExit("X image upload failed, HTTP %s; NO POST."%response.status_code)
        media_id=response.json().get("media_id_string")
        if not media_id:
            raise SystemExit("X returned no media ID; NO POST.")
        media.append(media_id)
    if len(media)!=4:
        raise SystemExit("Media validation failed, cannot publish incomplete story.")
    response=session.post("https://api.x.com/2/tweets",
                         json={"text":caption,"media":{"media_ids":media}},
                         timeout=60)
    if not response.ok:
        raise SystemExit("X post creation returned HTTP %s; do not auto-retry."%
                         response.status_code)
    tweet_id=response.json().get("data",{}).get("id")
    if not tweet_id:
        raise SystemExit("X response lacks post ID; status ambiguous, NO RETRY.")
    print("POST_URL=https://x.com/yonnastgetahun/status/"+str(tweet_id))
    try:
        verify=session.get(
            "https://api.x.com/2/tweets/"+str(tweet_id),
            params={"tweet.fields":"attachments","expansions":"attachments.media_keys",
                    "media.fields":"type"},timeout=45)
        if not verify.ok:
            raise RuntimeError("X readback HTTP "+str(verify.status_code))
        media_keys=verify.json().get("data",{}).get("attachments",{}).get("media_keys",[])
        if len(media_keys)!=4:
            raise RuntimeError("X returned "+str(len(media_keys))+" media keys, expected 4")
        print("VERIFIED_PUBLICATION_WITH_FOUR_IMAGES="+str(tweet_id))
    except Exception as exc:
        raise SystemExit("X post CREATED but attachment readback unverified: "+
                         str(exc)+". DO NOT RETRY automatically.")

if __name__=="__main__":
    main()
