#!/usr/bin/env python3
"""Manual-only LinkedIn member-profile video publisher.

This is intentionally separate from the approved PDF/document publisher.
It reuses that publisher's authenticated REST request helpers, but uses the
LinkedIn Videos API and creates a post with the returned native video URN.
No automatic publication retry is allowed.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import publish_linkedin as base


ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "social/video/cooperative_traffic_revised_preview.mp4"
CAPTION = ROOT / "social/video/linkedin-caption.txt"
VIDEO_SHA256 = "d3f37bf1b53cf4cf3e686f194cd0af0e5289f1e56f9d392db37891c744a09e99"
PUBLISH_CONFIRM = "YES_PUBLISH_APPROVED_COOPERATIVE_TRAFFIC_LINKEDIN_VIDEO"
MAX_VIDEO_BYTES = 5_000_000_000


def must(condition, message):
    if not condition:
        raise RuntimeError(message)


def configured_identity():
    """Use the existing member identity without requiring OpenID userinfo.

    The established document publisher already stores the approved personal
    member URN in LINKEDIN_PERSON_URN. Some member-publishing tokens can retain
    w_member_social while denying the separate /v2/userinfo read capability;
    video publication should therefore authenticate the actual publishing call
    without changing the existing document publisher.
    """
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    owner = os.environ.get("LINKEDIN_PERSON_URN", "").strip()
    must(token and owner, "Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN GitHub secret")
    must(owner.startswith("urn:li:person:") and len(owner) < 150, "Invalid personal author URN")
    return token, owner


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate():
    must(VIDEO.is_file(), "Approved MP4 is missing")
    size = VIDEO.stat().st_size
    must(0 < size <= MAX_VIDEO_BYTES, "Approved MP4 is missing or oversized")
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

    must(CAPTION.is_file(), "Approved LinkedIn caption is missing")
    caption = CAPTION.read_text(encoding="utf-8").strip()
    must(300 <= len(caption) <= 3000, "LinkedIn caption length is invalid")
    for anchor in (
        "96 simulated drivers",
        "voluntary-style condition was 38 network-seconds higher",
        "one shifted driver",
        "development NO-GO",
        "#ChatGPT",
        "#Claude",
    ):
        must(anchor in caption, "LinkedIn caption anchor missing: " + anchor)
    return caption


def upload_video(token, owner):
    size = VIDEO.stat().st_size
    status, _, data = base.api_request(
        "POST",
        "/rest/videos?action=initializeUpload",
        token,
        payload={
            "initializeUploadRequest": {
                "owner": owner,
                "fileSizeBytes": size,
                "uploadCaptions": False,
                "uploadThumbnail": False,
            }
        },
    )
    must(status == 200, "LinkedIn video initialization failed")
    record = data.get("value") or {}
    video_urn = record.get("video", "")
    instructions = record.get("uploadInstructions") or []
    upload_token = record.get("uploadToken", "")
    must(video_urn.startswith("urn:li:video:"), "No LinkedIn video URN returned")
    must(instructions, "LinkedIn returned no video upload instructions")

    etags = []
    with VIDEO.open("rb") as source:
        for instruction in instructions:
            first = int(instruction["firstByte"])
            last = int(instruction["lastByte"])
            source.seek(first)
            part = source.read(last - first + 1)
            must(len(part) == last - first + 1, "LinkedIn video part is incomplete")
            request = Request(
                instruction["uploadUrl"],
                data=part,
                method="PUT",
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(part)),
                    "Content-Range": f"bytes {first}-{last}/{size}",
                    "User-Agent": "cooperative-traffic-linkedin-video-publisher/1.0",
                },
            )
            try:
                with urlopen(request, timeout=120) as response:
                    must(response.status in (200, 201, 202, 204), "LinkedIn video part upload failed")
                    etag = response.headers.get("ETag", "").strip('"')
                    must(etag, "LinkedIn video part returned no ETag")
                    etags.append(etag)
            except Exception as exc:
                raise RuntimeError("LinkedIn video upload may be ambiguous; no post attempted") from exc

    status, _, _ = base.api_request(
        "POST",
        "/rest/videos?action=finalizeUpload",
        token,
        payload={
            "finalizeUploadRequest": {
                "video": video_urn,
                "uploadToken": upload_token,
                "uploadedPartIds": etags,
            }
        },
    )
    must(status == 200, "LinkedIn video finalization failed")
    return video_urn


def wait_after_finalize():
    # The token can upload and publish member media but lacks the separate
    # restricted read capability required by GET /rest/videos/{urn}. The
    # documented upload sequence ends at finalize; allow processing time before
    # the one post attempt, matching the established document publisher path.
    time.sleep(15)


def publish(token, owner, caption):
    video_urn = upload_video(token, owner)
    wait_after_finalize()
    post = {
        "author": owner,
        "commentary": caption,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "content": {"media": {"title": "Cooperative Traffic Research", "id": video_urn}},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    status, headers, _ = base.api_request("POST", "/rest/posts", token, payload=post)
    must(status == 201, "LinkedIn did not acknowledge video post creation; NO RETRY")
    post_urn = headers.get("x-restli-id", "")
    must(post_urn.startswith(("urn:li:share:", "urn:li:ugcPost:")), "LinkedIn returned no valid post ID")

    print("LINKEDIN_POST_URL=https://www.linkedin.com/feed/update/" + post_urn + "/")
    print("LINKEDIN_VIDEO_ATTACHMENT_ACCEPTED=" + video_urn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=("validate", "verify", "publish"), required=True)
    parser.add_argument("--confirmation", default="")
    args = parser.parse_args()
    caption = validate()
    if args.action == "validate":
        print("PASS: LinkedIn video asset and caption validated; NO POST")
        return
    if args.action == "verify":
        base.identity()
        print("PASS: LinkedIn member OAuth authenticated; NO POST")
        return
    must(args.confirmation == PUBLISH_CONFIRM, "Manual publication confirmation mismatch")
    token, owner = configured_identity()
    publish(token, owner, caption)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
