#!/usr/bin/env python3
"""Download the flag SVGs listed in tools/flags/sources.tsv from Wikimedia Commons.

Usage (from the mod root; -I keeps Python from importing anything from the download folder):
    python3 -I tools/flags/fetch_svg.py [--work ~/forge/flag-work] [coa_key ...]

For each row it asks the Commons API for the file's URL and licence (extmetadata
LicenseShortName / License), fills the `licence` column, and downloads the SVG to
<work>/svg/<coa_key>.svg only when the licence is public domain or CC0. Any other
licence is written as "SKIP: <licence>" and nothing is downloaded. The sha256 column
records the downloaded file, so render.py can refuse a file that changed.

Downloaded SVGs are untrusted data: this script only writes them to disk. It never parses
them as code, and render.py only shows them through an <img> element (no scripts run there).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "sources.tsv"
API = "https://commons.wikimedia.org/w/api.php"
UA = "FlagSvgBatch/1.0 (small one-off batch of public-domain flag files; paced, honours Retry-After)"
OK_LICENCES = ("pd", "public domain", "cc0", "cc-zero", "cc0 1.0")


def read_manifest():
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    rows = [dict(zip(header, (ln.split("\t") + [""] * len(header))[:len(header)])) for ln in lines[1:] if ln.strip()]
    return header, rows


def write_manifest(header, rows):
    out = ["\t".join(header)] + ["\t".join(r.get(h, "") for h in header) for r in rows]
    MANIFEST.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def get(url: str, tries: int = 5) -> bytes:
    """GET with a pause between requests and back-off on HTTP 429 (Wikimedia rate limit)."""
    for attempt in range(tries):
        time.sleep(6)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == tries - 1:
                raise
            wait = min(300, int(e.headers.get("Retry-After", "0") or 0) or 30 * (attempt + 1)) + 5
            print(f"  rate limited, waiting {wait} s", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def file_info(title: str) -> dict:
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo", "titles": title,
        "iiprop": "url|extmetadata", "iiextmetadatafilter": "LicenseShortName|License",
    })
    data = json.loads(get(f"{API}?{q}"))
    page = next(iter(data["query"]["pages"].values()))
    if "missing" in page or "imageinfo" not in page:
        return {}
    ii = page["imageinfo"][0]
    meta = ii.get("extmetadata", {})
    return {
        "url": ii["url"].split("?")[0],
        "short": meta.get("LicenseShortName", {}).get("value", ""),
        "code": meta.get("License", {}).get("value", ""),
    }


def licence_ok(info: dict) -> bool:
    vals = (info.get("short", "").strip().lower(), info.get("code", "").strip().lower())
    return any(v in OK_LICENCES or v.startswith("cc0") for v in vals)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", default=str(Path.home() / "forge/flag-work"))
    ap.add_argument("keys", nargs="*")
    args = ap.parse_args()
    svgdir = Path(args.work).expanduser() / "svg"
    svgdir.mkdir(parents=True, exist_ok=True)
    header, rows = read_manifest()
    status = 0
    for r in rows:
        if args.keys and r["coa_key"] not in args.keys:
            continue
        title = "File:" + urllib.parse.unquote(r["commons_file_page"].rsplit("/File:", 1)[1]).replace("_", " ")
        if r.get("sha256") and (svgdir / f"{r['coa_key']}.svg").exists():
            continue  # already fetched
        try:
            info = file_info(title)
        except (urllib.error.URLError, OSError) as e:
            print(f"FAILED {r['coa_key']}: {e}")
            status = 1
            continue
        if not info:
            print(f"MISSING {r['coa_key']}: {title} not on Commons")
            r["licence"], r["sha256"] = "MISSING", ""
            status = 1
            continue
        lic = info["short"] or info["code"]
        if not licence_ok(info):
            print(f"SKIP {r['coa_key']}: licence {lic!r}")
            r["licence"], r["sha256"] = f"SKIP: {lic}", ""
            continue
        try:
            data = get(info["url"])
        except (urllib.error.URLError, OSError) as e:
            print(f"FAILED {r['coa_key']}: {e}")
            status = 1
            continue
        if not data.lstrip().startswith((b"<?xml", b"<svg", b"<!--", b"<!DOCTYPE")):
            print(f"BAD {r['coa_key']}: download is not SVG text")
            status = 1
            continue
        (svgdir / f"{r['coa_key']}.svg").write_bytes(data)
        r["licence"], r["sha256"] = lic, hashlib.sha256(data).hexdigest()
        print(f"ok {r['coa_key']}: {lic}, {len(data)} bytes", flush=True)
        write_manifest(header, rows)  # keep progress if a later row fails
    write_manifest(header, rows)
    return status


if __name__ == "__main__":
    sys.exit(main())
