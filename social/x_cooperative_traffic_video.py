#!/usr/bin/env python3
"""Manual-only X video publisher using the existing OAuth 1.0a secrets."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "social/video/cooperative_traffic_revised_preview.mp4"
CAPTION = ROOT / "social/video/x-caption.txt"
VIDEO_SHA256 = "d3f37bf1b53cf4cf3e686f194cd0af0e5289f1e56f9d392db37891c744a09e99"
PUBLISH_CONFIRM = "YES_PUBLISH_APPROVED_COOPERATIVE_TRAFFIC_X_VIDEO"
MEDIA_ENDPOINT = "https://upload.twitter.com/1.1/media/upload.json"
POST_ENDPOINT = "https://api.x.com/2/tweets"
CHUNK_BYTES = 4 * 1024 * 1024


def must(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate():
    must(VIDEO.is_file(), "Approved MP4 is missing")
    must(0 < VIDEO.stat().st_size <= 512 * 1024 * 1024, "MP4 is missing or exceeds legacy X video limit")
    with VIDEO.open("rb") as source:
        must(source.read(12)[4:8] == b"ftyp", "Asset is not an MP4 container")
    must(sha256(VIDEO) == VIDEO_SHA256, "MP4 checksum differs from approved asset; NO POST")
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,nb_frames",
            "-of", "json", str(VIDEO),
        ], check=True, capture_output=True, text=True,
    )
    metadata = json.loads(probe.stdout)
    streams = metadata.get("streams") or []
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    must(video is not None, "MP4 has no video stream")
    must(not any(stream.get("codec_type") == "audio" for stream in streams), "MP4 unexpectedly has audio")
    must(video.get("codec_name") == "h264", "MP4 codec is not H.264")
    must((video.get("width"), video.get("height")) == (1080, 1080), "MP4 is not 1080x1080")
    must(video.get("pix_fmt") == "yuv420p", "MP4 pixel format is not yuv420p")
    must(video.get("r_frame_rate") == "24/1", "MP4 frame rate differs from approved asset")
    must(metadata.get("format", {}).get("duration") == "27.000000", "MP4 duration differs from approved asset")
    must(CAPTION.is_file(), "Approved X caption is missing")
    caption = CAPTION.read_text(encoding="utf-8").strip()
    must(len(caption) <= 280, "X caption exceeds 280 characters")
    for tag in ("#AI", "#AIagents", "#OpenScience", "#Research", "#ChatGPT", "#Claude"):
        must(tag in caption.split(), "Required X hashtag missing: " + tag)
    return caption


def session_from_environment():
    from requests_oauthlib import OAuth1Session

    names = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")
    must(all(os.environ.get(name) for name in names), "Missing X OAuth credentials; NO POST")
    return OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def verify_credentials():
    response = session_from_environment().get(
        "https://api.x.com/2/users/me", params={"user.fields": "id,username"}, timeout=45
    )
    must(response.ok, "X read-only identity check failed")
    must((response.json().get("data") or {}).get("id"), "X identity response lacked a user ID")
    print("PASS: X OAuth authenticated; NO POST")


def upload_video(session):
    total_bytes = VIDEO.stat().st_size
    response = session.post(
        MEDIA_ENDPOINT,
        data={
            "command": "INIT",
            "media_type": "video/mp4",
            "total_bytes": total_bytes,
            "media_category": "tweet_video",
        },
        timeout=60,
    )
    must(response.ok, "X video INIT failed; NO POST")
    payload = response.json()
    media_id = str(payload.get("media_id_string") or payload.get("media_id") or "")
    must(media_id, "X INIT returned no media ID; NO POST")

    with VIDEO.open("rb") as source:
        segment = 0
        while True:
            chunk = source.read(CHUNK_BYTES)
            if not chunk:
                break
            response = session.post(
                MEDIA_ENDPOINT,
                data={"command": "APPEND", "media_id": media_id, "segment_index": segment},
                files={"media": ("chunk", chunk, "application/octet-stream")},
                timeout=120,
            )
            must(response.ok, "X video APPEND failed; no post attempted")
            segment += 1

    response = session.post(
        MEDIA_ENDPOINT,
        data={"command": "FINALIZE", "media_id": media_id},
        timeout=60,
    )
    must(response.ok, "X video FINALIZE failed; NO POST")
    return media_id, response.json().get("processing_info")


def wait_until_processed(session, media_id, processing_info):
    while processing_info:
        state = processing_info.get("state")
        if state == "succeeded":
            return
        if state == "failed":
            raise RuntimeError("X video processing failed; no post attempted")
        time.sleep(min(int(processing_info.get("check_after_secs", 5)), 30))
        response = session.get(
            MEDIA_ENDPOINT,
            params={"command": "STATUS", "media_id": media_id},
            timeout=60,
        )
        must(response.ok, "X video STATUS failed; no post attempted")
        processing_info = response.json().get("processing_info")


def publish(session, caption):
    media_id, processing_info = upload_video(session)
    wait_until_processed(session, media_id, processing_info)
    response = session.post(
        POST_ENDPOINT,
        json={"text": caption, "media": {"media_ids": [media_id]}},
        timeout=60,
    )
    must(response.ok, "X post creation failed; do not auto-retry")
    post_id = str((response.json().get("data") or {}).get("id") or "")
    must(post_id, "X post response lacked an ID; status ambiguous, NO RETRY")

    readback = session.get(
        POST_ENDPOINT + "/" + post_id,
        params={
            "tweet.fields": "attachments",
            "expansions": "attachments.media_keys",
            "media.fields": "type",
        },
        timeout=45,
    )
    must(readback.ok, "X post created but readback failed; do not retry")
    body = readback.json()
    keys = ((body.get("data") or {}).get("attachments") or {}).get("media_keys") or []
    media = (body.get("includes") or {}).get("media") or []
    must(len(keys) == 1, "X readback did not confirm exactly one media attachment")
    must(any(item.get("media_key") == keys[0] and item.get("type") == "video" for item in media),
         "X readback did not confirm a video attachment")
    print("X_POST_URL=https://x.com/yonnastgetahun/status/" + post_id)
    print("VERIFIED_X_VIDEO_ATTACHMENT=" + media_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=("validate", "verify", "publish"), required=True)
    parser.add_argument("--confirmation", default="")
    args = parser.parse_args()
    caption = validate()
    if args.action == "validate":
        print("PASS: X video asset and caption validated; NO POST")
        return
    if args.action == "verify":
        verify_credentials()
        return
    must(args.confirmation == PUBLISH_CONFIRM, "Manual publication confirmation mismatch")
    session = session_from_environment()
    publish(session, caption)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
