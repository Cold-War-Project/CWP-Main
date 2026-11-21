# Province density test: split every passable land province of the VANILLA map into ~TARGET px pieces.
# Reads vanilla only. Writes pd_labels.npy (new province code per pixel) and pd_children.json beside itself.
import json, time
from pd_common import *
from scipy import ndimage
TARGET = 55; MINPX = 16; SEED = 1946
MODE = os.environ.get('PD_MODE', 'uniform'); TAG = os.environ.get('PD_TAG', ''); CAP = int(os.environ.get('PD_CAP', '0'))
target_of = None
t0 = time.time()
L = load_image(); H, W = L.shape
S = load_states(); loc = load_locators(); nav = load_naval(); adj = load_adjacencies()
byid = {v["id"]: v for v in S.values()}
imp = set().union(*[v["impassable"] for v in S.values()])
passable = {p for v in S.values() if not v["sea"] for p in v["provinces"]} - imp
st = nocomment(read(VAN + "/common/strait_definitions/strait_definitions.txt"))
strait_land = {code(x) for x in re.findall(r"land_endpoint\s*=\s*(x[0-9A-Fa-f]{6})", st)}
# anchors: province code -> list of (x, row, kind) target points; the piece nearest each keeps the old id
anchors = {}
for h, d in loc.items():
    for sid, (x, z) in d.items():
        v = byid.get(sid)
        if v and h in v["hubs"]: anchors.setdefault(v["hubs"][h], []).append((int(x) + 0.5, min(H - 1, max(0, int(H - z))) + 0.5, "hub_" + h))   # the pixel holding the locator
for p, x, y, ty in nav:
    if ty == "harbor": anchors.setdefault(p, []).append((x + 0.5, H - 1 - y + 0.5, "harbor"))
for f, t, ty, th, c in adj:
    if c[0] >= 0: anchors.setdefault(f, []).append((c[0] + 0.5, H - 1 - c[1] + 0.5, "adjacency"))
    if c[2] >= 0: anchors.setdefault(t, []).append((c[2] + 0.5, H - 1 - c[3] + 0.5, "adjacency"))
for i, x, z in load_spline_anchors():
    sid, n = divmod(i, 100); v = byid.get(sid); h = SPLINE_HUB.get(n)
    if v and h in v["hubs"]: anchors.setdefault(v["hubs"][h], []).append((int(x) + 0.5, min(H - 1, max(0, int(H - z))) + 0.5, "spline_" + h))
named = script_named_provinces() & passable
strait_land = strait_land | named   # kept whole
print("provinces kept whole because vanilla script names them:", len(named))
print("anchored provinces", len(anchors), "strait endpoints kept whole", len(strait_land & passable))
rng = np.random.default_rng(SEED)
# smooth displacement field so borders are not ruler-straight
G = 6
def field():
    lo = rng.uniform(-1, 1, (H // G + 2, W // G + 2)).astype(np.float32)
    return ndimage.zoom(lo, G, order=1)[:H, :W] * 1.8
DX, DY = field(), field()
flat = L.ravel()
order = np.argsort(flat, kind="stable")
uniq, start, counts = np.unique(flat[order], return_index=True, return_counts=True)
print("sorted", round(time.time() - t0), "s")
if MODE == 'tiers':
    import pd_tiers
    tier_of = pd_tiers.province_tiers(S); area = {int(u): int(n_) for u, n_ in zip(uniq, counts)}
    scale, predicted = pd_tiers.scale_for_cap(tier_of, area, [p for p in passable if p not in strait_land and p in area], len(uniq), CAP)
    target_of = {p: (pd_tiers.BASE[t] * scale if pd_tiers.BASE[t] else None) for p, t in tier_of.items()}
    print('tiers: scale %.4f, px targets' % scale, {t: (round(b * scale, 1) if b else None) for t, b in pd_tiers.BASE.items()}, 'predicted total', predicted, 'cap', CAP)
used = set(int(u) for u in uniq)
STRUCT = ndimage.generate_binary_structure(2, 1)
def kmeans(P, k, iters=12):
    n = len(P); c = np.empty((k, 2), np.float32); c[0] = P[rng.integers(n)]
    d = ((P - c[0]) ** 2).sum(1)
    for j in range(1, k):
        c[j] = P[d.argmax()]; d = np.minimum(d, ((P - c[j]) ** 2).sum(1))
    for _ in range(iters):
        lab = ((P[:, None, :] - c[None, :, :]) ** 2).sum(2).argmin(1)
        sums = np.zeros((k, 2), np.float32); np.add.at(sums, lab, P); cnt = np.bincount(lab, minlength=k)
        nz = cnt > 0; c[nz] = sums[nz] / cnt[nz, None]
    return ((P[:, None, :] - c[None, :, :]) ** 2).sum(2).argmin(1)
def cleanup(img):
    """img: local int array, -1 outside the province. Makes pieces connected where possible and removes tiny pieces."""
    for _ in range(4):
        changed = False
        for j in np.unique(img[img >= 0]):
            m = img == j
            cc, n = ndimage.label(m, STRUCT)
            sizes = np.bincount(cc.ravel())[1:]
            main = sizes.argmax() + 1
            for comp in range(1, n + 1):
                if comp == main and sizes[comp - 1] >= MINPX: continue
                cm = cc == comp
                ring = ndimage.binary_dilation(cm, STRUCT) & ~cm
                cand = img[ring]; cand = cand[(cand >= 0) & (cand != j)]
                if cand.size:
                    img[cm] = np.bincount(cand).argmax(); changed = True
        if not changed: break
    return img
children = {}; stats = dict(split=0, merged_anchor=0, disconnected_kept=0, anchor_far=0)
newL = flat.copy()
new_codes_needed = []
plan = []   # (parent, flat idx array, piece labels local, kept label)
for ui in range(len(uniq)):
    c = int(uniq[ui])
    if c not in passable: continue
    n = int(counts[ui]); tg = TARGET if target_of is None else target_of.get(c)
    if tg is None: continue
    k = int(n / tg + 0.5)
    if k < 2 or c in strait_land: continue
    idx = order[start[ui]:start[ui] + n]
    ys = (idx // W).astype(np.int32); xs = (idx % W).astype(np.int32)
    P = np.stack([xs + DX.ravel()[idx], ys + DY.ravel()[idx]], 1).astype(np.float32)
    lab = kmeans(P, k)
    y0, x0 = ys.min() - 1, xs.min() - 1
    img = np.full((ys.max() - y0 + 2, xs.max() - x0 + 2), -1, np.int32)
    img[ys - y0, xs - x0] = lab
    img = cleanup(img)
    lab = img[ys - y0, xs - x0]
    # kept piece: every piece holding an anchor; without anchors the piece at the centroid
    keep = set(); apix = []
    for ax, ay, kind in anchors.get(c, ()):
        d2 = (xs + 0.5 - ax) ** 2 + (ys + 0.5 - ay) ** 2; i = int(d2.argmin())   # pixel centres
        if d2[i] > 36: stats["anchor_far"] += 1
        keep.add(int(lab[i])); apix.append((int(xs[i]), int(ys[i])))
    if len(keep) > 1:
        # also keep the pieces lying on the straight line between anchors, so the kept province stays in one piece
        for (bx, by) in apix[1:]:
            steps = max(abs(bx - apix[0][0]), abs(by - apix[0][1]), 1)
            for s_ in range(steps + 1):
                lx = apix[0][0] + round((bx - apix[0][0]) * s_ / steps) - x0; ly = apix[0][1] + round((by - apix[0][1]) * s_ / steps) - y0
                if img[ly, lx] >= 0: keep.add(int(img[ly, lx]))
    if not keep:
        keep.add(int(lab[int(((xs - xs.mean()) ** 2 + (ys - ys.mean()) ** 2).argmin())]))
    keep = sorted(keep); kl = keep[0]
    if len(keep) > 1:
        stats["merged_anchor"] += 1
        lab = np.where(np.isin(lab, keep), kl, lab)
        img[ys - y0, xs - x0] = lab
        if ndimage.label(img == kl, STRUCT)[1] > 1: stats["disconnected_kept"] += 1
    pieces = [int(j) for j in np.unique(lab) if j != kl]
    if not pieces: continue
    plan.append((c, idx, lab, pieces)); stats["split"] += 1
    if stats["split"] % 5000 == 0: print(stats["split"], "provinces split", round(time.time() - t0), "s", flush=True)
total_new = sum(len(p[3]) for p in plan)
free = np.setdiff1d(np.arange(1, 0xFFFFFF, dtype=np.uint32), np.fromiter(used, np.uint32), assume_unique=True)
newc = rng.choice(free, size=total_new, replace=False); ni = 0
for c, idx, lab, pieces in plan:
    kids = []
    for j in pieces:
        nc = int(newc[ni]); ni += 1
        sel = idx[lab == j]; newL[sel] = nc; kids.append((nc, int(sel.size)))
    children[hx(c)] = [(hx(k), s) for k, s in kids]
np.save("pd_labels%s.npy" % TAG, newL.reshape(H, W))
json.dump(dict(target=TARGET, mode=MODE, cap=CAP, seed=SEED, stats=stats, children=children), open("pd_children%s.json" % TAG, "w"))
print("stats", stats, "new provinces", total_new, "total colours", len(used) + total_new, "time", round(time.time() - t0), "s")
