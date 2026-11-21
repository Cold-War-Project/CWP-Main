# Shared loaders for the province density test. Reads vanilla only.
import sys, os, re, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pylib"))
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
VAN = "F:/SteamLibrary/steamapps/common/Victoria 3/game"
HEX = re.compile(r"x[0-9A-Fa-f]{6}")
def read(p): return open(p, encoding="utf-8-sig").read()
def nocomment(t): return re.sub(r"#[^\n]*", "", t)
def code(h): return int(h[1:], 16)
def hx(c): return "x%06X" % c
def load_image():
    a = np.asarray(Image.open(VAN + "/map_data/provinces.png").convert("RGB")).astype(np.uint32)
    return (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
def load_states():
    """state -> dict(id, file, provinces[int], impassable set, prime set, hubs{type:int})"""
    out = {}
    for f in sorted(glob.glob(VAN + "/map_data/state_regions/*.txt")):
        t = nocomment(read(f))
        parts = re.split(r"^(STATE_[A-Z0-9_]+)\s*=\s*\{", t, flags=re.M)
        for i in range(1, len(parts), 2):
            name, body = parts[i], parts[i + 1]
            def lst(key):
                m = re.search(r"\b" + key + r"\s*=\s*\{([^}]*)\}", body)
                return [code(x) for x in HEX.findall(m.group(1))] if m else []
            hubs = {}
            for h in ("city", "port", "farm", "mine", "wood"):
                m = re.search(r"\b" + h + r"\s*=\s*\"?(x[0-9A-Fa-f]{6})", body)
                if m: hubs[h] = code(m.group(1))
            out[name] = dict(id=int(re.search(r"\bid\s*=\s*(\d+)", body).group(1)), file=os.path.basename(f), sea=os.path.basename(f).startswith("99"),
                             provinces=lst("provinces"), impassable=set(lst("impassable")), prime=set(lst("prime_land")), hubs=hubs)
    return out
def load_locators():
    """type -> {state_id: (x, z)}"""
    out = {}
    for h in ("city", "port", "farm", "mine", "wood"):
        t = read(VAN + "/gfx/map/map_object_data/generated_map_object_locators_%s.txt" % h)
        out[h] = {int(i): (float(x), float(z)) for i, x, z in re.findall(r"id=(\d+)\s*position=\{\s*([\-\d.]+)\s+[\-\d.]+\s+([\-\d.]+)", t)}
    return out
def load_naval():
    t = read(VAN + "/common/travel_network/naval_network.txt")
    return [(code(p), int(x), int(y), ty) for p, x, y, ty in re.findall(r"province=(x[0-9A-Fa-f]{6})\s+x=(\d+)\s+y=(\d+)\s+type=(\w+)", t)]
def load_adjacencies():
    rows = []
    for line in read(VAN + "/map_data/adjacencies.csv").splitlines()[1:]:
        c = line.split(";")
        if len(c) >= 8 and HEX.fullmatch(c[0] or "") and HEX.fullmatch(c[1] or ""):
            rows.append((code(c[0]), code(c[1]), c[2], c[3], [int(float(v)) for v in c[4:8]]))
    return rows
def load_spline_anchors():
    """[(id, x, z)] from the binary spline network. Hub anchors have id = state_id * 100 + n: 0 city, 1 farm, 2 mine, 3 port, 4 wood."""
    import struct
    b = open(VAN + "/gfx/map/spline_network/spline_network.splnet", "rb").read()
    pat = re.compile(rb"\x14\x00(....)\x4c\x00\x01\x00\x03\x00\x0d\x00(....)\x0d\x00(....)\x04\x00", re.S)
    return [(struct.unpack("<I", m.group(1))[0], struct.unpack("<f", m.group(2))[0], struct.unpack("<f", m.group(3))[0]) for m in pat.finditer(b)]
SPLINE_HUB = {0: "city", 1: "farm", 2: "mine", 3: "port", 4: "wood"}
RELEASABLES = "common/country_creation/00_releasable_countries.txt"
def script_named_provinces():
    """Province codes named by id in vanilla script, apart from the files the mod rewrites or that are handled as anchors."""
    skip = ("history/states", "travel_network", "strait_definitions", RELEASABLES)
    out = set()
    for root in ("common", "events"):
        for f in glob.glob(VAN + "/" + root + "/**/*.txt", recursive=True):
            if any(s in f.replace("\\", "/") for s in skip): continue
            out.update(code(x) for x in HEX.findall(nocomment(read(f))))
    return out
def load_default_map():
    t = nocomment(read(VAN + "/map_data/default.map"))
    def lst(key):
        m = re.search(key + r"\s*=\s*\{([^}]*)\}", t)
        return {code(x) for x in HEX.findall(m.group(1))} if m else set()
    return lst("sea_starts"), lst("lakes")
