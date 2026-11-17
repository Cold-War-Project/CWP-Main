"""Sector of each building type (primary / secondary / tertiary), read from the mod's building groups.

The map is built from the mod this package sits in (tools/econ_bench -> mod root), following each
building's `building_group` up its `parent_group` chain to a root group.

Value added = sales - input costs. Government and military buildings sell nothing (their cost shows
up as negative value added) and the construction sector's output is consumed by construction rather
than sold, so all three are left out of the shares. Real GDP counts government services and
construction (about 10-20% and 4-6% of GDP), so the game's tertiary share runs low by design; compare
trends and the primary/secondary split rather than exact levels.
"""
from __future__ import annotations

import glob
import os
import re
from functools import lru_cache

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ROOT_SECTOR = {
    "bg_agriculture": "primary", "bg_plantations": "primary", "bg_extraction": "primary",
    "bg_fossil_fuels": "primary", "bg_ranching": "primary",
    "bg_manufacturing": "secondary", "bg_power": "secondary",
    "bg_urban_facilities": "tertiary", "bg_service": "tertiary", "bg_infrastructure": "tertiary",
}
EXCLUDED = {"building_construction_sector"}  # consumed, not sold
SECTORS = ("primary", "secondary", "tertiary")


@lru_cache(maxsize=None)
def building_sectors(mod_root: str = MOD_ROOT) -> dict:
    parent = {}
    for f in glob.glob(os.path.join(mod_root, "common/building_groups/*.txt")):
        t = open(f, encoding="utf-8-sig", errors="replace").read()
        for m in re.finditer(r"^(bg_\w+)\s*=\s*\{(.*?)^\}", t, re.M | re.S):
            p = re.search(r"parent_group\s*=\s*(\w+)", m.group(2))
            parent[m.group(1)] = p.group(1) if p else None

    def root(g):
        seen = set()
        while parent.get(g) and g not in seen:
            seen.add(g)
            g = parent[g]
        return g

    out = {}
    for f in glob.glob(os.path.join(mod_root, "common/buildings/*.txt")):
        t = open(f, encoding="utf-8-sig", errors="replace").read()
        for m in re.finditer(r"^(building_\w+)\s*=\s*\{(.*?)^\}", t, re.M | re.S):
            g = re.search(r"building_group\s*=\s*(\w+)", m.group(2))
            if g and m.group(1) not in EXCLUDED:
                s = ROOT_SECTOR.get(root(g.group(1)))
                if s:
                    out[m.group(1)] = s
    return out


def shares(buildings: dict) -> dict:
    """{primary, secondary, tertiary: share of value added} plus {"by_building": {b: share}}."""
    smap = building_sectors()
    va = {b: x["va"] for b, x in buildings.items() if b in smap}
    total = sum(v for v in va.values() if v > 0)
    if total <= 0:
        return {}
    out = {s: sum(v for b, v in va.items() if smap[b] == s) / total for s in SECTORS}
    out["by_building"] = {b: v / total for b, v in va.items()}
    return out
