"""Geopolitical milestones a median observer run should recognisably follow.

Each check is evaluated on every yearly sample of every run, within its window of years; the report
gives the share of runs where it holds. Dates here only say when the real outcome held. Content
must reach it through mechanics, never by date (AGENTS.md core rule). Owners name the thread that
would act on a gap. Sources: docs/agents/areas/economy-benchmarks.md ("Geopolitics").
"""
from __future__ import annotations

import re

COMMUNIST = re.compile(r"peoples_republic|peoples_democracy|soviet|council|phalanstere|cybernetic|anarchist")
AUTOCRATIC = re.compile(r"dictatorship|junta|corporate_state|absolute|autocracy|one_party|^gov_kingdom$|sultanate|sheikhdom|"
                        r"chiefdom|theocracy|islamic|minority_rule|party_led|regency|colonial|chartered")


def regime(gov: str | None) -> str:
    g = gov or ""
    if "military_occupation" in g:
        return "occupied"
    if COMMUNIST.search(g):
        return "communist"
    if AUTOCRATIC.search(g):
        return "autocratic"
    return "pluralist"


def exists(geo, tag):
    return tag in geo["countries"]


def sovereign(geo, tag):
    c = geo["countries"].get(tag)
    return bool(c) and not c["subject_of"]


def is_regime(geo, tag, kind):
    c = geo["countries"].get(tag)
    return bool(c) and regime(c["government"]) == kind


def nuclear(geo, tag):
    c = geo["countries"].get(tag)
    return bool(c) and bool(c["nuclear_vars"])


def bloc_led_by(geo, tag):
    return any(b["leader"] == tag for b in geo["blocs"])


def china_mainland_communist(geo, econ):
    cands = [t for t in ("PRC", "ROC", "CHI") if t in econ]
    if not cands:
        return False
    big = max(cands, key=lambda t: econ[t]["population"])
    return regime(geo["countries"].get(big, {}).get("government")) == "communist"


def two_chinas(geo, econ):
    return sum(1 for t in ("PRC", "ROC", "CHI") if t in econ) >= 2


def us_soviet_war(geo):
    return any("USA" in w["participants"] and "RUS" in w["participants"] for w in geo["wars"])


# (key, title, owner thread, first year, last year, check(geo, econ) -> bool)
CHECKS = [
    ("west_bloc", "A western bloc led by the USA", "events-logic / intl-orgs", 1947, 1990, lambda g, e: bloc_led_by(g, "USA")),
    ("east_bloc", "An eastern bloc led by the USSR", "events-logic / intl-orgs", 1947, 1990, lambda g, e: bloc_led_by(g, "RUS")),
    ("ussr_communist", "The USSR stays communist", "politics", 1946, 1990, lambda g, e: is_regime(g, "RUS", "communist")),
    ("usa_pluralist", "The USA stays a pluralist democracy", "politics", 1946, 1990, lambda g, e: is_regime(g, "USA", "pluralist")),
    ("no_superpower_war", "No direct USA-USSR war", "military / events-logic", 1946, 1990, lambda g, e: not us_soviet_war(g)),
    ("two_germanys", "Two German states (FRG and GDR)", "germany", 1950, 1989, lambda g, e: exists(g, "GER") and exists(g, "DDR")),
    ("frg_sovereign", "West Germany sovereign (not occupied)", "germany", 1956, 1990, lambda g, e: sovereign(g, "GER")),
    ("frg_pluralist", "West Germany a pluralist democracy", "germany / politics", 1950, 1990, lambda g, e: is_regime(g, "GER", "pluralist")),
    ("gdr_communist", "East Germany communist", "germany / politics", 1950, 1989, lambda g, e: is_regime(g, "DDR", "communist")),
    ("two_koreas", "Two Korean states", "korea", 1949, 1990, lambda g, e: exists(g, "NRK") and exists(g, "STK")),
    ("china_communist", "A communist government holds mainland China", "china", 1950, 1990, china_mainland_communist),
    ("two_chinas", "Two Chinas (PRC and ROC on Taiwan)", "china", 1950, 1990, two_chinas),
    ("india_free", "India independent", "decolonization", 1950, 1990, lambda g, e: sovereign(g, "HND") or sovereign(g, "IND")),
    ("pakistan", "Pakistan exists", "decolonization / history", 1948, 1990, lambda g, e: exists(g, "PAK")),
    ("indonesia_free", "Indonesia independent", "decolonization", 1950, 1990, lambda g, e: sovereign(g, "IDS")),
    ("north_vietnam", "A communist Vietnamese state (DRV)", "decolonization", 1955, 1990, lambda g, e: exists(g, "DAI") and is_regime(g, "DAI", "communist")),
    ("japan_pluralist", "Japan a pluralist democracy", "politics / history", 1950, 1990, lambda g, e: is_regime(g, "JAP", "pluralist")),
    ("poland_communist", "Poland communist", "politics (sovietization)", 1949, 1988, lambda g, e: is_regime(g, "POL", "communist")),
    ("czech_communist", "Czechoslovakia communist", "politics (sovietization)", 1949, 1988, lambda g, e: is_regime(g, "CZH", "communist")),
    ("hungary_communist", "Hungary communist", "politics (sovietization)", 1949, 1988, lambda g, e: is_regime(g, "HUN", "communist")),
    ("ussr_nuclear", "USSR has the bomb", "nuclear (#818)", 1950, 1990, lambda g, e: nuclear(g, "RUS")),
    ("uk_nuclear", "Britain has the bomb", "nuclear (#818)", 1953, 1990, lambda g, e: nuclear(g, "GBR")),
    ("france_nuclear", "France has the bomb", "nuclear (#818)", 1961, 1990, lambda g, e: nuclear(g, "FRA")),
    ("china_nuclear", "China has the bomb", "nuclear (#818)", 1965, 1990,
     lambda g, e: any(nuclear(g, t) for t in ("PRC", "ROC", "CHI"))),
]

# Counts over time: {key: (title, {year: (low, high)}, fn(geo) -> number)}
SOVEREIGN_STATES = {1946: (55, 75), 1950: (60, 80), 1955: (70, 90), 1960: (90, 115), 1965: (110, 135),
                    1970: (120, 145), 1980: (145, 170), 1990: (150, 175)}  # UN membership plus non-members
NUCLEAR_POWERS = {1946: (1, 1), 1950: (2, 2), 1953: (2, 3), 1960: (3, 4), 1965: (5, 5), 1975: (5, 6), 1990: (5, 8)}


def count_sovereign(geo):
    return sum(1 for c in geo["countries"].values() if not c["subject_of"])


def count_nuclear(geo):
    return sum(1 for c in geo["countries"].values() if c["nuclear_vars"])


COUNTS = {
    "sovereign_states": ("Sovereign states (not subjects)", SOVEREIGN_STATES, count_sovereign),
    "nuclear_powers": ("Nuclear powers", NUCLEAR_POWERS, count_nuclear),
    "subjects": ("Subjects (colonies, puppets, dominions, occupations)", None, lambda g: len(g["subjects"])),
    "wars": ("Wars in progress", None, lambda g: len(g["wars"])),
    "communist_states": ("Communist states", {1950: (12, 16), 1960: (13, 17), 1970: (14, 20), 1980: (18, 26), 1990: (8, 16)},
                         lambda g: sum(1 for c in g["countries"].values() if regime(c["government"]) == "communist")),
    "blocs": ("Power blocs", None, lambda g: len(g["blocs"])),
}
