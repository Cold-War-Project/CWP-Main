# Preview pictures of the split layout. Reads pd_labels.npy + vanilla; writes PNGs into OUT.
import colorsys, sys
from pd_common import *
from scipy import ndimage
OUT = sys.argv[1]; TAG = os.environ.get("PD_TAG", ""); PRE = os.environ.get("PD_PRE", "layout_55px")
os.makedirs(OUT, exist_ok=True)
N = np.load("pd_labels%s.npy" % TAG); L = load_image(); H, W = L.shape
S = load_states()
names = sorted(k for k, v in S.items() if not v["sea"])
state_of = np.zeros(1 << 24, np.uint16); kind = np.zeros(1 << 24, np.uint8)   # kind 0 water/lake, 2 impassable, 3 land
for i, k in enumerate(names, 1):
    v = S[k]
    for p in v["provinces"]:
        state_of[p] = i; kind[p] = 2 if p in v["impassable"] else 3
base = np.zeros((len(names) + 1, 3), np.float32)
for i in range(1, len(names) + 1):
    base[i] = colorsys.hsv_to_rgb((i * 0.61803398875) % 1.0, 0.38 + 0.22 * ((i * 7) % 5) / 4, 0.95)
SI = state_of[L]; K = kind[L]
def render(P, label):
    """P: province code per pixel (old or new layout)."""
    shade = 0.80 + 0.20 * (((P.astype(np.uint64) * 2654435761) >> 11) & 255).astype(np.float32) / 255
    img = base[SI] * shade[..., None]
    img[K == 2] = (0.42, 0.42, 0.42); img[K == 0] = (0.10, 0.15, 0.27)
    def edge(A):
        e = np.zeros(A.shape, bool)
        e[:, :-1] |= A[:, :-1] != A[:, 1:]; e[:-1, :] |= A[:-1, :] != A[1:, :]
        return e
    land = K == 3
    img[edge(P) & land] *= 0.55          # new province borders
    img[edge(L) & (K > 0)] *= 0.45       # original province borders (darker)
    img[edge(SI) & (K > 0)] = 0.0        # state region borders
    out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    return out
new = render(N, "new"); Image.fromarray(new).save(os.path.join(OUT, PRE + "_world_full.png"), compress_level=6)
Image.fromarray(new).resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(OUT, PRE + "_world_half.png"))
old = render(L, "old")
boxes = ndimage.find_objects(SI.astype(np.int32))
def crop(tag, states, zoom, pad=12):
    ids = [names.index(s) + 1 for s in states]
    ys = [boxes[i - 1][0] for i in ids]; xs = [boxes[i - 1][1] for i in ids]
    y0 = max(0, min(s.start for s in ys) - pad); y1 = min(H, max(s.stop for s in ys) + pad)
    x0 = max(0, min(s.start for s in xs) - pad); x1 = min(W, max(s.stop for s in xs) + pad)
    a, b = old[y0:y1, x0:x1], new[y0:y1, x0:x1]
    gap = np.full((a.shape[0], 6, 3), 255, np.uint8)
    both = np.concatenate([a, gap, b], 1)
    im = Image.fromarray(both).resize((both.shape[1] * zoom, both.shape[0] * zoom), Image.NEAREST)
    im.save(os.path.join(OUT, PRE + "_%s_before_after.png" % tag)); print(tag, (x0, y0, x1, y1), im.size)
crop("korea", ["STATE_PYONGYANG", "STATE_SARIWON", "STATE_SEOUL", "STATE_YANGHO", "STATE_BUSAN"], 4)
crop("levant", ["STATE_PALESTINE", "STATE_LEBANON", "STATE_SYRIA", "STATE_SINAI", "STATE_TRANSJORDAN"], 4)
crop("germany", ["STATE_BRANDENBURG", "STATE_BAVARIA", "STATE_RHINELAND", "STATE_SCHLESWIG_HOLSTEIN", "STATE_SAXONY"], 4)
