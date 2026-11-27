"""FIT township layout, measured off the developer's site plan D5 (1600 px wide copy).
Writes layout.json (metres, x east, y north) for the Blender build, and overlay.png to check it against the plan."""
import json, math, random
from shapely.geometry import Polygon, LineString, box, Point, MultiPolygon
from shapely.ops import unary_union

random.seed(7)

# ---------- site (plan pixels, y down) ----------
ANNEX = Polygon([(408, 180), (645, 180), (645, 76), (842, 76), (842, 236), (408, 236)])
MAIN = Polygon([(880, 256), (1252, 256), (1252, 494), (1488, 494), (1488, 508), (1550, 508), (1550, 782), (1492, 782),
                (1492, 882), (1438, 882), (1438, 830), (1312, 830), (1312, 938), (1074, 938), (1074, 1032), (845, 1032),
                (845, 815), (885, 815), (885, 782), (700, 782), (520, 575), (440, 500), (490, 492), (590, 498),
                (825, 500), (825, 442), (880, 442)])
HOLES = [Polygon([(1245, 665), (1420, 665), (1420, 710), (1325, 710), (1325, 765), (1245, 765)]),   # others land
         box(1083, 780, 1153, 822), box(1140, 822, 1240, 882)]                                          # others land
SITE = unary_union([ANNEX, MAIN]).difference(unary_union(HOLES))

# ---------- roads: (points, width in metres) ----------
R = []
def road(pts, w): R.append((pts, w))
road([(1153, 256), (1153, 776)], 24)                # 24 m spine
road([(700, 768), (1550, 768)], 24)                 # 24 m south road
for x in [927, 967, 1007, 1045, 1120]:              # 12 m grid, north and south of the 590 road
    road([(x, 256 if x >= 927 else 500), (x, 760)], 12)
road([(1083, 256), (1083, 596)], 12)                # the column that becomes the linear park further south
for x in [887, 847, 810, 770, 730, 693, 653, 617]:  # 12 m grid, west part
    road([(x, 500), (x, 590)], 12)
for x in [807, 847, 890]:
    road([(x, 596), (x, 760)], 12)
road([(927, 380), (1153, 380)], 9)
road([(825, 473), (1153, 473)], 12)
road([(545, 590), (1153, 590)], 12)
road([(1153, 430), (1252, 430)], 18)
road([(1213, 430), (1213, 768)], 18)
road([(1395, 508), (1395, 622)], 18)
road([(1250, 624), (1550, 624)], 18)
road([(1474, 624), (1474, 768)], 18)
road([(987, 776), (987, 1032)], 18)
road([(867, 815), (867, 1000)], 18)
road([(845, 1005), (1074, 1005)], 18)
road([(1074, 905), (1312, 905)], 18)
road([(845, 830), (930, 830)], 15)
road([(845, 950), (930, 950)], 18)
road([(1290, 776), (1290, 905)], 18)
# north annex
road([(690, 80), (690, 236)], 12)
road([(690, 100), (842, 100)], 12)
road([(690, 197), (842, 197)], 9)
road([(770, 100), (770, 197)], 9)
# outside the site
RASTE = ([(320, 241), (1290, 241)], 11)
MEHAM = ([(330, 397), (915, 1012)], 22)
DRAIN = ([(372, 375), (958, 990)], 7)

# ---------- special zones (plan pixels) ----------
SCO = box(747, 723, 833, 757)
CLUB = box(553, 603, 650, 663)
SUBSTATION = box(667, 715, 740, 757)
CETP = box(1083, 822, 1140, 876)
PARKS = [box(1086, 597, 1116, 752), box(653, 610, 747, 717), box(972, 335, 1000, 375), box(1050, 478, 1080, 505),
         box(855, 505, 880, 540), box(930, 505, 960, 540), box(700, 515, 722, 540), box(1010, 640, 1040, 670),
         box(735, 80, 760, 195), box(785, 80, 810, 195), box(440, 492, 520, 560)]
COMMUNITY = [box(890, 265, 924, 450), box(1050, 387, 1080, 473), box(725, 600, 745, 660)]
GATE = (712, 768)

# ---------- scale: fit the 138 acres ----------
S = 1.07  # metres per plan pixel (scale bar reads about 1.1; tuned so the site is about 138 acres)
area = SITE.area * S * S
print('site area acres', round(area / 4046.86, 1))
CX, CY = SITE.centroid.x, SITE.centroid.y
def m(p): return ((p[0] - CX) * S, -(p[1] - CY) * S)
def mpoly(g):
    return Polygon([m(p) for p in g.exterior.coords], [[m(p) for p in r.coords] for r in g.interiors])

def road_poly(pts, w):
    return LineString([m(p) for p in pts]).buffer(w / 2, cap_style=2, join_style=2)

site = mpoly(SITE) if SITE.geom_type == 'Polygon' else MultiPolygon([mpoly(g) for g in SITE.geoms])
roads = unary_union([road_poly(p, w) for p, w in R]).intersection(site.buffer(1))
special = {k: mpoly(v) for k, v in dict(SCO=SCO, CLUB=CLUB, SUBSTATION=SUBSTATION, CETP=CETP).items()}
parks = unary_union([mpoly(p) for p in PARKS]).intersection(site)
community = [mpoly(c) for c in COMMUNITY]
raste = road_poly(*RASTE); meham = road_poly(*MEHAM); drain = road_poly(*DRAIN)

blocks = site.difference(roads.buffer(1.5)).difference(parks).difference(unary_union(list(special.values()) + community))
blocks = [b for b in (blocks.geoms if hasattr(blocks, 'geoms') else [blocks]) if b.area > 150]

def zone(c):
    x, y = c.x / S + CX, -c.y / S + CY
    if y < 240:
        if x < 640 or (640 <= x < 668): return 'ind_big'
        if 700 < x < 810 and y > 200: return 'com'
        return 'res'
    if x > 1150 or y > 776: return 'ind'
    return 'res'

PRE_T = []  # trees planted while filling blocks
B = []   # buildings: kind, cx, cy, w, d, h, rot
def add(kind, cx, cy, w, d, h, rot=0.0): B.append(dict(k=kind, x=round(cx, 2), y=round(cy, 2), w=round(w, 2), d=round(d, 2), h=round(h, 2), r=round(rot, 4)))

def rect_fits(poly, cx, cy, w, d):
    return poly.buffer(0.3).contains(box(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2))

def fill_block(b, kind):
    minx, miny, maxx, maxy = b.bounds
    W, H = maxx - minx, maxy - miny
    vertical = H >= W          # long axis
    L, Sd = (H, W) if vertical else (W, H)
    if kind == 'res':
        rows = 2 if Sd >= 24 else 1
        depth = Sd / rows
        hd = min(12.0, depth - 3.0)
        if hd < 6: return
        step = 7.0
        n = int((L - 2) // step)
        off0 = (L - n * step) / 2
        for r in range(rows):
            for i in range(n):
                t = off0 + step * (i + 0.5)
                # front of the house towards the road (outer edge of the block)
                s = (2.0 + hd / 2) if r == 0 else (Sd - 2.0 - hd / 2)
                if vertical: cx, cy, w, d = minx + s, miny + t, hd, 6.3
                else: cx, cy, w, d = minx + t, miny + s, 6.3, hd
                if rect_fits(b, cx, cy, w, d):
                    add('res', cx, cy, w, d, random.choice([8.6, 9.2, 9.8, 10.4]))
        if rows == 2:
            k = 0.0
            while k < L:
                if vertical: PRE_T.append((minx + Sd / 2, miny + k))
                else: PRE_T.append((minx + k, miny + Sd / 2))
                k += random.choice([10, 13, 16])
    elif kind in ('ind', 'ind_big'):
        big = kind == 'ind_big' or b.area > 9000
        rows = 2 if Sd >= (90 if big else 56) else 1
        depth = Sd / rows
        t = 0.0
        while t < L - 12:
            front = random.choice([60, 75, 90]) if big else random.choice([22, 26, 30, 36])
            front = min(front, L - t)
            if front < 14: break
            for r in range(rows):
                sw, sd = front - 6, depth - (14 if big else 9)
                if sd < 8: continue
                s = (depth / 2 + 2) if r == 0 else (Sd - depth / 2 - 2)
                tc = t + front / 2
                if vertical: cx, cy, w, d = minx + s, miny + tc, sd, sw
                else: cx, cy, w, d = minx + tc, miny + s, sw, sd
                if rect_fits(b, cx, cy, w, d):
                    add('shed', cx, cy, w, d, random.choice([9.5, 10.5, 11.5]) + (2 if big else 0))
                elif rect_fits(b, cx, cy, w * 0.7, d * 0.7):
                    add('shed', cx, cy, w * 0.7, d * 0.7, 9.5)
            t += front
    elif kind == 'com':
        add('sco', b.centroid.x, b.centroid.y, W * 0.9, H * 0.6, 13.5)

import numpy as np
from PIL import Image as _I, ImageDraw as _D
def pack(poly, sizes, gap=2.0, step=2):
    inner = poly.buffer(-1.5)
    if inner.is_empty: return []
    minx, miny, maxx, maxy = inner.bounds
    W, H = int(maxx - minx) + 2, int(maxy - miny) + 2
    img = _I.new('L', (W, H), 0); d = _D.Draw(img)
    for g in (inner.geoms if hasattr(inner, 'geoms') else [inner]):
        d.polygon([(x - minx, y - miny) for x, y in g.exterior.coords], fill=1)
        for r in g.interiors: d.polygon([(x - minx, y - miny) for x, y in r.coords], fill=0)
    ok = np.array(img, dtype=np.int32)
    occ = np.zeros_like(ok)
    out = []
    for cw, cd in sizes:
        cw_, cd_ = int(cw), int(cd)
        for y in range(0, H - cd_, step):
            for x in range(0, W - cw_, step):
                if ok[y:y + cd_, x:x + cw_].all() and not occ[y:y + cd_, x:x + cw_].any():
                    out.append((minx + x, miny + y, cw, cd))
                    g = int(gap)
                    occ[max(0, y - g):y + cd_ + g, max(0, x - g):x + cw_ + g] = 1
    return out

def tile_block(b, kind):
    big = kind == 'ind_big'
    sizes = [(80, 52), (52, 80), (64, 46), (46, 64)] if big else [(36, 26), (26, 36), (30, 22), (22, 30), (24, 18), (18, 24)]
    cells = pack(b, sizes, gap=2 if big else 1)
    for x, y, cw, cd in cells:
        iw, idp = (8, 10) if big else (5, 7)
        h = random.choice([9.5, 10.5, 11.5]) + (2.5 if big else 0)
        if big or min(cw, cd) < 20:
            add('shed', x + cw / 2, y + cd / 2, cw - iw, cd - idp, h)
        else:
            add('shed', x + cw / 2, y + cd / 2 + 1.5, cw - iw, cd - idp - 3, h)
            add('office', x + cw / 2, y + 3.2, min(10, cw - iw), 4.5, 7.2)
    return len(cells)

BIGZ = unary_union([mpoly(box(400, 170, 668, 240)), mpoly(box(1160, 250, 1256, 425)), mpoly(box(1255, 505, 1555, 618))])
COM2 = mpoly(box(700, 200, 812, 240))
parts = []
for b in blocks:
    for g, z in ((b.intersection(BIGZ), 'ind_big'), (b.intersection(COM2), 'com'), (b.difference(BIGZ).difference(COM2), None)):
        for q in (g.geoms if hasattr(g, 'geoms') else [g]):
            if q.geom_type == 'Polygon' and q.area > 150:
                parts.append((q, z or zone(q.centroid)))
for b, z in parts:
    minx, miny, maxx, maxy = b.bounds
    regular = b.area / ((maxx - minx) * (maxy - miny)) > 0.88
    if z in ('ind', 'ind_big'):
        tile_block(b, z)
    elif regular or z == 'com':
        fill_block(b, z)
    else:
        n0 = len(B); fill_block(b, z)
        if len(B) - n0 < b.area / 260:   # irregular residential block: tile it instead
            del B[n0:]
            for x, y, cw, cd in pack(b, [(7, 13), (13, 7)], gap=1):
                if cw < cd: add('res', x + 3.5, y + 6.5, 6.3, 11.5, random.choice([8.6, 9.2, 9.8, 10.4]))
                else: add('res', x + 6.5, y + 3.5, 11.5, 6.3, random.choice([8.6, 9.2, 9.8, 10.4]))

# SCO row: 22 shops, ground plus three floors
sco = special['SCO']; minx, miny, maxx, maxy = sco.bounds
n = 22; wsc = (maxx - minx) / n
for i in range(n):
    add('sco', minx + wsc * (i + 0.5), (miny + maxy) / 2 + 2, wsc - 0.4, (maxy - miny) * 0.62, random.choice([13.2, 13.6]))
# club: clubhouse, pool, courts
c = special['CLUB']; minx, miny, maxx, maxy = c.bounds; cw, ch = maxx - minx, maxy - miny
add('club', minx + cw * 0.3, miny + ch * 0.68, cw * 0.42, ch * 0.42, 9)
POOL = dict(x=minx + cw * 0.3, y=miny + ch * 0.24, w=cw * 0.36, d=ch * 0.22)
COURTS = [dict(x=minx + cw * 0.72, y=miny + ch * (0.25 + 0.27 * i), w=cw * 0.34, d=ch * 0.2) for i in range(3)]
# substation, CETP, community buildings
s_ = special['SUBSTATION']; minx, miny, maxx, maxy = s_.bounds
for i in range(4):
    add('util', minx + (maxx - minx) * (0.15 + 0.22 * i), (miny + maxy) / 2, 7, 9, 5)
add('club', (minx + maxx) / 2, miny + 6, (maxx - minx) * 0.8, 8, 6)
ce = special['CETP']; minx, miny, maxx, maxy = ce.bounds
TANKS = [dict(x=minx + (maxx - minx) * fx, y=miny + (maxy - miny) * fy, r=11) for fx in (0.3, 0.72) for fy in (0.3, 0.72)]
for cm in community:
    minx, miny, maxx, maxy = cm.bounds
    L = max(maxx - minx, maxy - miny); vert = (maxy - miny) > (maxx - minx)
    k = max(1, int(L // 45))
    for i in range(k):
        t = (i + 0.5) / k
        if vert: add('club', (minx + maxx) / 2, miny + (maxy - miny) * t, (maxx - minx) * 0.7, min(30, (maxy - miny) / k * 0.6), 8)
        else: add('club', minx + (maxx - minx) * t, (miny + maxy) / 2, min(30, (maxx - minx) / k * 0.6), (maxy - miny) * 0.7, 8)

# ---------- trees ----------
T = []
bld = unary_union([box(b['x'] - b['w'] / 2, b['y'] - b['d'] / 2, b['x'] + b['w'] / 2, b['y'] + b['d'] / 2) for b in B]).buffer(1.5)
water = unary_union([box(p['x'] - p['w'] / 2, p['y'] - p['d'] / 2, p['x'] + p['w'] / 2, p['y'] + p['d'] / 2) for p in [POOL] + COURTS])
def tree(x, y, big=False):
    p = Point(x, y)
    if not site.contains(p) or bld.contains(p) or water.buffer(2).contains(p): return
    T.append(dict(x=round(x, 2), y=round(y, 2), r=round(random.uniform(2.6, 3.6) * (1.25 if big else 1), 2), h=round(random.uniform(6.5, 9), 2)))
for x, y in PRE_T: tree(x, y)
for b, z in parts:
    if z != 'res': continue
    mnx, mny, mxx, mxy = b.bounds
    for _ in range(int(b.area / 420)):
        x, y = random.uniform(mnx, mxx), random.uniform(mny, mxy)
        if b.contains(Point(x, y)): tree(x, y)
for pts, w in R:
    ln = LineString([m(p) for p in pts])
    for side in (-1, 1):
        o = ln.parallel_offset(w / 2 + 2.2, 'left' if side < 0 else 'right')
        d = 0.0
        while d < o.length:
            pt = o.interpolate(d); tree(pt.x, pt.y, big=w >= 18); d += (11 if w >= 18 else 15)
geoms = site.geoms if hasattr(site, 'geoms') else [site]
for g in geoms:
    ring = g.exterior.buffer(-4).exterior if g.exterior.buffer(-4).geom_type == 'Polygon' else None
    if ring is None:
        continue
    d = 0.0
    while d < ring.length:
        pt = ring.interpolate(d); tree(pt.x, pt.y, big=True); d += 9
for pk in (parks.geoms if hasattr(parks, 'geoms') else [parks]):
    minx, miny, maxx, maxy = pk.bounds
    n = int(pk.area / 160)
    for _ in range(n):
        x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        if pk.buffer(-3).contains(Point(x, y)): tree(x, y)

def coords(g):
    gs = g.geoms if hasattr(g, 'geoms') else [g]
    return [[list(map(lambda c: [round(c[0], 2), round(c[1], 2)], p.exterior.coords))] + [list(map(lambda c: [round(c[0], 2), round(c[1], 2)], r.coords)) for r in p.interiors] for p in gs if p.area > 1]

plinth = unary_union([site, raste.intersection(box(*site.buffer(40).bounds)), meham.intersection(site.buffer(45)), drain.intersection(site.buffer(45))]).buffer(12, join_style=2).buffer(-4, join_style=2)
plinth = max(plinth.geoms, key=lambda g: g.area) if hasattr(plinth, 'geoms') else plinth
gate = m(GATE)
out = dict(scale=S, plinth=coords(plinth), site=coords(site), roads=coords(roads), raste=coords(raste.intersection(plinth)),
           meham=coords(meham.intersection(plinth)), drain=coords(drain.intersection(plinth)), parks=coords(parks), holes=coords(unary_union([mpoly(h) for h in HOLES])),
           pads=coords(unary_union(blocks).buffer(0)), buildings=B, trees=T, pool=POOL, courts=COURTS, tanks=TANKS, gate=[round(gate[0], 2), round(gate[1], 2)])
import shapely
out['radius'] = round(max(math.hypot(x, y) for x, y in plinth.exterior.coords), 1)
json.dump(out, open('/home/claude/fit3d/layout.json', 'w'))
print('buildings', len(B), {k: sum(1 for b in B if b['k'] == k) for k in set(b['k'] for b in B)}, 'trees', len(T))

# ---------- overlay check ----------
from PIL import Image, ImageDraw
im = Image.open('/home/claude/trueyards/public/fit/FIT-Site-Plan-138-Acres.jpg').convert('RGB').resize((1600, 1129))
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
def px(p): return (p[0] / S + CX, -p[1] / S + CY)
for g in (roads.geoms if hasattr(roads, 'geoms') else [roads]):
    d.polygon([px(c) for c in g.exterior.coords], fill=(60, 60, 60, 90))
for b in B:
    col = {'res': (255, 255, 255, 220), 'shed': (20, 40, 90, 220), 'office': (240, 240, 240, 240), 'sco': (200, 150, 60, 230), 'club': (220, 60, 60, 230), 'util': (120, 120, 120, 230)}[b['k']]
    d.rectangle([px((b['x'] - b['w'] / 2, b['y'] + b['d'] / 2)), px((b['x'] + b['w'] / 2, b['y'] - b['d'] / 2))], fill=col)
for t in T:
    x, y = px((t['x'], t['y'])); d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(30, 140, 50, 230))
for g in geoms:
    d.line([px(c) for c in g.exterior.coords], fill=(255, 0, 0, 255), width=2)
Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save('/home/claude/fit3d/overlay.png')
