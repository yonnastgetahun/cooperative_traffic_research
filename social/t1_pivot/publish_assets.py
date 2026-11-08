#!/usr/bin/env python3
"""Byte-verified public approved Cooperative Traffic Research pivot media.

Never accepts substituted bytes, an HTML interstitial, or changed image order.
The four X images are panels 02-05: the caption acts as the cover. LinkedIn
uses all five original panels via the approved PDF. No publication here.
"""
import argparse
import hashlib
from io import BytesIO
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from PIL import Image
from pypdf import PdfReader

PDF = (
    "https://at.adobe.com/7oEcwCwYr5OGlU3B",
    "0f0042b44a08ca4c726e94a71cbc3506375d3e1d00035e0ba38a6773a14ff34d",
)
# Preserves the complete story except the dedicated cover panel (01).
X_PANELS = [
    ("02_result", "https://at.adobe.com/vg2awA9W5kSTXUpT",
     "4c9badd4959981d7a9a92cff15eebe3a638c543828546317cb9d2a06406ffae0"),
    ("03_controls", "https://at.adobe.com/oQCkemOZN3ijHo2n",
     "b76cec29b4ae6ba627578b0b7927129f701b92ac3a0981f60f6a04a0c892fd9f"),
    ("04_rng", "https://at.adobe.com/qe43v1si0o9QimYT",
     "139de85a6ec380e431293c4a83c9de9bc26e1248cdeced969f8e1cbaf8166af7"),
    ("05_pivot", "https://at.adobe.com/mZLFfwijvb0hf5EP",
     "cb4565e4c35a2e4959d43ce60e4df6b01a2f223b4cb8e404b73f574468e63daa"),
]
X_COPY = Path("social/x-traffic-pivot-2026-11-08-draft.txt")
LI_COPY = Path("social/linkedin/traffic_pivot_announcement.txt")
LI_PDF = Path("social/linkedin/traffic_pivot_carousel.pdf")
LANDING = "https://github.com/yonnastgetahun/cooperative_traffic_research/blob/main/docs/POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md"
OLD_TAGS = ("#AI", "#BuildInPublic", "#AIResearch", "#AIStartups",
            "#MultiAgentSystems", "#ProductManagement", "#OpenSource")


def check_captions():
    x = X_COPY.read_text(encoding="utf-8").strip()
    li = LI_COPY.read_text(encoding="utf-8").strip()
    for text, site in ((x, "X"), (li, "LinkedIn")):
        if text.count(LANDING) != 1:
            raise RuntimeError(site + ": expected exactly one findings link")
        if not set(OLD_TAGS).issubset(text.split()):
            raise RuntimeError(site + ": expected seven historical hashtags")
        if "#TrafficResearch" not in text.split():
            raise RuntimeError(site + ": missing traffic research hashtag")
    if not all(s in li for s in ("2,131 additional network-seconds",
                                "2,177 additional seconds", "380 vehicles")):
        raise RuntimeError("LinkedIn text does not match approved scientific findings")
    if not all(s in x for s in ("+2,131 network-s", "shared lane RNGs", "independent simulators")):
        raise RuntimeError("X text does not match approved pivot")
    effective = len(x) - len(LANDING) + 23
    if effective > 280:
        raise RuntimeError("X text too long after URL shortening: " + str(effective))
    print("Verified LinkedIn caption and X caption; X effective length:", effective)
    return x


def read_exact_url(url, checksum, limit=6_000_000):
    if not url.startswith("https://at.adobe.com/"):
        raise RuntimeError("Unapproved media source")
    request = Request(url, headers={"User-Agent": "cooperative-traffic-approved-asset-audit"})
    with urlopen(request, timeout=65) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise RuntimeError("Approved asset too large")
        content = response.read(limit + 1)
    if len(content) > limit:
        raise RuntimeError("Approved media too large")
    digest = hashlib.sha256(content).hexdigest()
    if digest != checksum:
        raise RuntimeError("Approved asset hash mismatch. STOP, no publication.")
    return content


def fetch_x_images():
    out = []
    for name, url, checksum in X_PANELS:
        blob = read_exact_url(url, checksum)
        with Image.open(BytesIO(blob)) as im:
            if im.format != "PNG" or im.size != (1080, 1350):
                raise RuntimeError("X image is not the approved 1080x1350 PNG: " + name)
            im.verify()
        print("PASS:", name, "approved PNG", len(blob), "bytes")
        out.append((name, blob))
    if len(out) != 4:
        raise RuntimeError("X requires exactly four approved images")
    return out


def fetch_linkedin_document():
    content = read_exact_url(*PDF)
    if not content.startswith(b"%PDF-"):
        raise RuntimeError("LinkedIn asset is not a PDF")
    pdf = PdfReader(BytesIO(content), strict=True)
    if len(pdf.pages) != 5 or any(float(p.mediabox.width) < 600 for p in pdf.pages):
        raise RuntimeError("LinkedIn document is not the approved five-page carousel")
    print("PASS: approved LinkedIn five-page PDF", len(content), "bytes")
    return content


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=("preflight", "prepare-linkedin", "prepare-x"),
                   required=True)
    args = p.parse_args()
    check_captions()
    if args.action in ("preflight", "prepare-linkedin"):
        pdf = fetch_linkedin_document()
        if args.action == "prepare-linkedin":
            LI_PDF.write_bytes(pdf)
    if args.action in ("preflight", "prepare-x"):
        fetch_x_images()
    print("PASS: approved media integrity; no publication by this script")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("STOP before any post: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
