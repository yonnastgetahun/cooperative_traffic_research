#!/usr/bin/env python3
"""One-shot, approval-gated publication of verified 3-panel scientific pivot.

Preflight is entirely read-only. No text-only fallback or automatic post retry.
Research experiments, policies and reserved cohorts are out of scope.
"""
import argparse
import hashlib
import importlib.util
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen
import zipfile

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "social/scientific_direction_2026_11"
LANDING = "https://yonnastgetahun.github.io/cooperative_traffic_research/site/#direction"
PDF_URL = "https://at.adobe.com/6jrOXpPadJMxYtJp"
PDF_SHA = "6ca2e85d69da4725832975213a6a89e36d4cbe01fe9fb982e6af43febfeddbf1"
ZIP_URL = "https://at.adobe.com/dswVptXPYpwyCf9K"
ZIP_SHA = "4235db95beeb21166e3cc993db2c2aed78fee63c64007da9120decbe58f8ab86"
X_EXPECTED = {
    "x/01_question.png": "83d37520202b1ae1575f4bfd385b4abf8b7f193db09c00fd90c379f4d025f35a",
    "x/02_evidence.png": "2953831e67cf3528f2e85da06e9e3e4ae43321db77cf652be1ae02e2a3853507",
    "x/03_direction.png": "9bee3a9a174684380b6fa71cc6a2b0692de4f3023d4beda612eec5a3f0b89295",
}
MARKER = BASE / "approved-publish-marker.json"
CAPTION_LI = BASE / "linkedin-caption.txt"
CAPTION_X = BASE / "x-caption.txt"

def checksum(blob):
    return hashlib.sha256(blob).hexdigest()

def download(url, digest, maxbytes=10_000_000):
    if not url.startswith("https://at.adobe.com/"):
        raise RuntimeError("Unapproved media host")
    req = Request(url, headers={"User-Agent": "cooperative-traffic-approved-direction-2026"})
    with urlopen(req, timeout=65) as resp:
        data = resp.read(maxbytes + 1)
    if len(data) > maxbytes:
        raise RuntimeError("Media exceeds accepted size")
    if checksum(data) != digest:
        raise RuntimeError("Approved media checksum mismatch. NO POST")
    return data

def validate_marker():
    marker = json.loads(MARKER.read_text(encoding="utf-8"))
    expected = {
        "approved_by_user": True,
        "approval_scope": ["linkedin_personal_profile_document_three_pages",
                           "x_one_post_three_images"],
        "status": "PUBLISH_ONCE",
        "landing": LANDING,
        "linkedin_pdf_sha256": PDF_SHA,
        "x_zip_sha256": ZIP_SHA,
    }
    if marker != expected:
        raise RuntimeError("Approved single-use marker mismatch. NO POST")

def caption(platform):
    path = CAPTION_LI if platform == "linkedin" else CAPTION_X
    s = path.read_text(encoding="utf-8").strip()
    if s.count(LANDING) != 1:
        raise RuntimeError(platform + " requires one exact website URL")
    if platform == "linkedin":
        if not 350 <= len(s) <= 3000:
            raise RuntimeError("Invalid LinkedIn caption length")
        for needle in ("central question", "equally informed independent choices",
                       "negative and inconclusive results"):
            if needle not in s:
                raise RuntimeError("Missing approved LinkedIn anchor: " + needle)
    else:
        length = len(s) - len(LANDING) + 23
        if length > 280 or length < 100:
            raise RuntimeError("Invalid X caption length, URL-adjusted: " + str(length))
    return s

def approved_pdf():
    b = download(PDF_URL, PDF_SHA)
    if not b.startswith(b"%PDF-"):
        raise RuntimeError("LinkedIn media is not PDF")
    pdf = PdfReader(BytesIO(b), strict=True)
    if len(pdf.pages) != 3:
        raise RuntimeError("LinkedIn must have exactly 3 pages")
    for page in pdf.pages:
        if (int(float(page.mediabox.width)), int(float(page.mediabox.height))) != (1080, 1350):
            raise RuntimeError("LinkedIn page dimensions differ")
    links = []
    for annot in pdf.pages[2].get("/Annots", []):
        a = annot.get_object().get("/A")
        if a is not None and a.get("/URI"):
            links.append(str(a["/URI"]))
    if LANDING not in links:
        raise RuntimeError("PDF website link missing on final page")
    print("PASS: LinkedIn exact 3-page approved PDF, bytes=" + str(len(b)))
    return b

def approved_pngs():
    data = download(ZIP_URL, ZIP_SHA)
    with zipfile.ZipFile(BytesIO(data)) as z:
        if set(z.namelist()) != set(X_EXPECTED):
            raise RuntimeError("X ZIP members do not match approved three images")
        result = []
        for name, expected in X_EXPECTED.items():
            b = z.read(name)
            if checksum(b) != expected:
                raise RuntimeError("X approved image hash mismatch: " + name)
            with Image.open(BytesIO(b)) as im:
                if im.format != "PNG" or im.size != (1200, 675):
                    raise RuntimeError("X approved PNG dimensions/type mismatch")
                im.verify()
            result.append((name.split("/")[-1], b))
    print("PASS: exact three approved X PNG images and ZIP checksums")
    return result

def preflight():
    validate_marker()
    caption("linkedin")
    caption("x")
    approved_pdf()
    approved_pngs()
    print("PASS: approved website destination, both captions and all four media checks; NO POST")

def publish_linkedin():
    validate_marker()
    s = caption("linkedin")
    pdf = approved_pdf()
    import_path = ROOT / "social/linkedin/publish_linkedin.py"
    spec = importlib.util.spec_from_file_location("existing_linkedin_publisher", import_path)
    publisher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(publisher)
    # Reuse the successfully deployed member OAuth / Documents API / Posts API path,
    # replacing only its media and title with these explicitly approved new assets.
    publisher.PDF = BASE / "approved-linkedin-3page.pdf"
    publisher.DOC_TITLE = "Cooperative Traffic Research - Making the Central Question Central"
    publisher.PDF.write_bytes(pdf)
    token, author = publisher.identity()
    publisher.publish(token, author, s)
    print("LinkedIn 201 document-post creation returned; verify the rendered PDF on post.")

def publish_x():
    from requests_oauthlib import OAuth1Session
    validate_marker()
    s = caption("x")
    images = approved_pngs()
    keys = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")
    if any(not os.environ.get(k) for k in keys):
        raise RuntimeError("Required X credentials missing; NO POST")
    session = OAuth1Session(os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"])
    ids = []
    for name, blob in images:
        res = session.post("https://upload.twitter.com/1.1/media/upload.json",
                           files={"media": (name, blob, "image/png")}, timeout=60)
        if not res.ok:
            raise RuntimeError("X image upload " + name + " failed HTTP " + str(res.status_code) + "; NO POST")
        media_id = res.json().get("media_id_string")
        if not media_id:
            raise RuntimeError("X media ID missing; NO POST")
        ids.append(media_id)
    if len(ids) != 3:
        raise RuntimeError("Three verified X media IDs required")
    res = session.post("https://api.x.com/2/tweets",
                       json={"text": s, "media": {"media_ids": ids}}, timeout=60)
    if not res.ok:
        raise RuntimeError("X creation returned HTTP " + str(res.status_code) + "; NO RETRY")
    post_id = (res.json().get("data") or {}).get("id")
    if not post_id:
        raise RuntimeError("X create result ambiguous; NO RETRY")
    print("CREATED_X_URL=https://x.com/yonnastgetahun/status/" + str(post_id))
    check = session.get("https://api.x.com/2/tweets/" + str(post_id),
                        params={"tweet.fields":"attachments",
                                "expansions":"attachments.media_keys",
                                "media.fields":"type"}, timeout=45)
    if not check.ok:
        raise RuntimeError("X post created but attachment readback failed. DO NOT RETRY")
    keys = (check.json().get("data") or {}).get("attachments", {}).get("media_keys", [])
    if len(keys) != 3:
        raise RuntimeError("X post exists but readback did not confirm all 3 PNG attachments. DO NOT RETRY")
    print("VERIFIED_X_POST_WITH_THREE_IMAGES=" + str(post_id))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", required=True, choices=["preflight","linkedin","x"])
    action = p.parse_args().action
    try:
        {"preflight": preflight,
         "linkedin": publish_linkedin,
         "x": publish_x}[action]()
    except Exception as exc:
        print("STOP: " + str(exc), file=sys.stderr)
        sys.exit(1)
