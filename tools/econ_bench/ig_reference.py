"""Who-governs plausibility check, 1946-1950 (from the IG-attraction thread's reference table,
~/forge/ig-reference.md, 2026-11-19). Loose by design: a run "matches" a row when at least two of
the expected governing IGs are in government (or the one, if only one is listed), at least one
expected top-3 IG is in the top 3 by clout, and the largest IG is not on the never-largest list.
"""
U, R, L, I, P, D, A, B, N = ("trade_unions", "rural_folk", "landowners", "intelligentsia", "petty_bourgeoisie",
                             "devout", "armed_forces", "bureaucrats", "industrialists")

# tag(s): (govern, top3, never largest)
ROWS = {
    ("USA",): ([U, R, L, I], [U, P, N], [R, A]),
    ("RUS",): ([B, A], [B, A], [R]),
    ("GBR",): ([U, I], [U, P], [L, D]),
    ("FRA",): ([U, D, I, P], [U, P], [L]),
    ("ITA",): ([D, P, R, N], [D, P], [A]),
    ("GER", "AOZ", "BOZ", "FOZ"): ([D, N, P], [D, N], []),
    ("JAP",): ([B, N, R], [B, N, L], [A]),
    ("ROC", "CHI"): ([A, L, N, B], [A, L], [U]),
    ("PRC",): ([A, R, B], [A, R], [L, N]),
    ("HND", "IND"): ([I, R, N, P], [R, L, I], [A]),
    ("PAK",): ([L, D, B, A], [L, D], [U]),
    ("IDS",): ([I, D, A], [R, D, A], [N]),
    ("EGY",): ([L, D], [L, D], [U]),
    ("PER", "IRN"): ([L, D, A], [L, D], [U]),
    ("TUR",): ([B, A, I], [B, A, R], [U]),
    ("SAU",): ([L, D], [D, L], [U]),
    ("ETH",): ([L, D, A], [L, D], [U]),
    ("THA",): ([A, B], [A, B, D], [U]),
    ("BRZ",): ([L, A, N], [L, R, A], [U]),
    ("ARG",): ([U, A], [U, A], [L]),
    ("MEX",): ([B, U, R], [B, R, U], [D]),
    ("SPA",): ([A, D, L], [A, D, L], [U]),
    ("POR",): ([D, L, A, B], [D, L], [U]),
    ("POL", "CZH", "HUN", "ROM", "BUL"): ([B, A], [B], [R, L]),
    ("YUG",): ([B, A], [B, A], [R]),
    ("SWE", "NOR", "DEN"): ([U, R, I], [U], [L]),
    ("CAN",): ([I, N, R, D], [U, P], [L]),
    ("AST",): ([U, I], [U, P], [L]),
    ("PHI",): ([L, N], [L, R], [U]),
    ("STK",): ([L, A, B], [L, A], [U]),
    ("NRK",): ([B, A], [B, A], [L]),
}
WINDOW = (1946, 1950)


def check(tag: str, country: dict):
    for tags, (gov, top, never) in ROWS.items():
        if tag in tags:
            igs = country.get("igs") or []
            if not igs:
                return None
            ingov = set(country.get("government_igs", []))
            top3 = [g["ig"] for g in igs[:3]]
            need = min(2, len(gov))
            return {"govern": len(ingov & set(gov)) >= need, "top": any(t in top3 for t in top),
                    "never": igs[0]["ig"] not in never, "largest": igs[0]["ig"], "in_gov": sorted(ingov)}
    return None
