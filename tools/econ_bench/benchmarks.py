"""Historical economic benchmarks, as ranges the median observer run should land in.

Game money is not dollars, so every benchmark is a ratio: a country's GDP or GDP per capita
relative to the USA, the USA's share of world GDP, or a country's growth since 1950. The
reasoning and sources are in docs/agents/areas/economy-benchmarks.md; keep the two in step.

Anchors are Maddison (2007, millions of 1990 international dollars) for 1950, 1973 and 1989;
in-between years are interpolated and widened. The USSR range spans Maddison (low) to the CIA's
Cold War estimates (high), which disagree by about half.
"""

# Entities: a benchmark country may be several tags in the game (zones before a state exists,
# a tag that changes). The first existing tag list that has population is used, summed.
ENTITIES = {
    "USA": [["USA"]],
    "USSR": [["RUS"], ["RSF"]],
    "UK": [["GBR"]],
    "France": [["FRA"]],
    "West Germany": [["GER"], ["AOZ", "BOZ", "FOZ"]],
    "Japan": [["JAP"]],
    "China": [["PRC", "ROC", "CHI"]],
    "India": [["HND"], ["IND"]],
    "Italy": [["ITA"]],
    "Brazil": [["BRZ"]],
}

# GDP relative to the USA: {entity: {year: (low, high)}}
GDP_VS_USA = {
    "USSR":         {1950: (0.30, 0.45), 1955: (0.32, 0.47), 1960: (0.35, 0.50), 1970: (0.38, 0.55), 1980: (0.35, 0.55), 1990: (0.28, 0.50)},
    "UK":           {1950: (0.20, 0.28), 1955: (0.19, 0.26), 1960: (0.18, 0.25), 1970: (0.16, 0.22), 1980: (0.15, 0.20), 1990: (0.14, 0.19)},
    "France":       {1950: (0.13, 0.18), 1955: (0.14, 0.19), 1960: (0.15, 0.20), 1970: (0.17, 0.22), 1980: (0.16, 0.21), 1990: (0.15, 0.20)},
    "West Germany": {1950: (0.12, 0.18), 1955: (0.17, 0.24), 1960: (0.23, 0.30), 1970: (0.24, 0.31), 1980: (0.23, 0.29), 1990: (0.18, 0.24)},
    "Japan":        {1950: (0.09, 0.13), 1955: (0.11, 0.16), 1960: (0.15, 0.22), 1970: (0.28, 0.38), 1980: (0.33, 0.42), 1990: (0.34, 0.44)},
    "China":        {1950: (0.13, 0.20), 1955: (0.15, 0.22), 1960: (0.15, 0.24), 1970: (0.15, 0.24), 1980: (0.20, 0.30), 1990: (0.28, 0.42)},
    "India":        {1950: (0.12, 0.18), 1955: (0.12, 0.17), 1960: (0.12, 0.17), 1970: (0.12, 0.16), 1980: (0.13, 0.17), 1990: (0.15, 0.21)},
    "Italy":        {1950: (0.09, 0.13), 1955: (0.10, 0.14), 1960: (0.12, 0.16), 1970: (0.14, 0.19), 1980: (0.15, 0.19), 1990: (0.14, 0.18)},
}

# GDP per capita relative to the USA
GDPPC_VS_USA = {
    "USSR":         {1950: (0.25, 0.38), 1960: (0.28, 0.42), 1970: (0.30, 0.45), 1980: (0.28, 0.45), 1990: (0.25, 0.40)},
    "UK":           {1950: (0.65, 0.80), 1960: (0.65, 0.80), 1970: (0.64, 0.78), 1980: (0.64, 0.76), 1990: (0.64, 0.78)},
    "France":       {1950: (0.48, 0.62), 1960: (0.58, 0.72), 1970: (0.70, 0.84), 1980: (0.72, 0.84), 1990: (0.70, 0.82)},
    "West Germany": {1950: (0.38, 0.52), 1960: (0.60, 0.76), 1970: (0.70, 0.84), 1980: (0.74, 0.86), 1990: (0.74, 0.88)},
    "Japan":        {1950: (0.16, 0.24), 1960: (0.28, 0.40), 1970: (0.58, 0.72), 1980: (0.66, 0.78), 1990: (0.72, 0.85)},
    "China":        {1950: (0.03, 0.07), 1960: (0.04, 0.08), 1970: (0.04, 0.07), 1980: (0.04, 0.08), 1990: (0.06, 0.10)},
    "India":        {1950: (0.05, 0.08), 1960: (0.04, 0.07), 1970: (0.04, 0.06), 1980: (0.04, 0.06), 1990: (0.04, 0.07)},
}

# USA share of world GDP (all countries in the game summed)
USA_WORLD_SHARE = {1950: (0.24, 0.30), 1960: (0.22, 0.28), 1970: (0.20, 0.26), 1980: (0.19, 0.24), 1990: (0.19, 0.24)}

# Real GDP growth since 1950 (multiple of the 1950 value). Game GDP is at game prices, which move,
# so read these as a rough check on pace, not a hard target.
GROWTH_SINCE_1950 = {
    "USA":          {1960: (1.30, 1.55), 1970: (1.90, 2.30), 1980: (2.60, 3.10), 1990: (3.60, 4.30)},
    "USSR":         {1960: (1.50, 1.85), 1970: (2.30, 2.90), 1980: (3.00, 3.80), 1990: (3.40, 4.40)},
    "Japan":        {1960: (2.00, 2.60), 1970: (5.50, 7.00), 1980: (8.50, 10.5), 1990: (12.5, 15.5)},
    "West Germany": {1960: (2.30, 2.90), 1970: (3.50, 4.30), 1980: (4.50, 5.50), 1990: (5.00, 6.00)},
}

# Defence spending as a share of GDP (OMB historical tables for the USA; SIPRI and CIA estimates for
# the others; the USSR figure is very uncertain). Compared against the game's military goods and
# wages, which leave out part of what a real defence budget counts.
MILITARY_SHARE = {
    "USA":    {1950: (0.04, 0.07), 1955: (0.09, 0.12), 1960: (0.08, 0.10), 1970: (0.07, 0.09), 1980: (0.04, 0.06), 1990: (0.045, 0.06)},
    "USSR":   {1950: (0.09, 0.20), 1960: (0.10, 0.20), 1970: (0.11, 0.20), 1980: (0.12, 0.20), 1990: (0.10, 0.20)},
    "UK":     {1950: (0.06, 0.10), 1960: (0.05, 0.07), 1970: (0.04, 0.06), 1980: (0.04, 0.06), 1990: (0.035, 0.05)},
    "France": {1950: (0.05, 0.08), 1960: (0.05, 0.07), 1970: (0.03, 0.045), 1980: (0.03, 0.045), 1990: (0.03, 0.04)},
    "West Germany": {1960: (0.03, 0.05), 1970: (0.03, 0.04), 1980: (0.025, 0.04), 1990: (0.02, 0.035)},
    "Japan":  {1960: (0.008, 0.015), 1970: (0.006, 0.012), 1980: (0.008, 0.012), 1990: (0.008, 0.012)},
}

# Rank the economies should hold (by GDP) in the median run; USA first throughout.
RANK_RULES = [
    ("USA first by GDP every sampled year", lambda year, ranking: ranking[:1] == ["USA"]),
    ("USSR in the top three until 1990", lambda year, ranking: year >= 1990 or "USSR" in ranking[:3]),
]

# Fiscal health: great powers should not default.
GREAT_POWERS = ["USA", "USSR", "UK", "France", "West Germany", "Japan", "China", "India", "Italy"]

TABLES = {
    "gdp_vs_usa": ("GDP relative to the USA", GDP_VS_USA),
    "gdppc_vs_usa": ("GDP per capita relative to the USA", GDPPC_VS_USA),
    "growth_since_1950": ("GDP as a multiple of its 1950 value", GROWTH_SINCE_1950),
    "military_share": ("Military spending as a share of GDP", MILITARY_SHARE),
}


def band(table: dict, entity: str, year: int):
    """(low, high) for entity in year, linearly interpolated between the given years; None outside them."""
    pts = table.get(entity) if entity is not None else table
    if not pts:
        return None
    ys = sorted(pts)
    if year < ys[0] or year > ys[-1]:
        return None
    if year in pts:
        return pts[year]
    lo = max(y for y in ys if y < year)
    hi = min(y for y in ys if y > year)
    f = (year - lo) / (hi - lo)
    return tuple(a + (b - a) * f for a, b in zip(pts[lo], pts[hi]))

# Shares of value added by sector (primary: agriculture, forestry, fishing, mining, oil and gas;
# secondary: manufacturing and utilities, construction left out). Tertiary is the rest. Approximate,
# from national accounts histories and World Bank WDI (from 1960); USSR from Western reconstructions.
# The game leaves government services and construction out of the base (see sectors.py), so its
# tertiary share runs low; the primary and secondary ranges are the ones to compare.
SECTOR_SHARES = {
    "primary": {
        "USA":          {1950: (0.08, 0.11), 1960: (0.05, 0.08), 1970: (0.04, 0.06), 1980: (0.05, 0.07), 1990: (0.03, 0.05)},
        "USSR":         {1950: (0.25, 0.35), 1970: (0.15, 0.22), 1990: (0.12, 0.18)},
        "UK":           {1950: (0.08, 0.11), 1970: (0.04, 0.06), 1990: (0.03, 0.06)},
        "France":       {1950: (0.14, 0.20), 1970: (0.07, 0.10), 1990: (0.04, 0.06)},
        "West Germany": {1950: (0.10, 0.14), 1970: (0.04, 0.06), 1990: (0.02, 0.03)},
        "Japan":        {1955: (0.20, 0.24), 1970: (0.07, 0.09), 1990: (0.03, 0.04)},
        "China":        {1952: (0.50, 0.58), 1970: (0.35, 0.42), 1990: (0.27, 0.32)},
        "India":        {1950: (0.52, 0.60), 1970: (0.42, 0.48), 1990: (0.31, 0.36)},
    },
    "secondary": {
        "USA":          {1950: (0.31, 0.35), 1960: (0.29, 0.33), 1970: (0.25, 0.29), 1980: (0.22, 0.26), 1990: (0.19, 0.22)},
        "USSR":         {1950: (0.30, 0.40), 1970: (0.38, 0.45), 1990: (0.38, 0.45)},
        "UK":           {1950: (0.36, 0.40), 1970: (0.30, 0.35), 1990: (0.21, 0.25)},
        "France":       {1950: (0.30, 0.36), 1970: (0.27, 0.31), 1990: (0.20, 0.24)},
        "West Germany": {1950: (0.38, 0.44), 1970: (0.38, 0.43), 1990: (0.30, 0.34)},
        "Japan":        {1955: (0.26, 0.30), 1970: (0.34, 0.38), 1990: (0.27, 0.30)},
        "China":        {1952: (0.15, 0.22), 1970: (0.30, 0.38), 1990: (0.33, 0.38)},
        "India":        {1950: (0.10, 0.14), 1970: (0.13, 0.17), 1990: (0.17, 0.21)},
    },
}
TABLES["primary_share"] = ("Primary sector share of value added", SECTOR_SHARES["primary"])
TABLES["secondary_share"] = ("Manufacturing and utilities share of value added", SECTOR_SHARES["secondary"])
