"""Geopolitical state of a save: blocs, subjects, wars, regimes, existence, nuclear status, CWP journal entries.

Called by save.extract with the save text and the id -> tag map; returns a JSON-able dict.
"""
from __future__ import annotations

import re

from .save import db_entries, field, sub_block, top_section

SUBJECT_TYPES = {"puppet", "dominion", "protectorate", "personal_union", "chartered_company", "tributary",
                 "vassal", "colony", "crown_land", "military_occupation"}
KEY_LAW_GROUPS = {"lawgroup_governance_principles", "lawgroup_distribution_of_power", "lawgroup_economic_system",
                  "lawgroup_trade_policy", "lawgroup_land_reform", "lawgroup_labour_associations", "lawgroup_free_speech",
                  "lawgroup_citizenship"}
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

    # Rulers: name, IG, ideology (Jack's politics check: who rules, for how long).
    ruler_of = {cid: field(b, "ruler") for cid, b in db_entries(top_section(text, "country_manager")) if cid in countries}
    want_chars = {r: cid for cid, r in ruler_of.items() if r and r != "4294967295"}
    ig_def = {iid: (field(b, "definition") or "").replace("ig_", "")
              for iid, b in db_entries(top_section(text, "interest_groups"))}
    for chid, b in db_entries(top_section(text, "character_manager")):
        cid = want_chars.get(chid)
        if cid:
            countries[cid]["ruler"] = {
                "id": chid, "name": f"{field(b, 'first_name') or ''} {field(b, 'last_name') or ''}".strip(),
                "ig": ig_def.get(field(b, "interest_group") or ""), "ideology": (field(b, "ideology") or "").replace("ideology_", ""),
                "born": field(b, "birth_date")}

    # Interest groups and parties: who governs, who has clout (Jack's per-run plausibility check).
    ig_by_id = {}
    for iid, b in db_entries(top_section(text, "interest_groups")):
        c = countries.get(field(b, "country"))
        if not c or field(b, "dead") == "yes":
            continue
        g = {"ig": (field(b, "definition") or "").replace("ig_", ""), "clout": round(float(field(b, "clout") or 0), 4),
             "in_government": field(b, "in_government") == "yes", "party": None}
        ig_by_id[iid] = g
        c.setdefault("igs", []).append(g)
    for pid, b in db_entries(top_section(text, "parties")):
        c = countries.get(field(b, "country"))
        mem = re.search(r"\bmembers=\{([^}]*)\}", b)
        if not c or not mem or not mem.group(1).split():
            continue
        name = (field(b, "definition") or "").replace("_party", "")
        members = [ig_by_id[i] for i in mem.group(1).split() if i in ig_by_id]
        for g in members:
            g["party"] = name
        c.setdefault("parties", []).append({"party": name, "members": [g["ig"] for g in members],
                                            "votes": int(float(field(b, "votes") or 0)),
                                            "in_government": any(g["in_government"] for g in members)})
    for c in countries.values():
        c["igs"] = sorted(c.get("igs", []), key=lambda g: -g["clout"])
        c["government_igs"] = [g["ig"] for g in c["igs"] if g["in_government"]]
        from .sectors import law_groups
        lg = law_groups()
        c["key_laws"] = {lg[l].replace("lawgroup_", ""): l.replace("law_", "") for l in c.get("laws", []) if l in lg and lg[l] in KEY_LAW_GROUPS}
        c["ruling_parties"] = [p["party"] for p in c.get("parties", []) if p["in_government"]]

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

    # Living characters from the historical figure pool.
    chars = top_section(text, "character_manager")
    # The save keeps no template name, so figures carry a character variable `cwp_fig` (figure pool).
    figures = len(re.findall(r"flag=cwp_fig\b", chars))

    return {"figures": figures, "global_vars": gv, "blocs": list(blocs.values()), "subjects": subjects, "wars": wars, "journal_entries": jes,
            "countries": {c["tag"]: {k: v for k, v in c.items() if k != "tag"} for c in countries.values()}}
