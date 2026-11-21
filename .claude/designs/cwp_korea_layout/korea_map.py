# Read-only look at the Korean provinces in provinces.png. Writes a picture to the scratchpad.
import sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
MOD = r"C:/Users/Matthew Winter/Documents/Paradox Interactive/Victoria 3/mod/Cold War Project - Rebuild"
states = {
 "SEOUL_S": "03EAAF 305000 70EFC0 7B6E17 A0E2EE A84864 ACB4D5 B05000",
 "SEOUL_N": "709080 71770E E0D3E4 FD1E20",
 "BUSAN": "076864 305080 31D000 806A04 9BA8B5 A00BB8 C3F34F",
 "YANGHO": "34B782 8ACAAA A48A8B AE0221 B0D000 B0D080 BC0C5A C81C12 D42CA8 F09080 F91D98",
 "SARIWON": "00227F 08C343 21D080 4C743B 4FC1C9 701101 8B0207 8FC58D 92D8ED A0987D A0D080 BD9C6F CF9212 EDB9A8",
 "PYONGYANG": "096D79 11044D 12BC01 47D537 5204B8 605101 640C37 701180 7BEA9E 808E39 880F26 913CAF A2DB51 B8F465 C5EF9A DD6252 EAF581 F01000 F01180",
}
base = {"SEOUL_S": (90,140,230), "SEOUL_N": (230,120,60), "BUSAN": (60,190,200), "YANGHO": (120,200,120), "SARIWON": (220,80,80), "PYONGYANG": (200,90,170)}
col2state = {}
for s, v in states.items():
    for h in v.split():
        col2state[(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))] = (s, h)
im = Image.open(MOD + "/map_data/provinces.png").convert("RGB")
W, H = im.size
print("map size", W, H)
x0, x1, y0, y1 = 6500, 7500, 400, 1700
crop = im.crop((x0, y0, x1, y1)); px = crop.load()
info = {}
minx=miny=10**9; maxx=maxy=-1
for y in range(y1-y0):
    for x in range(x1-x0):
        c = px[x,y]
        if c in col2state:
            d = info.setdefault(c, [0,0,0,10**9,-1,10**9,-1])
            d[0]+=1; d[1]+=x; d[2]+=y
            d[3]=min(d[3],y); d[4]=max(d[4],y); d[5]=min(d[5],x); d[6]=max(d[6],x)
            minx=min(minx,x); maxx=max(maxx,x); miny=min(miny,y); maxy=max(maxy,y)
print("bbox (map px)", x0+minx, y0+miny, x0+maxx, y0+maxy, "found", len(info), "of", len(col2state))
pad=12; S=6
bx0=max(0,minx-pad); by0=max(0,miny-pad); bx1=min(x1-x0-1,maxx+pad); by1=min(y1-y0-1,maxy+pad)
w=bx1-bx0+1; h=by1-by0+1
out = Image.new("RGB", (w*S, h*S), (25,35,60)); op = out.load()
import colorsys
def shade(c, s, i):
    r,g,b = base[s]; k = 0.80 + 0.07*(i%5)
    return (min(255,int(r*k)), min(255,int(g*k)), min(255,int(b*k)))
order = {c:i for i,c in enumerate(sorted(info, key=lambda c:(info[c][2]/info[c][0], info[c][1]/info[c][0])))}
for y in range(h):
    for x in range(w):
        c = px[bx0+x, by0+y]
        if c in col2state:
            col = shade(c, col2state[c][0], order[c])
        elif c == (255,255,255) or (c[0]<40 and c[1]<40):  # unknown: draw raw colour dimmed
            col = (c[0]//3, c[1]//3, c[2]//3)
        else:
            col = (60+c[0]//6, 60+c[1]//6, 60+c[2]//6)
        # borders
        edge = False
        if x+1<w and px[bx0+x+1,by0+y]!=c: edge=True
        if y+1<h and px[bx0+x,by0+y+1]!=c: edge=True
        for dy in range(S):
            for dx in range(S):
                op[x*S+dx, y*S+dy] = col
        if edge:
            for d in range(S):
                if x+1<w and px[bx0+x+1,by0+y]!=c: op[x*S+S-1, y*S+d] = (0,0,0)
                if y+1<h and px[bx0+x,by0+y+1]!=c: op[x*S+d, y*S+S-1] = (0,0,0)
dr = ImageDraw.Draw(out)
try: font = ImageFont.truetype("arial.ttf", 15)
except: font = ImageFont.load_default()
rows=[]
for c,i in sorted(order.items(), key=lambda t:t[1]):
    n,sx,sy,ymin,ymax,xmin,xmax = info[c]; cx=sx/n; cy=sy/n
    s,hx = col2state[c]
    dr.text(((cx-bx0)*S-8, (cy-by0)*S-8), str(i+1), fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
    rows.append((i+1, hx, s, n, round(x0+cx), round(y0+cy), y0+ymin, y0+ymax))
out.save("korea_provinces.png")
print("img", out.size)
for r in rows: print(*r)
