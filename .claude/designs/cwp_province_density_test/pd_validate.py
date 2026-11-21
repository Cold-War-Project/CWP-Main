# Validates the written mod against vanilla. Read-only.
import json, collections
import pd_common
from pd_common import *
TAG = os.environ.get("PD_TAG", ""); DEST = "C:/Users/Matthew Winter/Documents/Paradox Interactive/Victoria 3/mod/" + os.environ.get("PD_NAME", "CWP Province Density Test")
L = load_image(); H, W = L.shape
S0 = load_states(); loc = load_locators(); nav = load_naval(); adj = load_adjacencies()
a = np.asarray(Image.open(DEST + "/map_data/provinces.png")); assert a.shape == (H, W, 3) and a.dtype == np.uint8, a.shape
N = (a[..., 0].astype(np.uint32) << 16) | (a[..., 1].astype(np.uint32) << 8) | a[..., 2]
meta = json.load(open("pd_children%s.json" % TAG)); kids = {code(k): [code(c) for c, s in v] for k, v in meta["children"].items()}
parent = {c: p for p, ks in kids.items() for c in ks}
oldc, newc = set(np.unique(L).tolist()), set(np.unique(N).tolist())
print("colours old", len(oldc), "new", len(newc), "| old ids all still present:", oldc <= newc, "| new ids:", len(newc - oldc), "== children:", (newc - oldc) == set(parent))
# every pixel: new code is the old code or one of its children
par_arr = np.arange(1 << 24, dtype=np.uint32)
for c, p in parent.items(): par_arr[c] = p
print("pixels whose new province is not inside its parent:", int((par_arr[N] != L).sum()))
imp = set().union(*[v["impassable"] for v in S0.values()]); seas = {p for v in S0.values() if v["sea"] for p in v["provinces"]}
print("split parents that are impassable or sea:", len(set(kids) & (imp | seas)))
cnt = np.bincount(N.ravel(), minlength=1 << 24)
land_new = [int(cnt[c]) for v in S0.values() if not v["sea"] for p in v["provinces"] if p not in imp for c in [p] + kids.get(p, [])]
q = np.percentile(land_new, [0, 1, 5, 25, 50, 75, 95, 99, 100])
print("passable land provinces", len(land_new), "mean px %.1f" % np.mean(land_new), "percentiles 0/1/5/25/50/75/95/99/100:", [int(x) for x in q], "| under 10 px:", sum(x < 10 for x in land_new))
# state regions in the mod
pd_common.VAN_SAVE = pd_common.VAN
def states_from(root):
    old = pd_common.VAN; pd_common.VAN = root
    try: return load_states()
    finally: pd_common.VAN = old
S1 = states_from(DEST)
print("state regions vanilla(land)", sum(1 for v in S0.values() if not v["sea"]), "mod files", len(S1))
bad = 0; where = collections.Counter()
for k, v in S1.items():
    v0 = S0[k]
    exp = [c for p in v0["provinces"] for c in [p] + kids.get(p, [])]
    if v["provinces"] != exp: bad += 1
    if v["impassable"] != v0["impassable"] or v["hubs"] != v0["hubs"] or v["id"] != v0["id"]: bad += 1
    if v["prime"] != {c for p in v0["prime"] for c in [p] + kids.get(p, [])}: bad += 1
    for p in v["provinces"]: where[p] += 1
print("state regions differing from expectation:", bad, "| provinces listed in more than one state:", sum(1 for n in where.values() if n > 1),
      "| new ids not in any state:", len(set(parent) - set(where)), "| land-state ids not in image:", len(set(where) - newc))
# history
def owned(path):
    t = nocomment(read(path)); out = []
    for m in re.finditer(r"\bowned_provinces\s*=\s*\{([^}]*)\}", t): out.append([code(x) for x in HEX.findall(m.group(1))])
    return out, t
h0, t0 = owned(VAN + "/common/history/states/00_states.txt"); h1, t1 = owned(DEST + "/common/history/states/00_states.txt")
okh = len(h0) == len(h1) and all(b == [c for p in a_ for c in [p] + kids.get(p, [])] for a_, b in zip(h0, h1))
own1 = set(x for l in h1 for x in l); own0 = set(x for l in h0 for x in l)
print("create_state blocks", len(h0), len(h1), "| each block = parents + their children:", okh, "| children of owned parents not owned:", len({c for c, p in parent.items() if p in own0} - own1),
      "| braces", t1.count("{"), t1.count("}"), "| create_state count equal:", t0.count("create_state") == t1.count("create_state"))
bad_quotes = [q for q in re.findall(r'"[^"\n]*"', t1) if " " in q.strip('"') and HEX.search(q)]
print("quoted strings holding more than one province id:", len(bad_quotes))
r0, r1 = nocomment(read(VAN + "/" + RELEASABLES)), nocomment(read(DEST + "/" + RELEASABLES))
l0 = [[code(x) for x in HEX.findall(m.group(1))] for m in re.finditer(r"\bprovinces\s*=\s*\{([^}]*)\}", r0)]
l1 = [[code(x) for x in HEX.findall(m.group(1))] for m in re.finditer(r"\bprovinces\s*=\s*\{([^}]*)\}", r1)]
print("releasable province lists", len(l0), len(l1), "| each = parents + children:", l1 == [[c for p in a_ for c in [p] + kids.get(p, [])] for a_ in l0], "| braces", r1.count("{"), r1.count("}"))
named = script_named_provinces(); print("script-named provinces that were split:", len(named & set(kids)))
# spline hub anchors: same containment as vanilla
sp0 = sp1 = spn = 0; port_changed = []
byid_ = {v["id"]: (k, v) for k, v in S0.items()}
for i, x, z in load_spline_anchors():
    sid, n_ = divmod(i, 100); h = SPLINE_HUB.get(n_)
    if sid not in byid_ or h not in byid_[sid][1]["hubs"]: continue
    hub = byid_[sid][1]["hubs"][h]; py, px = min(H - 1, max(0, int(H - z))), int(x) % W
    spn += 1; a0 = L[py, px] == hub; a1 = N[py, px] == hub; sp0 += a0; sp1 += a1
    if a0 != a1: port_changed.append((byid_[sid][0], h))
print("hub spline anchors inside their hub province: vanilla", sp0, "mod", sp1, "of", spn, "| changed:", port_changed[:10])
# coast: every province that touched water still does
water = np.ones(1 << 24, bool)
for v in S0.values():
    if not v["sea"]:
        for p in v["provinces"]: water[p] = False
Wm = water[L]
nb = np.zeros_like(Wm); nb[1:, :] |= Wm[:-1, :]; nb[:-1, :] |= Wm[1:, :]; nb[:, 1:] |= Wm[:, :-1]; nb[:, :-1] |= Wm[:, 1:]
coast0 = set(np.unique(L[nb & ~Wm]).tolist()); coast1 = set(np.unique(N[nb & ~Wm]).tolist())
print("provinces touching water in vanilla:", len(coast0), "| of these no longer touching water:", len(coast0 - coast1),
      "| port hubs among them:", sum(1 for v in S0.values() if v["hubs"].get("port") in (coast0 - coast1)))
# terrain
tt = read(DEST + "/map_data/province_terrains.txt"); terr = {code(a_): b for a_, b in re.findall(r'^(x[0-9A-Fa-f]{6})="([^"]*)"', tt, flags=re.M)}
print("terrain entries", len(terr), "| every image colour has terrain:", newc <= set(terr), "| children match parent terrain:", all(terr[c] == terr[p] for c, p in parent.items()))
# anchors
byid = {v["id"]: v for v in S0.values()}
tot = same = in0 = in1 = 0
for h, d in loc.items():
    for sid, (x, z) in d.items():
        v = byid.get(sid)
        if not v or h not in v["hubs"]: continue
        py, px = min(H - 1, max(0, int(H - z))), int(x) % W
        tot += 1; same += (N[py, px] == L[py, px]); inhub0 = L[py, px] == v["hubs"][h]; in0 += inhub0; in1 += N[py, px] == v["hubs"][h]
print("hub locator pixels with unchanged province id:", same, "/", tot, "| locator inside its hub province: vanilla", in0, "mod", in1)
hub_ok = sum(1 for v in S0.values() for h, p in v["hubs"].items() if p in newc); print("hub provinces still on the map:", hub_ok, "/", sum(len(v["hubs"]) for v in S0.values()))
def nearest_same(points):
    ok = n = 0
    for p, x, row in points:
        if p not in kids: continue
        n += 1
        r = 14; y0, y1, x0, x1 = max(0, row - r), min(H, row + r + 1), max(0, x - r), min(W, x + r + 1)
        yy, xx = np.nonzero(L[y0:y1, x0:x1] == p)
        if not len(yy): ok += 1; continue      # anchor further than 14 px from its province: nothing to compare
        i = ((yy + y0 - row) ** 2 + (xx + x0 - x) ** 2).argmin()
        ok += N[yy[i] + y0, xx[i] + x0] == p
    return ok, n
print("harbour nodes whose nearest pixel of their province kept the id: %d / %d" % nearest_same([(p, x, H - 1 - y) for p, x, y, ty in nav if ty == "harbor"]))
pts = [(f, c[0], H - 1 - c[1]) for f, t, ty, th, c in adj if c[0] >= 0] + [(t, c[2], H - 1 - c[3]) for f, t, ty, th, c in adj if c[2] >= 0]
print("adjacency endpoints kept: %d / %d" % nearest_same(pts))
st = nocomment(read(VAN + "/common/strait_definitions/strait_definitions.txt"))
se = {code(x) for x in re.findall(r"land_endpoint\s*=\s*(x[0-9A-Fa-f]{6})", st)}; print("strait land endpoints split:", len(se & set(kids)))
for f in ["map_data/provinces.png", "map_data/province_terrains.txt", "common/history/states/00_states.txt", "map_data/state_regions/00_west_europe.txt", ".metadata/metadata.json"]:
    b = open(os.path.join(DEST, f), "rb").read(); v = os.path.join(VAN, f)
    vb = open(v, "rb").read() if os.path.exists(v) else b""
    print("%-45s %10d bytes  BOM %s (vanilla %s)  CR %d" % (f, len(b), b[:3] == b"\xef\xbb\xbf", vb[:3] == b"\xef\xbb\xbf" if vb else "-", b.count(b"\r")))
