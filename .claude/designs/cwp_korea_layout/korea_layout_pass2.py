# PREVIEW ONLY. Reads provinces.png, proposes a ~90 province layout for Korea, writes a picture
# and a JSON of the proposal to the scratchpad. Does not write anything into the mod.
import json, math, os, random
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
MOD = r"C:/Users/Matthew Winter/Documents/Paradox Interactive/Victoria 3/mod/Cold War Project - Rebuild"
import sys
MODE = sys.argv[1] if len(sys.argv) > 1 else "C"
# Calibration: Seoul's city hub (37.57N) is at row 1203.5 and Pyongyang's (39.02N) at 1162.4: 38N = row ~1192.
# But the north-west state's port hub (Haeju, 38.04N, in history Soviet zone) sits at row 1195.5: the Hwanghae
# coast is drawn about 4 rows too far south. B = one straight line at 1196. C = 1192, stepping to 1196 on that coast.
Y38 = 1196 if MODE == "B" else 1192
WEST = {"701180", "11044D", "913CAF"}
TARGET = 90
MIN_PIECE = 45      # a cut-off piece smaller than this is merged into a neighbour on its side of the line
random.seed(1946)
states = {
    "SEOUL": "03EAAF 305000 70EFC0 7B6E17 A0E2EE A84864 ACB4D5 B05000 709080 71770E E0D3E4 FD1E20",
    "BUSAN": "076864 305080 31D000 806A04 9BA8B5 A00BB8 C3F34F",
    "YANGHO": "34B782 8ACAAA A48A8B AE0221 B0D000 B0D080 BC0C5A C81C12 D42CA8 F09080 F91D98",
    "SARIWON": "00227F 08C343 21D080 4C743B 4FC1C9 701101 8B0207 8FC58D 92D8ED A0987D A0D080 BD9C6F CF9212 EDB9A8",
    "PYONGYANG": "096D79 11044D 12BC01 47D537 5204B8 605101 640C37 701180 7BEA9E 808E39 880F26 913CAF A2DB51 B8F465 C5EF9A DD6252 EAF581 F01000 F01180",
}
state_of = {}
for s, v in states.items():
    for h in v.split():
        state_of[h] = s
im = Image.open(MOD + "/map_data/provinces.png").convert("RGB")
X0, Y0, X1, Y1 = 6900, 1040, 7100, 1340
crop = im.crop((X0, Y0, X1, Y1))
px = crop.load()
state_override = {}
pid = {}                       # (x,y) map coords -> province key
for y in range(Y1 - Y0):
    for x in range(X1 - X0):
        r, g, b = px[x, y]
        h = "%02X%02X%02X" % (r, g, b)
        if h in state_of:
            pid[(X0 + x, Y0 + y)] = h
parent = {h: h for h in state_of}          # piece -> original province
orig_pid = dict(pid)
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def pixels_of():
    d = {}
    for p, k in pid.items():
        d.setdefault(k, []).append(p)
    return d


def components(pts):
    s = set(pts)
    out = []
    while s:
        a = s.pop()
        comp = [a]
        st = [a]
        while st:
            x, y = st.pop()
            for dx, dy in N4:
                q = (x + dx, y + dy)
                if q in s:
                    s.remove(q)
                    comp.append(q)
                    st.append(q)
        out.append(comp)
    return sorted(out, key=len, reverse=True)


def north(p):
    if MODE == "C" and orig_pid.get(p) in WEST:
        return p[1] <= 1196
    return p[1] <= Y38


newcount = 0


def st(k):
    return state_override.get(k, state_of[parent[k]])


def newkey(orig):
    global newcount
    newcount += 1
    k = "NEW%02d" % newcount
    parent[k] = parent[orig]
    return k


def merge_into_neighbour(comp):
    cs = set(comp)
    score = {}
    for (x, y) in comp:
        for dx, dy in N4:
            q = (x + dx, y + dy)
            if q in pid and q not in cs and north(q) == north((x, y)):
                score[pid[q]] = score.get(pid[q], 0) + 1
    if not score:
        return None
    home = st(pid[comp[0]])
    same = {k: v for k, v in score.items() if st(k) == home}
    if same:
        score = same
    k = max(score, key=score.get)
    for p in comp:
        pid[p] = k
    return k


# ---- Step A: cut along the parallel
log = []
for k in sorted(set(pid.values())):
    pts = [p for p in pid if pid[p] == k]
    n = [p for p in pts if north(p)]
    s = [p for p in pts if not north(p)]
    if not n or not s:
        continue
    small = s if len(n) >= len(s) else n
    side = "south" if small is s else "north"
    for comp in components(small):
        if len(comp) >= MIN_PIECE:
            nk = newkey(k)
            for p in comp:
                pid[p] = nk
            log.append("cut  %s: %d px %s of the line become %s" % (k, len(comp), side, nk))
        else:
            to = merge_into_neighbour(comp)
            log.append("trim %s: %d px %s of the line -> %s" % (k, len(comp), side, to if to else "left in place"))


# ---- Step A1: the Yonan coast (south part of 11044D) joins the Ongjin piece: one southern province on that coast
ONGJIN = None
for k in set(pid.values()):
    if parent[k] == "701180":
        pts = [p for p in pid if pid[p] == k]
        if not north(pts[0]):
            ONGJIN = k
if ONGJIN:
    moved = 0
    for p in list(pid):
        if orig_pid[p] == "11044D" and not north(p):
            pid[p] = ONGJIN
            moved += 1
    log.append("Yonan coast: %d px joined to the Ongjin piece %s" % (moved, ONGJIN))

# ---- Step A2: Kaesong (the south piece of F01180) goes to STATE_SEOUL and is grown to a clickable size
KAESONG = None
for k in list(set(pid.values())):
    if parent[k] == "F01180":
        pts = [p for p in pid if pid[p] == k]
        if pts and not north(pts[0]):
            KAESONG = k
if KAESONG is None:            # the piece was too small and was merged: carve it back out of the merged neighbour
    cand = [p for p in orig_pid if orig_pid[p] == "F01180" and not north(p)]
    if cand:
        KAESONG = newkey("F01180")
        for p in cand:
            pid[p] = KAESONG
if KAESONG:
    state_override[KAESONG] = "SEOUL"
    mine = set(p for p in pid if pid[p] == KAESONG)
    while len(mine) < 60:
        ring = []
        for (x, y) in mine:
            for dx, dy in N4:
                q = (x + dx, y + dy)
                if q in pid and q not in mine and not north(q) and st(pid[q]) == "SEOUL":
                    ring.append(q)
        if not ring:
            break
        cx = sum(p[0] for p in mine) / len(mine); cy = sum(p[1] for p in mine) / len(mine)
        ring = sorted(set(ring), key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)[:6]
        for q in ring:
            pid[q] = KAESONG; mine.add(q)
    log.append("Kaesong piece %s: %d px, assigned to STATE_SEOUL" % (KAESONG, len(mine)))


def weight(pts):
    n = len(pts); cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    if 1178 <= cy <= 1225: return 1.6      # Kaesong-Seoul-Chuncheon corridor and the 1951-53 line of contact
    if 1150 <= cy < 1178: return 1.4       # the Pyongyang-Wonsan neck
    if 1225 < cy <= 1285 and cx >= 7005: return 1.3   # the Naktong and the Pusan perimeter
    if 1108 <= cy <= 1142: return 1.1      # Chosin and the approaches to the Yalu
    return 0.8


def stack_ns(pts):
    xs_ = [p[0] for p in pts]; ys_ = [p[1] for p in pts]
    n = len(pts); cy = sum(ys_) / n
    return (1150 <= cy <= 1225) and (max(ys_) - min(ys_)) >= 0.7 * (max(xs_) - min(xs_))


# ---- Step B: split the largest provinces until TARGET
def split(k, pts):
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - cx) ** 2 for p in pts) / n
    syy = sum((p[1] - cy) ** 2 for p in pts) / n
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in pts) / n
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    l1 = (sxx + syy) / 2 + math.sqrt(((sxx - syy) / 2) ** 2 + sxy ** 2)
    ax, ay = math.cos(th), math.sin(th)
    if stack_ns(pts):
        ax, ay = 0.0, 1.0
    d = 0.8 * math.sqrt(l1)
    seeds = [(cx - ax * d, cy - ay * d), (cx + ax * d, cy + ay * d)]
    for _ in range(8):
        acc = [[0, 0, 0], [0, 0, 0]]
        for (x, y) in pts:
            i = 0 if (x - seeds[0][0]) ** 2 + (y - seeds[0][1]) ** 2 <= (x - seeds[1][0]) ** 2 + (y - seeds[1][1]) ** 2 else 1
            acc[i][0] += x
            acc[i][1] += y
            acc[i][2] += 1
        seeds = [(a[0] / a[2], a[1] / a[2]) if a[2] else seeds[j] for j, a in enumerate(acc)]
    f1, f2 = random.uniform(.35, .6), random.uniform(.35, .6)
    p1, p2 = random.uniform(0, 6.28), random.uniform(0, 6.28)

    def noise(x, y):
        return 1.6 * (math.sin(f1 * x + 0.7 * f2 * y + p1) + math.sin(f2 * y - 0.6 * f1 * x + p2))

    part = {}
    for (x, y) in pts:
        d0 = math.hypot(x - seeds[0][0], y - seeds[0][1]) + noise(x, y)
        d1 = math.hypot(x - seeds[1][0], y - seeds[1][1]) - noise(x, y)
        part[(x, y)] = 0 if d0 <= d1 else 1
    for _ in range(4):                      # keep each part in one piece
        for i in (0, 1):
            comps = components([p for p in pts if part[p] == i])
            for c in comps[1:]:
                for p in c:
                    part[p] = 1 - i
    a = [p for p in pts if part[p] == 0]
    b = [p for p in pts if part[p] == 1]
    if min(len(a), len(b)) < MIN_PIECE:
        return False
    small = a if len(a) < len(b) else b
    nk = newkey(k)
    for p in small:
        pid[p] = nk
    return True


blocked = set()
while len(set(pid.values())) < TARGET:
    d = pixels_of()
    cand = sorted((k for k in d if k not in blocked and k != KAESONG), key=lambda k: -len(d[k]) * weight(d[k]))
    if not cand:
        break
    k = cand[0]
    if not split(k, d[k]):
        blocked.add(k)
d = pixels_of()
sizes = sorted(len(v) for v in d.values())
print("\n".join(log))
print("provinces:", len(d), "| new:", newcount, "| size min/median/max:", sizes[0], sizes[len(sizes) // 2], sizes[-1])
per_state = {}
for k in d:
    per_state.setdefault((st(k), "NRK" if north(d[k][0]) else "STK"), []).append(k)
for key in sorted(per_state):
    print(key, len(per_state[key]))
south_in_py = [k for k in d if st(k) == "PYONGYANG" and not north(d[k][0])]
print("STK pieces inside STATE_PYONGYANG:", [(k, parent[k], len(d[k])) for k in south_in_py])
with open(os.path.join(HERE, "korea_layout_pass2_%s.json" % MODE + ""), "w") as fh:
    json.dump({k: {"parent": parent[k], "state": st(k), "pixels": len(v)} for k, v in d.items()}, fh, indent=1)

# ---- picture
base = {"SEOUL": (95, 140, 225), "BUSAN": (60, 185, 195), "YANGHO": (115, 195, 115), "SARIWON": (215, 85, 85), "PYONGYANG": (195, 95, 170)}
xs = [p[0] for p in pid]
ys = [p[1] for p in pid]
pad = 10
S = 7
bx0, by0, bx1, by1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
w, h = bx1 - bx0 + 1, by1 - by0 + 1
out = Image.new("RGB", (w * S, h * S), (28, 40, 66))
dr = ImageDraw.Draw(out)
order = {k: i for i, k in enumerate(sorted(d, key=lambda k: (sum(p[1] for p in d[k]) / len(d[k]), sum(p[0] for p in d[k]) / len(d[k]))))}
for y in range(by0, by1 + 1):
    for x in range(bx0, bx1 + 1):
        k = pid.get((x, y))
        if k is None:
            r, g, b = px[x - X0, y - Y0]
            col = (52 + r // 9, 56 + g // 9, 62 + b // 9)
        else:
            r, g, b = base[st(k)]
            f = 0.78 + 0.06 * (order[k] % 5)
            if not north((x, y)) and (st(k) == "PYONGYANG" or k == KAESONG):
                r, g, b = (240, 200, 70)    # southern pieces of the north-west state
            col = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)))
        dr.rectangle([(x - bx0) * S, (y - by0) * S, (x - bx0) * S + S - 1, (y - by0) * S + S - 1], fill=col)
for (x, y), k in pid.items():
    for dx, dy in ((1, 0), (0, 1)):
        q = (x + dx, y + dy)
        k2 = pid.get(q)
        if k2 == k:
            continue
        zone = k2 is not None and north((x, y)) != north(q)
        newcut = k2 is not None and parent[k] == parent[k2]
        colr = (255, 255, 255) if zone else ((255, 235, 90) if newcut else (0, 0, 0))
        wd = 3 if zone else (2 if newcut else 1)
        X = (x - bx0) * S
        Y = (y - by0) * S
        if dx:
            dr.line([X + S - 1, Y, X + S - 1, Y + S - 1], fill=colr, width=wd)
        else:
            dr.line([X, Y + S - 1, X + S - 1, Y + S - 1], fill=colr, width=wd)
from PIL import ImageFont
try:
    font = ImageFont.truetype("arial.ttf", 17)
except Exception:
    font = ImageFont.load_default()


def label(mx, my, text, col=(255, 255, 255)):
    X = (mx - bx0) * S; Y = (my - by0) * S
    dr.ellipse([X - 4, Y - 4, X + 4, Y + 4], fill=col, outline=(0, 0, 0))
    dr.text((X + 7, Y - 10), text, fill=col, font=font, stroke_width=2, stroke_fill=(0, 0, 0))


def town(lat, lon, text):
    label(6989.2 + (lon - 126.98) * 23.0, 1203.5 + (37.57 - lat) * 27.0, text)


for nm, la, lo in (("Pyongyang", 39.02, 125.75), ("Seoul", 37.57, 126.98), ("Busan", 35.18, 129.0), ("Wonsan", 39.15, 127.44), ("Hamhung", 39.92, 127.54), ("Daegu", 35.87, 128.6), ("Sinuiju", 40.1, 124.4), ("Chongjin", 41.8, 129.78), ("Gwangju", 35.16, 126.85), ("Daejeon", 36.35, 127.38)):
    town(la, lo, nm)
for k in d:
    if not north(d[k][0]) and (st(k) == "PYONGYANG" or k == KAESONG):
        cx = sum(p[0] for p in d[k]) / len(d[k]); cy = sum(p[1] for p in d[k]) / len(d[k])
        nm = "Kaesong" if k == KAESONG else ("Ongjin" if parent[k] == "701180" else "Yonan")
        label(cx, cy, nm, (255, 240, 120))
out.save(os.path.join(HERE, "korea_layout_pass2_%s.png" % MODE))
print("picture", out.size)
