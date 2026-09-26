#!/usr/bin/env python3
"""Check the Cold War ideology pack against this checkout and installed assets.

Static content validation only: this does not execute Victoria 3 triggers or AI.
Standalone structural validator based on the tree representation used by the
local production-method parser. Comparison operators and tagged color blocks
are normalized because this checks structure/references, not trigger execution.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class Atom:
    value: str

@dataclass
class Pair:
    key: str
    value: str | Node

@dataclass
class Node:
    items: list[Pair | Atom]

def strip_comments(text: str) -> str:
    return re.sub(r'"(?:\\.|[^"\\])*"|#[^\r\n]*', lambda m: "" if m.group().startswith("#") else m.group(), text)

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0

    def take(self):
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of script")
        value = self.tokens[self.pos]
        self.pos += 1
        return value

    def parse(self, nested=False):
        items = []
        while self.pos < len(self.tokens):
            token = self.take()
            if token == "}" and nested:
                return Node(items)
            if token in {"{", "}", "="}:
                raise ValueError(f"Unexpected token {token}")
            if self.pos < len(self.tokens) and self.tokens[self.pos] == "=":
                self.take()
                value = self.take()
                if value in {"=", "}"}:
                    raise ValueError(f"Missing value for {token}")
                items.append(Pair(token, self.parse(True) if value == "{" else value.strip('"')))
            else:
                items.append(Atom(token.strip('"')))
        if nested:
            raise ValueError("Unclosed block")
        return Node(items)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VANILLA = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
LEX = re.compile(r'"(?:\\.|[^"\\])*"|\?=|!=|>=|<=|==|[{}=<>]|[^\s{}=#<>!?\"]+')
STANCES = {"strongly_disapprove", "disapprove", "neutral", "approve", "strongly_approve"}
PACKS = {
    "character": "cwp_character_ideologies*.txt",
    "interest_group": "cwp_interest_group_ideologies.txt",
    "movement": "cwp_movement_ideologies.txt",
}


def parse(text: str) -> Node:
    clean = strip_comments(text)
    matches = list(LEX.finditer(clean))
    end = 0
    for match in matches:
        if clean[end:match.start()].strip():
            raise ValueError(f"Malformed token near {clean[end:match.start()+30]!r}")
        end = match.end()
    if clean[end:].strip():
        raise ValueError("Malformed trailing token or unclosed quote")
    tokens = [m.group() for m in matches]
    tokens = ["=" if t in {"?=", "!=", ">=", "<=", "==", ">", "<"} else t for t in tokens]
    tokens = [t for i, t in enumerate(tokens) if not (t in {"hsv", "rgb", "hsv360"} and i+1 < len(tokens) and tokens[i+1] == "{")]
    return Parser(tokens).parse()


def pairs(node: Node):
    return [p for p in node.items if isinstance(p, Pair)]


def scalar(node: Node, key: str):
    return next((p.value for p in pairs(node) if p.key == key and isinstance(p.value, str)), None)


def child(node: Node, key: str) -> Node:
    return next((p.value for p in pairs(node) if p.key == key and isinstance(p.value, Node)), Node([]))


def atoms(node: Node, key: str):
    return [a.value for a in child(node, key).items if isinstance(a, Atom)]


def walk(node: Node):
    for p in pairs(node):
        yield p
        if isinstance(p.value, Node):
            yield from walk(p.value)


def definitions(folder: Path):
    result = {}
    for path in sorted(folder.glob("*.txt")):
        for p in pairs(parse(path.read_text(encoding="utf-8-sig"))):
            if isinstance(p.value, Node):
                result.setdefault(p.key, []).append((path, p.value))
    return result


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--vanilla", type=Path, default=DEFAULT_VANILLA, help="Victoria 3 game directory (icons and inherited support factors)")
    args = cli.parse_args()
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    ideologies = definitions(ROOT / "common/ideologies")
    laws = definitions(ROOT / "common/laws")
    law_groups = definitions(ROOT / "common/law_groups")
    law_group = {key: scalar(entries[-1][1], "group") for key, entries in laws.items()}
    known_by_group = {}
    for law, group in law_group.items():
        if group:
            known_by_group.setdefault(group, set()).add(law)

    packs = {}
    pack_sources = []
    for kind, pattern in PACKS.items():
        sources = sorted((ROOT / "common/ideologies").glob(pattern))
        require(bool(sources), f"Missing ideology pack: {pattern}")
        pack_sources.extend(sources)
        packs[kind] = {}
        for source in sources:
            for p in pairs(parse(source.read_text(encoding="utf-8-sig"))):
                if isinstance(p.value, Node):
                    require(p.key not in packs[kind], f"Duplicate pack ID: {p.key}")
                    packs[kind][p.key] = p.value
    expected = {"character": 48, "interest_group": 8, "movement": 8}
    for kind, count in expected.items():
        require(len(packs.get(kind, {})) == count, f"Expected {count} {kind} ideologies")
    new = {key: body for pack in packs.values() for key, body in pack.items()}

    localization = Counter()
    for path in (ROOT / "localization/english").rglob("*.yml"):
        for key in re.findall(r"(?m)^\s*([\w.]+):\d*\s", path.read_text(encoding="utf-8-sig")):
            localization[key] += 1
    for path in (ROOT / "localization/english").rglob("cwp_*ideolog*_l_english.yml"):
        raw = path.read_bytes()
        require(raw.startswith(b"\xef\xbb\xbf"), f"Missing localization BOM: {path.name}")
        require(b"\n" not in raw.replace(b"\r\n", b""), f"Non-CRLF localization: {path.name}")
        lines = raw.decode("utf-8-sig").splitlines()
        require(lines[0] == "l_english:", f"Invalid localization header: {path.name}")
        for i, line in enumerate(lines[1:], 2):
            if line.strip() and not line.lstrip().startswith("#"):
                require(bool(re.fullmatch(r'\s+[\w.]+:\d*\s+"(?:\\.|[^"\\])*"\s*', line)), f"Malformed localization {path.name}:{i}")

    stance_count = 0
    character_signatures = {}
    ratings = {"strongly_disapprove": -2, "disapprove": -1, "neutral": 0, "approve": 1, "strongly_approve": 2}
    for key, body in new.items():
        require(key.startswith("ideology_cwp_"), f"Missing namespace: {key}")
        require(len(ideologies[key]) == 1, f"Duplicate ideology: {key}")
        for suffix in ("", "_desc"):
            require(localization[key+suffix] == 1, f"Missing/duplicate localization: {key+suffix}")
        icon = scalar(body, "icon")
        require(icon and ((ROOT / icon).is_file() or (args.vanilla / icon).is_file()), f"Missing icon: {key}: {icon}")
        groups = [p for p in pairs(body) if p.key.startswith("lawgroup_")]
        cap = 3 if key in packs.get("interest_group", {}) else 4
        require(1 <= len(groups) <= cap, f"Law-group cap exceeded: {key}: {len(groups)} > {cap}")
        direct = Counter(p.key for p in pairs(body))
        require(all(n == 1 for n in direct.values()), f"Repeated ideology field: {key}")
        for group in pairs(body):
            if not group.key.startswith("lawgroup_"):
                continue
            require(group.key in law_groups and group.key in known_by_group, f"Disabled/unknown law group {key}: {group.key}")
            require(isinstance(group.value, Node), f"Invalid stance block: {key}/{group.key}")
            if not isinstance(group.value, Node):
                continue
            entries = pairs(group.value)
            require(len({p.key for p in entries}) == len(entries), f"Duplicate law stance: {key}/{group.key}")
            for law in entries:
                stance_count += 1
                require(law_group.get(law.key) == group.key, f"Unknown/misgrouped law: {key}/{group.key}/{law.key}")
                require(law.value in STANCES if isinstance(law.value, str) else False, f"Invalid stance: {key}/{law.key}")
        character = key in packs.get("character", {})
        require((scalar(body, "character_ideology") == "yes") == character, f"Wrong ideology category: {key}")
        if character:
            signature = tuple(sorted((g.key, tuple(sorted((p.key, p.value) for p in pairs(g.value)))) for g in groups))
            require(signature not in character_signatures, f"Identical character policy profiles: {key} and {character_signatures.get(signature)}")
            character_signatures[signature] = key
            for group in groups:
                require({p.key for p in pairs(group.value)} == known_by_group.get(group.key), f"Incomplete character law group: {key}/{group.key}")
            for field in ("country_trigger", "interest_group_leader_trigger", "non_interest_group_leader_trigger", "interest_group_leader_weight", "non_interest_group_leader_weight"):
                require(field in direct, f"Missing generation field: {key}/{field}")

    assigned_characters, assigned_igs = set(), set()
    character_pools = {}
    for path in (ROOT / "common/interest_groups").glob("*.txt"):
        if path.name == "cwp_bureaucrats.txt":
            continue  # Existing ninth-IG issue is outside this pack.
        for ig in pairs(parse(path.read_text(encoding="utf-8-sig"))):
            if not isinstance(ig.value, Node):
                continue
            pool = atoms(ig.value, "character_ideologies")
            require(len(pool) == len(set(pool)), f"Duplicate character pool entry: {ig.key}")
            character_pools[ig.key] = set(pool)
            assigned_characters.update(pool)
            assigned_igs.update(atoms(ig.value, "ideologies"))
            assigned_igs.update(p.value for p in walk(ig.value) if p.key == "add_ideology" and isinstance(p.value, str))
    for key in packs.get("character", {}):
        require(key in assigned_characters, f"Unreachable character ideology: {key}")
        body = packs["character"][key]
        eligible = {p.value for p in walk(child(body, "interest_group_leader_trigger")) if p.key == "is_interest_group_type"}
        nonleader_eligible = {p.value for p in walk(child(body, "non_interest_group_leader_trigger")) if p.key == "is_interest_group_type"}
        require(nonleader_eligible == eligible, f"Leader/nonleader eligibility mismatch: {key}: {nonleader_eligible ^ eligible}")
        assigned = {ig for ig, pool in character_pools.items() if key in pool}
        require(assigned == eligible, f"Character pool/eligibility mismatch: {key}: {assigned ^ eligible}")
        guards = [p.value for p in pairs(child(body, "non_interest_group_leader_trigger")) if p.key == "NAND" and isinstance(p.value, Node)]
        agitator_guards = [guard for guard in guards if scalar(guard, "has_role_of_type") == "agitator"]
        require(bool(agitator_guards), f"Missing agitator grievance guard: {key}")
        for guard in agitator_guards:
            goal_laws = [p.value.removeprefix("law_type:") for p in walk(child(guard, "owner")) if p.key == "has_law_or_variant" and isinstance(p.value, str)]
            require(bool(goal_laws), f"Empty agitator grievance goals: {key}")
            for law in goal_laws:
                group = child(body, law_group.get(law, ""))
                value = scalar(group, law)
                require(value in {"approve", "strongly_approve"}, f"Agitator goal outside approved policy: {key}/{law}")
                require(value is not None and ratings.get(value, -3) == max((ratings.get(p.value, -3) for p in pairs(group)), default=-3), f"Agitator goal below best policy: {key}/{law}")
    for key in packs.get("interest_group", {}):
        require(key in assigned_igs, f"Unassigned IG ideology: {key}")

    movements = definitions(ROOT / "common/political_movements")
    new_movements = {key: entries[-1][1] for key, entries in movements.items() if key.startswith("movement_cwp_")}
    require(len(new_movements) == 8, "Expected 8 Cold War political movements")
    assigned_movements = set()
    support_factors = set(definitions(args.vanilla / "common/political_movement_pop_support"))
    support_factors.update(definitions(ROOT / "common/political_movement_pop_support"))
    for key, body in new_movements.items():
        require(len(movements[key]) == 1, f"Duplicate movement: {key}")
        for suffix in ("", "_name", "_desc"):
            require(localization[key+suffix] == 1, f"Missing/duplicate movement localization: {key+suffix}")
        ideology = scalar(body, "ideology")
        require(ideology in packs.get("movement", {}), f"Invalid movement ideology: {key}/{ideology}")
        assigned_movements.add(ideology)
        for character in atoms(body, "character_ideologies"):
            require(character in ideologies and scalar(ideologies[character][-1][1], "character_ideology") == "yes", f"Invalid movement character pool: {key}/{character}")
        fields = {p.key for p in pairs(body)}
        for field in ("creation_trigger", "creation_weight", "disband_trigger", "character_support_trigger", "character_support_weight", "pop_support_trigger", "pop_support_weight", "can_pressure_interest_group"):
            require(field in fields, f"Missing movement field: {key}/{field}")
        completion = child(body, "disband_trigger")
        negative_program = child(child(child(body, "creation_trigger"), "NOT"), "AND")
        require(completion == negative_program and bool(completion.items), f"Creation/disband completion mismatch: {key}")
        goal_laws = [p.value.removeprefix("law_type:") for p in walk(completion) if p.key == "has_law_or_variant" and isinstance(p.value, str)]
        require(bool(goal_laws), f"Empty movement completion goals: {key}")
        movement_policy = packs.get("movement", {}).get(ideology, Node([]))
        for law in goal_laws:
            group = child(movement_policy, law_group.get(law, ""))
            value = scalar(group, law)
            require(value in {"approve", "strongly_approve"}, f"Movement goal outside approved policy: {key}/{law}")
            require(value is not None and ratings.get(value, -3) == max((ratings.get(p.value, -3) for p in pairs(group)), default=-3), f"Movement goal below best policy: {key}/{law}")
        pressure_igs = {p.value for p in walk(child(body, "can_pressure_interest_group")) if p.key == "is_interest_group_type"}
        eligible_igs = set()
        for character in atoms(body, "character_ideologies"):
            if character in ideologies:
                eligible_igs.update(p.value for p in walk(child(ideologies[character][-1][1], "interest_group_leader_trigger")) if p.key == "is_interest_group_type")
        require(pressure_igs == eligible_igs, f"Movement pressure/character eligibility mismatch: {key}")
        for factor in atoms(body, "pop_support_factors"):
            require(factor in support_factors, f"Unknown support factor: {key}/{factor}")
    for key in packs.get("movement", {}):
        require(key in assigned_movements, f"Unassigned movement ideology: {key}")

    # Scope the dependency check to pack files and CWP references in integration.
    sources = list(pack_sources)
    sources.append(ROOT / "common/political_movements/cwp_cold_war_movements.txt")
    for path in sources:
        if not path.exists():
            continue
        clean = strip_comments(path.read_text(encoding="utf-8-sig"))
        for law in re.findall(r"\blaw_type:(law_\w+)", clean):
            require(law_group.get(law) in known_by_group, f"Disabled/unknown trigger law: {path.name}/{law}")
        for ideology in re.findall(r"\bideology:(ideology_\w+)", clean):
            require(ideology in ideologies, f"Unknown referenced ideology: {path.name}/{ideology}")
    for folder in ("interest_groups", "history/characters", "parties", "laws", "scripted_triggers"):
        for path in (ROOT / "common" / folder).glob("*.txt"):
            clean = strip_comments(path.read_text(encoding="utf-8-sig"))
            if "ideology_cwp_" not in clean and "_party_character" not in clean:
                continue
            parse(clean)
            for ideology in re.findall(r"\bideology_cwp_\w+", clean):
                require(ideology in new, f"Unknown integrated ideology: {path.name}/{ideology}")
    helper_path = ROOT / "common/scripted_triggers/cwp_cold_war_party_triggers.txt"
    helper_nodes = {p.key: p.value for p in pairs(parse(helper_path.read_text(encoding="utf-8-sig"))) if isinstance(p.value, Node)}
    helpers = set(helper_nodes)
    party_families = {"vanguardist", "communist", "social_democrat", "market_liberal"}
    party_members = {}
    for family in party_families:
        helper = f"cwp_{family}_party_character"
        require(helper in helper_nodes, f"Missing party compatibility helper: {helper}")
        party_members[family] = {p.value.removeprefix("ideology:") for p in walk(helper_nodes.get(helper, Node([]))) if p.key == "has_ideology" and isinstance(p.value, str)}
    for path in (ROOT / "common/parties").glob("*.txt"):
        clean = strip_comments(path.read_text(encoding="utf-8-sig"))
        for helper in re.findall(r"\bcwp_\w+_party_character", clean):
            require(helper in helpers, f"Unknown party compatibility helper: {path.name}/{helper}")
    family_file = ROOT / "common/scripted_triggers/cwp_character_triggers.txt"
    family_nodes = {p.key: p.value for p in pairs(parse(family_file.read_text(encoding="utf-8-sig"))) if isinstance(p.value, Node)}
    family_loc_path = ROOT / "localization/english/replace/cwp_ideology_families_l_english.yml"
    family_loc = family_loc_path.read_text(encoding="utf-8-sig")
    family_members = set()
    for family in ("liberal", "progressive", "socialist", "conservative", "reactionary"):
        key = f"has_{family}_ideology"
        member_list = [p.value.removeprefix("ideology:") for p in walk(family_nodes[key]) if p.key == "has_ideology" and isinstance(p.value, str)]
        members = set(member_list)
        require(len(member_list) == len(members), f"Duplicate family member: {family}")
        family_members.update(members)
        require(members <= ideologies.keys(), f"Unknown ideology in family: {family}")
        loc_key = f"{family}_ideologies_list_tt"
        require(localization[loc_key] == 1, f"Missing/duplicate family localization: {loc_key}")
        line = next((line for line in family_loc.splitlines() if line.lstrip().startswith(loc_key + ":")), "")
        listed = set(re.findall(r"GetIdeology\('([^']+)'\)", line))
        require(listed == members, f"Family tooltip/predicate mismatch: {family}")
    for key in packs.get("character", {}):
        require(key in family_members, f"Character missing broad family integration: {key}")
    # Preserve monarchy support when adding a focused royalist current.
    monarchy_members = [p.value.removeprefix("ideology:") for p in walk(family_nodes["has_monarchist_ideology"]) if p.key == "has_ideology" and isinstance(p.value, str)]
    require(len(monarchy_members) == len(set(monarchy_members)), "Duplicate monarchist family member")
    expected_monarchists = {key for key, body in packs["character"].items() if scalar(child(body, "lawgroup_governance_principles"), "law_monarchy") == "strongly_approve"}
    require({key for key in monarchy_members if key.startswith("ideology_cwp_")} == expected_monarchists, "Focused monarchist family/policy mismatch")

    # Law AI accepts explicit approvers and two documented inherited-policy cases.
    for law, group in (("law_command_economy", "lawgroup_economic_system"), ("law_corporatized_unions", "lawgroup_labour_associations")):
        actual = {p.value.removeprefix("ideology:") for p in walk(child(laws[law][-1][1], "ai_will_do")) if p.key == "has_ideology" and isinstance(p.value, str) and p.value.startswith("ideology:ideology_cwp_")}
        expected = {key for key, body in packs["character"].items() if scalar(child(body, group), law) in {"approve", "strongly_approve"}}
        if law == "law_command_economy":
            inherited_policy = {"ideology_cwp_maoist", "ideology_cwp_soviet_conservative"}
            for key in inherited_policy:
                require(scalar(child(packs["character"][key], group), law) is None, f"Inherited-policy AI entry now has its own stance: {key}/{law}")
            expected.update(inherited_policy)
        require(actual == expected, f"Law AI/focused character policy mismatch: {law}: {actual ^ expected}")

    focus = json.loads((ROOT / "docs/ideologies/core_policy_focus.json").read_text(encoding="utf-8-sig"))
    for kind, records in focus.items():
        for suffix, groups in records.items():
            key = "ideology_cwp_" + suffix
            body = packs.get(kind, {}).get(key, Node([]))
            require({"lawgroup_" + group for group in groups.split()} == {p.key for p in pairs(body) if p.key.startswith("lawgroup_")}, f"Core policy-focus metadata mismatch: {key}")

    late_dates = {"titoist": "1950.1.1", "arab_socialist": "1952.1.1", "african_socialist": "1961.1.1", "military_developmentalist": "1961.1.1", "market_conservative": "1975.1.1"}
    expansion_records = []
    for path in sorted((ROOT / "docs/ideologies").glob("*_expansion.json")):
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        require(isinstance(records, list), f"Expected metadata array: {path.name}")
        expansion_records.extend(records)
    require(len(expansion_records) == 36, "Expected metadata for 36 new character profiles")
    require(len({record["id"] for record in expansion_records}) == len(expansion_records), "Duplicate expansion metadata ID")
    for record in expansion_records:
        key = record["id"]
        require(key in packs.get("character", {}), f"Missing expansion character: {key}")
        if key not in packs.get("character", {}):
            continue
        body = packs["character"][key]
        late_dates[key.removeprefix("ideology_cwp_")] = record["start_date"]
        require(set(record["law_groups"]) == {p.key for p in pairs(body) if p.key.startswith("lawgroup_")}, f"Metadata policy mismatch: {key}")
        eligible = {p.value for p in walk(child(body, "interest_group_leader_trigger")) if p.key == "is_interest_group_type"}
        require(set(record["interest_groups"]) == eligible, f"Metadata IG mismatch: {key}")
        require(bool(record["sources"]), f"Missing historical sources: {key}")
        declared_parties = record.get("party_families")
        require(isinstance(declared_parties, list), f"Missing/invalid metadata party families: {key}")
        declared_parties = set(declared_parties) if isinstance(declared_parties, list) else set()
        require(declared_parties <= party_families, f"Unknown metadata party family: {key}: {declared_parties - party_families}")
        integrated_parties = {family for family, members in party_members.items() if key in members}
        require(integrated_parties == declared_parties, f"Metadata party integration mismatch: {key}: {integrated_parties ^ declared_parties}")
        for family in record["families"]:
            family_body = family_nodes.get(f"has_{family}_ideology", Node([]))
            require(any(p.key == "has_ideology" and p.value == "ideology:"+key for p in walk(family_body)), f"Metadata family integration missing: {key}/{family}")
    for key, body in packs.get("character", {}).items():
        expected_date = late_dates.get(key.removeprefix("ideology_cwp_"), "1946.1.1")
        require(scalar(child(body, "country_trigger"), "game_date") == expected_date, f"Unexpected earliest character date: {key}")
    for key, body in new_movements.items():
        expected_date = {"movement_cwp_peasant_revolutionary": "1949.1.1", "movement_cwp_market_reform": "1975.1.1"}.get(key, "1946.1.1")
        require(scalar(child(body, "creation_trigger"), "game_date") == expected_date, f"Unexpected earliest movement date: {key}")
    if errors:
        raise SystemExit("FAILED:\n" + "\n".join(f"- {error}" for error in errors))
    print(f"PASS: {len(new)} ideologies (48 character, 8 IG, 8 movement), {len(new_movements)} movements, {stance_count} law stances; group caps, focused goals, unique profiles, references, integration, localization and icons checked.")
    print("Static validation only; launch, trigger execution, AI balance and saves are untested.")


if __name__ == "__main__":
    main()
