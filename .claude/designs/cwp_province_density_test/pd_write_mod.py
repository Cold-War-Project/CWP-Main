# Writes the test mod from pd_labels.npy + pd_children.json. Reads vanilla; writes only inside DEST.
import json, shutil
from pd_common import *
TAG = os.environ.get("PD_TAG", ""); NAME = os.environ.get("PD_NAME", "CWP Province Density Test"); MODID = os.environ.get("PD_ID", "cwp.province_density_test")
DESC = os.environ.get("PD_DESC", "every passable land province split into pieces of about 55 px")
DEST = "C:/Users/Matthew Winter/Documents/Paradox Interactive/Victoria 3/mod/" + NAME
N = np.load("pd_labels%s.npy" % TAG); H, W = N.shape
meta = json.load(open("pd_children%s.json" % TAG)); kids = {k.upper().replace("X", "x"): [c for c, s in v] for k, v in meta["children"].items()}
def norm(tok): return "x" + tok[1:].upper()
def raw(p):
    b = open(p, "rb").read(); bom = b.startswith(b"\xef\xbb\xbf")
    return b[3:].decode("utf-8") if bom else b.decode("utf-8"), bom
def put(rel, text, bom):
    p = os.path.join(DEST, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
added = dict(state_regions=0, prime_land=0, history=0, terrain=0, releasables=0)
# 1 provinces.png
os.makedirs(DEST + "/map_data", exist_ok=True)
rgb = np.stack([(N >> 16) & 255, (N >> 8) & 255, N & 255], -1).astype(np.uint8)
Image.fromarray(rgb, "RGB").save(DEST + "/map_data/provinces.png", compress_level=9)
# 2 state regions: children follow their parent in provinces = { } and prime_land = { }
def expand_quoted(m, key):
    def tok(t):
        k = kids.get(norm(t.group(1)))
        if not k: return t.group(0)
        added[key] += len(k)
        q = '"' if t.group(0).startswith('"') else ''
        return t.group(0) + "".join(' %s%s%s' % (q, c, q) for c in k)
    return m.group(1) + re.sub(r'"?\b(x[0-9A-Fa-f]{6})\b"?', tok, m.group(2)) + m.group(3)
for f in sorted(glob.glob(VAN + "/map_data/state_regions/*.txt")):
    name = os.path.basename(f)
    if name.startswith("99"): continue
    t, bom = raw(f)
    t = re.sub(r"(\bprovinces\s*=\s*\{)([^}]*)(\})", lambda m: expand_quoted(m, "state_regions"), t)
    t = re.sub(r"(\bprime_land\s*=\s*\{)([^}]*)(\})", lambda m: expand_quoted(m, "prime_land"), t)
    put("map_data/state_regions/" + name, t, bom)
# 3 history: children go to the same create_state as their parent
t, bom = raw(VAN + "/common/history/states/00_states.txt")
def expand_plain(m):
    return expand_quoted(m, "history")
t = re.sub(r"(\bowned_provinces\s*=\s*\{)([^}]*)(\})", expand_plain, t)
put("common/history/states/00_states.txt", t, bom)
# 3b releasable countries: their province lists get the children too
t, bom = raw(VAN + "/" + RELEASABLES)
t = re.sub(r"(\bprovinces\s*=\s*\{)([^}]*)(\})", lambda m: expand_quoted(m, "releasables"), t)
put(RELEASABLES, t, bom)
# 4 terrain: children take the parent's terrain
t, bom = raw(VAN + "/map_data/province_terrains.txt")
terr = {norm(a): b for a, b in re.findall(r'^(x[0-9A-Fa-f]{6})="([^"]*)"', t, flags=re.M)}
lines = []
for p, ks in kids.items():
    for c in ks: lines.append('%s="%s"' % (c, terr[p])); added["terrain"] += 1
if not t.endswith("\n"): t += "\n"
put("map_data/province_terrains.txt", t + "\n".join(lines) + "\n", bom)
# 5 metadata
os.makedirs(DEST + "/.metadata", exist_ok=True)
json.dump({"name": NAME, "id": MODID, "version": "0.1.0", "game_id": "victoria3",
           "supported_game_version": "1.15.*",
           "short_description": "Throwaway engine test for vanilla: %s (%d provinces instead of 40,875). No new states, no gameplay changes." % (DESC, len(np.unique(N))),
           "tags": [], "relationships": [], "game_custom_data": {"multiplayer_synchronized": True}},
          open(DEST + "/.metadata/metadata.json", "w", encoding="utf-8", newline="\n"), indent="\t")
print("added", added, "children", sum(len(v) for v in kids.values()))
