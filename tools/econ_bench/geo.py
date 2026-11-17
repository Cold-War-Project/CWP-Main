"""Geopolitical state of a save: blocs, subjects, wars, regimes, existence, nuclear status, CWP journal entries.

Called by save.extract with the save text and the id -> tag map; returns a JSON-able dict.
"""
from __future__ import annotations

import re

from .save import db_entries, field, sub_block, top_section

SUBJECT_TYPES = {"puppet", "dominion", "protectorate", "personal_union", "chartered_company", "tributary",
                 "vassal", "colony", "crown_land", "military_occupation"}
NUCLEAR_RX = re.compile(r"nuclear|atomic", re.I)


def _date_gt(a, b):
    ta = tuple(int(x) for x in a.split(".")[:3])
    tb = tuple(int(x) for x in b.split(".")[:3])
    return ta > tb


def extract_geo(text: str, tag_of: dict, owned: set) -> dict:
    blocs = {}
    for bid, b in db_entries(top_section(text, "power_bloc_manager")):
        if field(b, "status") != "active":
            continue
        nm = re.search(r'localized_name="([^"]+)"', b) or re.search(r'\bname="([^"]+)"', b)
        blocs[bid] = {"name": nm.group(1) if nm else bid, "leader": tag_of.get(field(b, "leader")),
                      "identity": field(b, "identity"), "cohesion": float(field(b, "cohesion") or 0),
                      "founded": field(b, "founding_date"), "members": []}

    countries = {}
    for cid, b in db_entries(top_section(text, "country_manager")):
        if cid not in owned:
            continue
        tag = tag_of[cid]
        join, leave, core = field(b, "power_bloc_join_date"), field(b, "power_bloc_leave_date"), field(b, "power_bloc_as_core")
        in_bloc = bool(join) and (not leave or _date_gt(join, leave))
        vb = sub_block(b, "variables")
        nuclear_vars = sorted({v for v in re.findall(r"flag=(\w+)", vb) if NUCLEAR_RX.search(v)})
        countries[cid] = {"tag": tag, "government": field(b, "government"), "country_type": field(b, "country_type"),
                          "in_bloc": in_bloc, "bloc_core": blocs.get(core, {}).get("name") if core else None,
                          "nuclear_vars": nuclear_vars, "laws": [], "techs_nuclear": []}
        if core in blocs:
            blocs[core]["members"].append(tag)

    for _, b in db_entries(top_section(text, "laws")):
        if "active=yes" in b:
            c = countries.get(field(b, "country"))
            if c:
                c["laws"].append(field(b, "law"))

    for _, b in db_entries(top_section(text, "technology")):
        c = countries.get(field(b, "country"))
        if c:
            acq = re.search(r"acquired_technologies=\{([^}]*)\}", b)
            if acq:
                c["techs_nuclear"] = [t for t in acq.group(1).split() if NUCLEAR_RX.search(t)]
                c["tech_count"] = len(acq.group(1).split())

    subjects = []
    for _, b in db_entries(top_section(text, "pacts")):
        act = field(b, "action")
        if act in SUBJECT_TYPES:
            tg = sub_block(b, "targets")
            a, s = field(tg, "first", 2), field(tg, "second", 2)
            if a is None:
                m1, m2 = re.search(r"first=(\d+)", tg), re.search(r"second=(\d+)", tg)
                a, s = (m1.group(1) if m1 else None), (m2.group(1) if m2 else None)
            subjects.append({"overlord": tag_of.get(a, a), "subject": tag_of.get(s, s), "type": act})

    plays = {}
    for pid, b in db_entries(top_section(text, "diplomatic_plays")):
        plays[pid] = {"initiator": tag_of.get(field(b, "initiator")), "target": tag_of.get(field(b, "target")),
                      "type": field(b, "type")}

    wars = []
    for wid, b in db_entries(top_section(text, "war_manager")):
        if "dead=yes" in b:
            continue
        parts = [tag_of.get(c, c) for c in re.findall(r"\bcountry=(\d+)\s*violator", b)]
        play = plays.get(field(b, "diplomatic_play"), {})
        wars.append({"id": wid, "start": field(b, "start_date"), "participants": parts,
                     "initiator": play.get("initiator"), "target": play.get("target"), "type": play.get("type")})

    jes = []
    for _, b in db_entries(top_section(text, "journal_entry_manager")):
        ty = field(b, "type")
        if ty and ty.startswith("je_cwp") and field(b, "active") == "yes":
            inv = re.search(r"involved_countries=\{([^}]*)\}", b)
            owner = field(b, "country")
            bars = {k: float(v) for k, v in re.findall(r"type=(\w+)\s*value=(-?[\d.]+)", sub_block(b, "progress_bars"))}
            jes.append({"type": ty, "country": tag_of.get(owner) if owner else None,
                        "involved": [tag_of.get(x, x) for x in inv.group(1).split()] if inv else [], "bars": bars})

    for c in countries.values():
        c["subject_of"] = next(({"overlord": s["overlord"], "type": s["type"]} for s in subjects if s["subject"] == c["tag"]), None)
        c["at_war"] = any(c["tag"] in w["participants"] for w in wars)

    gv = {}
    m = re.search(r"^variables=\{", text, re.M)
    if m:
        from .save import match_brace
        blk = text[m.end():match_brace(text, m.end() - 1)]
        for name, typ, ident in re.findall(r"flag=(cwp_\w+)\s*data=\{\s*type=(\w+)(?:\s*identity=(-?\d+))?", blk):
            gv[name] = int(ident) / 100000 if typ == "value" and ident else (ident == "1" if typ == "boolean" else typ)

    # Characters created from cwp_fig_ templates (the historical figure pool), alive in this save.
    chars = top_section(text, "character_manager")
    figures = sorted(set(re.findall(r'template="?(cwp_fig_\w+)', chars)))

    return {"figures": figures, "global_vars": gv, "blocs": list(blocs.values()), "subjects": subjects, "wars": wars, "journal_entries": jes,
            "countries": {c["tag"]: {k: v for k, v in c.items() if k != "tag"} for c in countries.values()}}
