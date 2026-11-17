#!/usr/bin/env python3
"""Render the flag SVGs fetched by fetch_svg.py into 768x512 DXT5 DDS textured emblems.

Usage (from the mod root):
    python3 -I tools/flags/render.py [--work ~/forge/flag-work] [coa_key ...]

For each manifest row with a public-domain/CC0 licence and a sha256, the SVG in
<work>/svg/<coa_key>.svg is checked against the recorded sha256, wrapped in a static
HTML page that shows it through an <img> element (no script runs), and screenshotted by
snap Firefox in headless mode at exactly 768x512. Snap confinement needs the page, the
output and the profile under $HOME, hence the default work folder. Pillow then writes
gfx/coat_of_arms/textured_emblems/cwp_flag_<coa_key without cwp_>.dds as DXT5, the format of
vanilla's 768x512 flag textures.

Afterwards run apply_textures.py to point the coat-of-arms definitions at the textures.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MANIFEST = HERE / "sources.tsv"
OUT = ROOT / "gfx/coat_of_arms/textured_emblems"
W, H = 768, 512
OK = ("pd", "public domain", "cc0", "cc-zero")

PAGE = ("<!doctype html><html><head><style>html,body{margin:0;padding:0;width:%dpx;height:%dpx;"
        "overflow:hidden;background:#000}img{display:block;width:%dpx;height:%dpx}</style></head>"
        "<body><img src=\"../svg/%s.svg\"></body></html>")


def rows():
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, (ln.split("\t") + [""] * len(header))[:len(header)])) for ln in lines[1:] if ln.strip()]


def licence_ok(lic: str) -> bool:
    lic = lic.strip().lower()
    return bool(lic) and not lic.startswith(("skip", "missing")) and (lic in OK or lic.startswith(("cc0", "public domain", "pd")))


def render(work: Path, key: str) -> Path:
    html = work / "html" / f"{key}.html"
    png = work / "png" / f"{key}.png"
    html.parent.mkdir(parents=True, exist_ok=True)
    png.parent.mkdir(parents=True, exist_ok=True)
    html.write_text(PAGE % (W, H, W, H, key), encoding="utf-8")
    if png.exists():
        png.unlink()
    cmd = ["firefox", "--headless", "--no-remote", "--profile", str(work / "profile"),
           "--window-size", f"{W},{H}", "--screenshot", str(png), html.as_uri()]
    subprocess.run(cmd, check=True, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not png.exists():
        raise RuntimeError("firefox wrote no screenshot")
    return png


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--work", default=str(Path.home() / "forge/flag-work"))
    ap.add_argument("keys", nargs="*")
    args = ap.parse_args()
    work = Path(args.work).expanduser()
    (work / "profile").mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    status = 0
    for r in rows():
        key = r["coa_key"]
        if args.keys and key not in args.keys:
            continue
        svg = work / "svg" / f"{key}.svg"
        if not licence_ok(r.get("licence", "")) or not r.get("sha256") or not svg.exists():
            print(f"skip {key}: not fetched or licence {r.get('licence', '')!r}")
            continue
        if hashlib.sha256(svg.read_bytes()).hexdigest() != r["sha256"]:
            print(f"BAD {key}: svg does not match the recorded sha256")
            status = 1
            continue
        try:
            png = render(work, key)
        except (subprocess.SubprocessError, OSError, RuntimeError) as e:
            print(f"FAILED {key}: {e}")
            status = 1
            continue
        im = Image.open(png).convert("RGBA")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        colours = len(im.resize((64, 43)).getcolors(64 * 43) or [])
        if colours < 2:
            print(f"BAD {key}: render is a single colour (SVG did not load?)")
            status = 1
            continue
        dds = OUT / f"cwp_flag_{key.removeprefix('cwp_')}.dds"
        im.save(dds, pixel_format="DXT5")
        print(f"ok {key}: {dds.relative_to(ROOT)}")
    return status


if __name__ == "__main__":
    sys.exit(main())
