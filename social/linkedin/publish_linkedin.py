#!/usr/bin/env python3
"""Fail-closed, manual-only LinkedIn personal-profile document publisher.

verify never posts; publish requires explicit confirmation and an exact
approved PDF checksum. Never output tokens, signed upload URLs or raw API errors.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.linkedin.com"
VERSION = "202609"
PUBLISH_CONFIRM = "YES_PUBLISH_APPROVED_LINKEDIN_DOCUMENT"
PDF_SHA256 = "0f0042b44a08ca4c726e94a71cbc3506375d3e1d00035e0ba38a6773a14ff34d"
CAPTION = Path(__file__).parent / "traffic_pivot_announcement.txt"
PDF = Path(__file__).parent / "traffic_pivot_carousel.pdf"
DOC_TITLE = "Cooperative Traffic Research - Why We're Evaluating Independent Simulators"


def must(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def approved_content(require_pdf):
    must(CAPTION.is_file(), "Approved LinkedIn caption is missing")
    caption = CAPTION.read_text(encoding="utf-8").strip()
    must(300 <= len(caption) <= 3000, "Caption length is invalid")
    for anchor in (
        "2,131 additional network-seconds",
        "2,177 additional seconds",
        "380 vehicles",
        "evaluate independently developed traffic simulation frameworks",
    ):
        must(anchor in caption, "Approved caption anchor missing: " + anchor)
    required_hashtags = (
        "#TrafficResearch", "#TransportationScience", "#AI", "#BuildInPublic",
        "#AIResearch", "#AIStartups", "#MultiAgentSystems",
        "#ProductManagement", "#OpenSource"
    )
    must(all(tag in caption.split() for tag in required_hashtags),
         "Approved LinkedIn research hashtags are missing; NO POST")
    if require_pdf:
        must(PDF.is_file(), "Approved five-page carousel PDF has not been uploaded to GitHub")
        must(5000 < PDF.stat().st_size <= 100_000_000, "PDF is missing or oversized")
        with PDF.open("rb") as f:
            must(f.read(5) == b"%PDF-", "Document is not a PDF")
        must(file_sha256(PDF) == PDF_SHA256,
             "PDF checksum differs from approved five-page carousel; NO POST")
    return caption


def api_request(method, path, token, payload=None):
    headers = {
        "Authorization": "Bearer " + token,
        "Linkedin-Version": VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "User-Agent": "cooperative-traffic-github-linkedin-publisher/1.0",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(API + path, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=45) as response:
            body = response.read(2_000_000)
            return response.status, response.headers, json.loads(body) if body else {}
    except HTTPError as exc:
        raise RuntimeError(
            "LinkedIn " + method + " returned HTTP " + str(exc.code) +
            ". Check token scopes, API version and developer app. No automatic retry."
        ) from None
    except URLError:
        raise RuntimeError("LinkedIn connection error; publication may be ambiguous. NO RETRY.") from None


def identity():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    owner = os.environ.get("LINKEDIN_PERSON_URN", "").strip()
    must(token and owner, "Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN GitHub secret")
    must(owner.startswith("urn:li:person:") and len(owner) < 150, "Invalid personal author URN")
    req = Request(API + "/v2/userinfo", headers={
        "Authorization": "Bearer " + token,
        "User-Agent": "cooperative-traffic-linkedin-auth-check"
    }, method="GET")
    try:
        with urlopen(req, timeout=30) as response:
            must(response.status == 200, "LinkedIn identity check failed")
            info = json.loads(response.read(50000))
    except HTTPError as exc:
        raise RuntimeError("LinkedIn userinfo returned HTTP " + str(exc.code)) from None
    except URLError:
        raise RuntimeError("LinkedIn userinfo is unavailable") from None
    sub = str(info.get("sub", ""))
    must(sub and owner == "urn:li:person:" + sub,
         "Author URN does not match the authorized LinkedIn member")
    return token, owner


def upload_document(token, author):
    status, _, data = api_request(
        "POST", "/rest/documents?action=initializeUpload", token,
        payload={"initializeUploadRequest": {"owner": author}}
    )
    must(status == 200, "Document initialization failed")
    record = data.get("value") or {}
    upload_url = record.get("uploadUrl", "")
    urn = record.get("document", "")
    must(urn.startswith("urn:li:document:"), "No LinkedIn document URN returned")
    must(upload_url.startswith("https://www.linkedin.com/dms-uploads/"),
         "Unexpected LinkedIn document upload destination")
    req = Request(upload_url, data=PDF.read_bytes(), method="PUT", headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/pdf",
        "User-Agent": "cooperative-traffic-github-linkedin-publisher/1.0"
    })
    try:
        with urlopen(req, timeout=120) as response:
            must(response.status in (200, 201, 202, 204), "Document upload failed")
            response.read(1024)
    except HTTPError as exc:
        raise RuntimeError("LinkedIn document upload HTTP " + str(exc.code)) from None
    except URLError:
        raise RuntimeError("LinkedIn upload may be ambiguous. No post attempted.") from None

    for _ in range(15):
        status, _, d = api_request("GET", "/rest/documents/" + quote(urn, safe=":"), token)
        must(status == 200, "Document status request failed")
        if d.get("status") == "AVAILABLE":
            return urn
        if d.get("status") == "PROCESSING_FAILED":
            raise RuntimeError("LinkedIn rejected document; no post attempted")
        time.sleep(4)
    raise RuntimeError("Document not ready; no post attempted")


def publish(token, author, caption):
    document_urn = upload_document(token, author)
    post = {
        "author": author,
        "commentary": caption,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "content": {"media": {"title": DOC_TITLE, "id": document_urn}},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    # Never retry this call automatically: a timeout may mean a post exists.
    status, headers, _ = api_request("POST", "/rest/posts", token, payload=post)
    must(status == 201, "LinkedIn did not acknowledge posting; NO RETRY")
    urn = headers.get("x-restli-id", "")
    must(urn.startswith(("urn:li:share:", "urn:li:ugcPost:")),
         "Post returned no valid ID; check profile before any retry")
    print("LINKEDIN_POST_CREATED=" + urn)
    print("LinkedIn confirmed document post creation. Do not re-run publication.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=("validate", "verify", "publish"), required=True)
    parser.add_argument("--confirmation", default="")
    args = parser.parse_args()
    caption = approved_content(require_pdf=args.action == "publish")
    if args.action == "validate":
        print("PASS: LinkedIn draft validated; carousel PDF upload required before publication.")
        return
    token, author = identity()
    if args.action == "verify":
        print("PASS: LinkedIn member OAuth authenticated; NO POST.")
        return
    must(args.confirmation == PUBLISH_CONFIRM, "Manual publication confirmation mismatch")
    publish(token, author, caption)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
