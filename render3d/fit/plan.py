"""Top-down plan render of the FIT township (exact layout from site plan D5) set in farmland, plus zone ID masks.
Renders in horizontal tiles so 20 machines can share one 4K frame.
Usage: python3 plan.py --layout layout.json --out tiles --w 3600 --h 3600 --samples 96 --tiles 20 --only 0,1   (beauty)
       python3 plan.py ... --id industrial|residential|commercial   (flat white-on-black mask of that zone)
Based on build.py.
Usage: python3 build.py --layout layout.json --out frames/ --frames 96 --first 0 --last 95 --w 1600 --h 1280 --samples 64
       python3 build.py ... --still 0 (renders one frame)   --blend model.blend (also saves the scene)"""
import argparse, json, math, os, random, sys
import bpy, bmesh
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument('--layout', default='layout.json'); ap.add_argument('--out', default='frames')
ap.add_argument('--frames', type=int, default=96); ap.add_argument('--first', type=int, default=0); ap.add_argument('--last', type=int, default=-1)
ap.add_argument('--w', type=int, default=1600); ap.add_argument('--h', type=int, default=1200)
ap.add_argument('--samples', type=int, default=64); ap.add_argument('--still', type=int, default=-1)
ap.add_argument('--blend', default=''); ap.add_argument('--only', default=''); ap.add_argument('--start_deg', type=float, default=-35.0)
ap.add_argument('--elev', type=float, default=34.0); ap.add_argument('--lens', type=float, default=70.0)
ap.add_argument('--dist', type=float, default=3260.0); ap.add_argument('--shift', type=float, default=-0.059)
ap.add_argument('--tiles', type=int, default=1); ap.add_argument('--obl', type=float, default=0.0); ap.add_argument('--tag', default=''); ap.add_argument('--azim', type=float, default=0.0); ap.add_argument('--id', default=''); ap.add_argument('--scale', type=float, default=1560.0)
ap.add_argument('--cx', type=float, default=-60.0); ap.add_argument('--cy', type=float, default=30.0)
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
L = json.load(open(A.layout))
random.seed(11)

# ---------- the site stops at the drain: nothing of FIT lies on the Meham-Beri road side (site plan D5) ----------
from shapely.geometry import Polygon, MultiPolygon, mapping
from shapely.ops import unary_union
_d0, _d1 = L['drain'][0][0][0], L['drain'][0][0][1]
_ux, _uy = _d1[0] - _d0[0], _d1[1] - _d0[1]; _ln = math.hypot(_ux, _uy); _ux, _uy = _ux / _ln, _uy / _ln; _nx, _ny = -_uy, _ux
_mp = [p for poly in L['meham'] for ring in poly for p in ring]
_side = 1 if sum((p[0] - _d0[0]) * _nx + (p[1] - _d0[1]) * _ny for p in _mp) > 0 else -1
def _t(x, y): return ((x - _d0[0]) * _nx + (y - _d0[1]) * _ny) * _side
_far = 5000
_o = 2.0
_hp = Polygon([(_d0[0] + _nx * _side * _o - _ux * _far, _d0[1] + _ny * _side * _o - _uy * _far), (_d0[0] + _nx * _side * _o + _ux * _far, _d0[1] + _ny * _side * _o + _uy * _far),
               (_d0[0] + _nx * _side * _far + _ux * _far, _d0[1] + _ny * _side * _far + _uy * _far), (_d0[0] + _nx * _side * _far - _ux * _far, _d0[1] + _ny * _side * _far - _uy * _far)])
def _clip(polys):
    out = []
    for poly in polys:
        g = Polygon(poly[0], poly[1:]).buffer(0).difference(_hp)
        for p in (g.geoms if hasattr(g, 'geoms') else [g]):
            if p.is_empty or p.area < 4: continue
            out.append([list(map(list, p.exterior.coords))] + [list(map(list, r.coords)) for r in p.interiors])
    return out
for k in ('plinth', 'site', 'pads', 'roads', 'parks', 'holes'):
    if k in L: L[k] = _clip(L[k])
L['buildings'] = [b for b in L['buildings'] if _t(b['x'], b['y']) < -2 - min(b['w'], b['d']) / 2]
L['trees'] = [t for t in L['trees'] if _t(t['x'], t['y']) < -2]
print('clipped to the drain line', flush=True)
os.makedirs(A.out, exist_ok=True); json.dump(L, open(os.path.join(A.out, 'layout_clipped.json'), 'w')) if not A.id else None

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------- materials ----------
def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c] + [a]
def mat(name, col, rough=0.75, metal=0.0, spec=0.35, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexc(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = spec
    if coat and 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = coat
    return m
M = dict(
    lawn=mat('lawn', '#A9BB8A', 0.9), park=mat('park', '#8EAD69', 0.9), pad=mat('pad', '#ECE7DB', 0.85),
    road=mat('road', '#8C8F94', 0.8), asphalt=mat('asphalt', '#86898E', 0.8), field=mat('field', '#CFC6A4', 0.95),
    water=mat('water', '#7FB4CC', 0.08, spec=0.6), pool=mat('pool', '#5BC0E0', 0.05, spec=0.7), court=mat('court', '#6FA57A', 0.7),
    wall=mat('wall', '#F5F2EC', 0.6), wall2=mat('wall2', '#E9E1D3', 0.6), roof=mat('roof', '#DDD7CC', 0.7), roof2=mat('roof2', '#CFC8BB', 0.7),
    shedwall=mat('shedwall', '#D6DADF', 0.55), shedroof=mat('shedroof', '#23395B', 0.45, spec=0.5),
    glass=mat('glass', '#3E4E63', 0.15, spec=0.6), stone=mat('stone', '#E6D6BB', 0.6), steel=mat('steel', '#B8BEC6', 0.35, metal=0.6),
    leaf1=mat('leaf1', '#557F41', 0.85), leaf2=mat('leaf2', '#66904B', 0.85), leaf3=mat('leaf3', '#47703C', 0.85), trunk=mat('trunk', '#6B5643', 0.9),
    marking=mat('marking', '#F7F5EF', 0.6), brass=mat('brass', '#B8955A', 0.35, metal=0.7),
)
# soil strata for the plinth sides (bands by height)
soil = bpy.data.materials.new('soil'); soil.use_nodes = True
nt = soil.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.95
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 0.02; mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
nt.links.new(tc.outputs['Object'], sep.inputs[0]); nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
mix.inputs[1].default_value = 3.0
nt.links.new(noise.outputs['Fac'], mix.inputs[0]); nt.links.new(sep.outputs['Z'], mix.inputs[2])
mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -46; mr.inputs['From Max'].default_value = 1.5
nt.links.new(mix.outputs[0], mr.inputs['Value']); nt.links.new(mr.outputs[0], ramp.inputs['Fac'])
cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
bands = [(0.0, '#5E4636'), (0.14, '#7A5A43'), (0.3, '#9C6B4C'), (0.44, '#B98A62'), (0.56, '#8C5F45'), (0.7, '#A77452'), (0.84, '#6E513D'), (0.95, '#7E9A5E')]
cr.elements[0].position = bands[0][0]; cr.elements[0].color = hexc(bands[0][1])
cr.elements[1].position = bands[1][0]; cr.elements[1].color = hexc(bands[1][1])
for p, c in bands[2:]:
    e = cr.elements.new(p); e.color = hexc(c)
nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
M['soil'] = soil

root = bpy.data.objects.new('FIT', None); sc.collection.objects.link(root)

def new_obj(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.parent = root
    return ob

def poly_faces(bm, polys, z, mi=0, extrude=0.0, side_mi=None):
    """Fill polygons (with holes) at height z; optionally extrude down by `extrude` with side material."""
    for poly in polys:
        edges = []
        for ring in poly:
            pts = ring[:-1] if ring[0] == ring[-1] else ring
            vs = [bm.verts.new((p[0], p[1], z)) for p in pts]
            for i in range(len(vs)): edges.append(bm.edges.new((vs[i], vs[(i + 1) % len(vs)])))
        res = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=edges)
        faces = [f for f in res['geom'] if isinstance(f, bmesh.types.BMFace)]
        for f in faces:
            f.material_index = mi
            if f.normal.z < 0: f.normal_flip()
        if extrude:
            ex = bmesh.ops.extrude_face_region(bm, geom=faces)
            nv = [v for v in ex['geom'] if isinstance(v, bmesh.types.BMVert)]
            for v in nv: v.co.z -= extrude
            for f in ex['geom']:
                if isinstance(f, bmesh.types.BMFace): f.material_index = side_mi if side_mi is not None else mi
            # the original top faces stay; flip the bottom
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])

def flat(name, polys, z, m, extrude=0.0):
    bm = bmesh.new(); poly_faces(bm, polys, z, 0, extrude); return new_obj(name, bm, [m])

# ---------- ground ----------
BASE = 0.6
bm = bmesh.new(); poly_faces(bm, L['plinth'], 0.0, 0, BASE, side_mi=1)
for f in bm.faces:
    if abs(f.normal.z) < 0.5: f.material_index = 1
new_obj('plinth', bm, [M['lawn'], M['soil']])
flat('pads', L['pads'], 0.22, M['pad'], 0.2)
flat('roads', L['roads'], 0.12, M['road'], 0.1)
flat('parks', L['parks'], 0.32, M['park'], 0.3)
flat('fields', L['holes'], 0.08, M['field'], 0.06)
flat('raste', L['raste'], 0.12, M['asphalt'], 0.1)
flat('meham', L['meham'], 0.14, M['asphalt'], 0.12)
flat('drain', L['drain'], -0.6, M['water'])

# ---------- buildings ----------
def box(bm, cx, cy, z0, w, d, h, rot=0.0, mi=0, top_mi=None):
    r = bmesh.ops.create_cube(bm, size=1.0)
    vs = r['verts']
    for v in vs:
        v.co.x = cx + v.co.x * w; v.co.y = cy + v.co.y * d; v.co.z = z0 + (v.co.z + 0.5) * h
    fs = {f for v in vs for f in v.link_faces}
    for f in fs:
        f.material_index = top_mi if (top_mi is not None and f.normal.z > 0.5) else mi
    return fs

bm = bmesh.new()   # houses: walls 0, wall2 1, roof 2, glass 3
for b in L['buildings']:
    if b['k'] != 'res': continue
    mi = 0 if random.random() < 0.72 else 1
    h = b['h']
    rm = 2 if random.random() < 0.6 else 4
    box(bm, b['x'], b['y'], 0.3, b['w'], b['d'], h, mi=mi, top_mi=rm)
    # glass band on the street side and a small terrace block
    if b['w'] < b['d']:
        box(bm, b['x'] + (b['w'] / 2) * random.choice([-1, 1]), b['y'], 3.4, 0.25, b['d'] * 0.7, 2.3, mi=3)
    else:
        box(bm, b['x'], b['y'] + (b['d'] / 2) * random.choice([-1, 1]), 3.4, b['w'] * 0.7, 0.25, 2.3, mi=3)
    box(bm, b['x'] + random.uniform(-1, 1), b['y'] + random.uniform(-1, 1), 0.3 + h, b['w'] * 0.45, b['d'] * 0.4, 2.6, mi=mi, top_mi=rm)
houses = new_obj('houses', bm, [M['wall'], M['wall2'], M['roof'], M['glass'], M['roof2']])

bm = bmesh.new()   # industrial: shed wall 0, roof 1, office wall 2, glass 3, skylights 4
for b in L['buildings']:
    if b['k'] == 'shed':
        box(bm, b['x'], b['y'], 0.3, b['w'], b['d'], b['h'], mi=0, top_mi=1)
        # roof ridge lines (skylights) along the long side
        n = max(2, int(max(b['w'], b['d']) // 14))
        for i in range(n):
            t = (i + 0.5) / n - 0.5
            if b['w'] >= b['d']: box(bm, b['x'] + t * b['w'], b['y'], 0.3 + b['h'], 1.2, b['d'] * 0.8, 0.35, mi=4)
            else: box(bm, b['x'], b['y'] + t * b['d'], 0.3 + b['h'], b['w'] * 0.8, 1.2, 0.35, mi=4)
    elif b['k'] == 'office':
        box(bm, b['x'], b['y'], 0.3, b['w'], b['d'], b['h'], mi=2, top_mi=2)
        box(bm, b['x'], b['y'] - b['d'] / 2, 2.6, b['w'] * 0.85, 0.2, 3.2, mi=3)
new_obj('industry', bm, [M['shedwall'], M['shedroof'], M['wall'], M['glass'], M['steel']])

bm = bmesh.new()   # SCO, club, utility: stone 0, glass 1, wall 2, steel 3
for b in L['buildings']:
    if b['k'] == 'sco':
        continue
    if False:
        fh = b['h'] / 4
        for f in range(4):
            box(bm, b['x'], b['y'], 0.3 + f * fh, b['w'], b['d'], fh * 0.62, mi=1)
            box(bm, b['x'], b['y'], 0.3 + f * fh + fh * 0.62, b['w'], b['d'], fh * 0.38, mi=0)
        box(bm, b['x'] - b['w'] / 2 + 0.15, b['y'], 0.3, 0.3, b['d'] + 0.2, b['h'] + 0.6, mi=0)
    elif b['k'] == 'club':
        box(bm, b['x'], b['y'], 0.3, b['w'], b['d'], b['h'] * 0.5, mi=1)
        box(bm, b['x'], b['y'], 0.3 + b['h'] * 0.5, b['w'] * 1.04, b['d'] * 1.04, b['h'] * 0.5, mi=2)
    elif b['k'] == 'util':
        box(bm, b['x'], b['y'], 0.3, b['w'], b['d'], b['h'], mi=3)
new_obj('civic', bm, [M['stone'], M['glass'], M['wall'], M['steel']])
bm = bmesh.new()   # SCO blocks on their own (commercial zone)
for b in L['buildings']:
    if b['k'] != 'sco': continue
    fh = b['h'] / 4
    for f in range(4):
        box(bm, b['x'], b['y'], 0.3 + f * fh, b['w'], b['d'], fh * 0.62, mi=1)
        box(bm, b['x'], b['y'], 0.3 + f * fh + fh * 0.62, b['w'], b['d'], fh * 0.38, mi=0)
    box(bm, b['x'], b['y'], 0.3 + b['h'], b['w'] * 0.96, b['d'] * 0.9, 0.5, mi=2)
new_obj('sco', bm, [M['stone'], M['glass'], M['wall'], M['steel']])

bm = bmesh.new()
p = L['pool']; box(bm, p['x'], p['y'], 0.2, p['w'], p['d'], 0.4, mi=0)
box(bm, p['x'], p['y'], 0.15, p['w'] + 5, p['d'] + 5, 0.35, mi=2)
for c in L['courts']: box(bm, c['x'], c['y'], 0.2, c['w'], c['d'], 0.3, mi=1)
for t in L['tanks']:
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=40, radius1=t['r'], radius2=t['r'], depth=3.0)
    for v in r['verts']: v.co += Vector((t['x'], t['y'], 1.8))
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = 3 if f.normal.z > 0.5 else 4
new_obj('amenity', bm, [M['pool'], M['court'], M['stone'], M['water'], M['wall']])

# gate: a brass-trimmed portal at the entrance
bm = bmesh.new(); gx, gy = L['gate']
box(bm, gx - 9, gy, 0.3, 2.2, 2.2, 9, mi=0); box(bm, gx + 9, gy, 0.3, 2.2, 2.2, 9, mi=0); box(bm, gx, gy, 9.3, 22, 3.2, 1.8, mi=1)
new_obj('gate', bm, [M['stone'], M['brass']])

# ---------- trees ----------
bm = bmesh.new()
for t in L['trees']:
    k = random.choice([0, 1, 2])
    r = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=t['r'])
    sq = random.uniform(0.85, 1.05)
    for v in r['verts']:
        v.co.z *= sq; v.co += Vector((t['x'], t['y'], t['h'] - t['r'] * 0.3))
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
    c = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.35, radius2=0.25, depth=t['h'] - t['r'])
    for v in c['verts']: v.co += Vector((t['x'], t['y'], (t['h'] - t['r']) / 2 + 0.3))
    for f in {f for v in c['verts'] for f in v.link_faces}: f.material_index = 3
trees = new_obj('trees', bm, [M['leaf1'], M['leaf2'], M['leaf3'], M['trunk']])
for poly in trees.data.polygons: poly.use_smooth = True

# soft bevels on buildings catch light at the edges like a real model
for name in ('houses', 'industry', 'civic', 'sco'):
    ob = bpy.data.objects[name]
    mod = ob.modifiers.new('bevel', 'BEVEL'); mod.width = 0.18; mod.segments = 1; mod.limit_method = 'ANGLE'

# ---------- surroundings: farmland, hedgerows, roads that run on past the site ----------
def rings(polys):
    return [ring for poly in polys for ring in poly[:1]]
SITE = rings(L['plinth'])
def inside(x, y, rs):
    for ring in rs:
        c = False; n = len(ring)
        for i in range(n - 1):
            (x1, y1), (x2, y2) = ring[i], ring[i + 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1: c = not c
        if c: return True
    return False
def near_site(x, y, m=14):
    return any(inside(x + dx, y + dy, SITE) for dx, dy in ((0, 0), (m, 0), (-m, 0), (0, m), (0, -m)))

HALF = A.scale / 2 + 60 if A.obl <= 0 else A.scale * 1.1 + 400
X0, X1, Y0, Y1 = A.cx - HALF, A.cx + HALF, A.cy - HALF, A.cy + HALF

# Meham-Beri road and the drain run on past the site, along the drain's line
d0, d1 = L['drain'][0][0][0], L['drain'][0][0][1]
dx, dy = d1[0] - d0[0], d1[1] - d0[1]; ln = math.hypot(dx, dy); ux, uy = dx / ln, dy / ln; nx, ny = -uy, ux
mpts = [p for poly in L['meham'] for ring in poly for p in ring]
mc = (sum(p[0] for p in mpts) / len(mpts), sum(p[1] for p in mpts) / len(mpts))
off = (mc[0] - d0[0]) * nx + (mc[1] - d0[1]) * ny
dc = [((p[0] - d0[0]) * nx + (p[1] - d0[1]) * ny) for p in mpts]
half_w = (max(dc) - min(dc)) / 2 if max(dc) - min(dc) < 60 else 12.0
mid = (max(dc) + min(dc)) / 2
def strip(o, w, t0=-1800, t1=1800):
    a = (d0[0] + nx * o, d0[1] + ny * o)
    return [[[a[0] + ux * t0 + nx * w, a[1] + uy * t0 + ny * w], [a[0] + ux * t1 + nx * w, a[1] + uy * t1 + ny * w],
             [a[0] + ux * t1 - nx * w, a[1] + uy * t1 - ny * w], [a[0] + ux * t0 - nx * w, a[1] + uy * t0 - ny * w],
             [a[0] + ux * t0 + nx * w, a[1] + uy * t0 + ny * w]]]
flat('meham_ext', [strip(mid, max(half_w, 10.0))], 0.1, M['asphalt'], 0.1)
# the drain runs along the road to its north-west end, then turns north as the canal (site plan D5)
_tend = (d1[0] - d0[0]) * ux + (d1[1] - d0[1]) * uy
flat('drain_ext', [strip(0.0, 4.0, -1800, _tend)], 0.02, M['water'])
_cx = d1[0] - 70.0
flat('canal_turn', [[[[d1[0] - 4, d1[1] - 4], [d1[0] + 4, d1[1] + 4], [_cx + 4, d1[1] + 30], [_cx - 4, d1[1] + 22], [d1[0] - 4, d1[1] - 4]]]], 0.02, M['water'])
flat('canal', [[[[_cx - 4, d1[1] + 22], [_cx + 4, d1[1] + 22], [_cx + 4, A.cy + HALF + 400], [_cx - 4, A.cy + HALF + 400], [_cx - 4, d1[1] + 22]]]], 0.02, M['water'])
# dashed centre line and edge lines on the highway
bm = bmesh.new()
for t in range(-1800, 1800, 14):
    cx_ = d0[0] + nx * mid + ux * t; cy_ = d0[1] + ny * mid + uy * t
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r['verts']:
        lx, ly, lz = v.co.x * 6.0, v.co.y * 0.35, v.co.z * 0.05
        v.co = Vector((cx_ + ux * lx + nx * ly, cy_ + uy * lx + ny * ly, 0.24 + lz))
new_obj('marks', bm, [M['marking']])
# the 7K rasta along the north edge runs on to the frame edges
ry0 = min(p[1] for p in L['raste'][0][0]); ry1 = max(p[1] for p in L['raste'][0][0])
# the 7K rasta runs east to the frame edge (to Patwapur); at its west end it turns south and meets the Meham-Beri road
_rx0 = min(p[0] for p in L['raste'][0][0])
flat('raste_ext', [[[[_rx0, ry0], [X1, ry0], [X1, ry1], [_rx0, ry1], [_rx0, ry0]]]], 0.11, M['asphalt'], 0.1)
# where the line x = _rx0 meets the highway centre line
_tj = ((_rx0 + 6) - (d0[0] + nx * mid)) / ux if abs(ux) > 1e-6 else 0
_yj = d0[1] + ny * mid + uy * _tj
flat('raste_link', [[[[_rx0, _yj], [_rx0 + 11, _yj], [_rx0 + 11, ry1], [_rx0, ry1], [_rx0, _yj]]]], 0.11, M['asphalt'], 0.1)

random.seed(7)
def on_road(x, y):
    t = (x - d0[0]) * nx + (y - d0[1]) * ny
    if abs(t - mid) < half_w + 4 or abs(t) < 6: return True
    if ry0 - 4 < y < ry1 + 4 and x > min(p[0] for p in L['raste'][0][0]) - 6: return True
    if min(p[0] for p in L['raste'][0][0]) - 6 < x < min(p[0] for p in L['raste'][0][0]) + 17 and y < ry1 + 4: return True
    if abs(x - (L['drain'][0][0][1][0] - 70.0)) < 9 and y > L['drain'][0][0][1][1]: return True
    return False
# farmland: a grid of rectangular killa fields split into strips, each with its own crop and furrow direction
crops = ['#6B8C3C', '#7A9A44', '#86A24D', '#5E8036', '#94AC5C', '#A3B468', '#7F9A4A', '#9A8360', '#A88F6C', '#B5A27A', '#BFB24E', '#718F43']
weights = [10, 10, 9, 8, 6, 5, 8, 5, 4, 3, 2, 8]
fm = bpy.data.materials.new('farm'); fm.use_nodes = True; nt = fm.node_tree; N = nt.nodes; Lk = nt.links.new
pb = N['Principled BSDF']; pb.inputs['Roughness'].default_value = 0.96
at = N.new('ShaderNodeAttribute'); at.attribute_name = 'Col'
ad = N.new('ShaderNodeAttribute'); ad.attribute_name = 'D'; ad.attribute_type = 'GEOMETRY'
tc = N.new('ShaderNodeTexCoord')
wx = N.new('ShaderNodeTexWave'); wx.bands_direction = 'X'; wx.inputs['Scale'].default_value = 0.18; wx.inputs['Distortion'].default_value = 0.6
wy = N.new('ShaderNodeTexWave'); wy.bands_direction = 'Y'; wy.inputs['Scale'].default_value = 0.18; wy.inputs['Distortion'].default_value = 0.6
Lk(tc.outputs['Object'], wx.inputs['Vector']); Lk(tc.outputs['Object'], wy.inputs['Vector'])
mw = N.new('ShaderNodeMix'); mw.data_type = 'RGBA'; Lk(ad.outputs['Fac'], mw.inputs['Factor']); Lk(wx.outputs['Color'], mw.inputs['A']); Lk(wy.outputs['Color'], mw.inputs['B'])
m1 = N.new('ShaderNodeMix'); m1.data_type = 'RGBA'; m1.blend_type = 'MULTIPLY'; m1.inputs['Factor'].default_value = 0.16
Lk(at.outputs['Color'], m1.inputs['A']); Lk(mw.outputs['Result'], m1.inputs['B'])
noise = N.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 0.05; noise.inputs['Detail'].default_value = 7
Lk(tc.outputs['Object'], noise.inputs['Vector'])
m2 = N.new('ShaderNodeMix'); m2.data_type = 'RGBA'; m2.blend_type = 'OVERLAY'; m2.inputs['Factor'].default_value = 0.28
Lk(m1.outputs['Result'], m2.inputs['A']); Lk(noise.outputs['Color'], m2.inputs['B'])
Lk(m2.outputs['Result'], pb.inputs['Base Color'])
M['farm'] = fm
# earth under everything shows through as the bunds between fields
earth = mat('earth', '#7F8650', 0.97)
bm = bmesh.new(); r = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=HALF + 300)
for v in r['verts']: v.co += Vector((A.cx, A.cy, -0.08))
new_obj('earth', bm, [earth])
KILLA = 58.0
bm = bmesh.new(); col = bm.loops.layers.color.new('Col'); dl = bm.faces.layers.float.new('D')
edges_for_trees = []
gx0 = math.floor(X0 / KILLA) * KILLA; gy0 = math.floor(Y0 / KILLA) * KILLA
xk = gx0
while xk < X1:
    yk = gy0
    while yk < Y1:
        cx_, cy_ = xk + KILLA / 2, yk + KILLA / 2
        corners = [(xk, yk), (xk + KILLA, yk), (xk, yk + KILLA), (xk + KILLA, yk + KILLA), (cx_, cy_)]
        n = random.choice([2, 2, 3, 3, 4, 5]); horiz = random.random() < 0.5
        for j in range(n):
            if horiz: x0_, x1_, y0_, y1_ = xk, xk + KILLA, yk + KILLA * j / n, yk + KILLA * (j + 1) / n
            else: x0_, x1_, y0_, y1_ = xk + KILLA * j / n, xk + KILLA * (j + 1) / n, yk, yk + KILLA
            g = 0.7
            sc_ = [(x0_, y0_), (x1_, y0_), (x0_, y1_), (x1_, y1_), ((x0_ + x1_) / 2, (y0_ + y1_) / 2)]
            if any(near_site(px, py, 3) or on_road(px, py) for px, py in sc_): continue
            vs = [bm.verts.new((x0_ + g, y0_ + g, -0.02)), bm.verts.new((x1_ - g, y0_ + g, -0.02)), bm.verts.new((x1_ - g, y1_ - g, -0.02)), bm.verts.new((x0_ + g, y1_ - g, -0.02))]
            f = bm.faces.new(vs)
            c = hexc(random.choices(crops, weights)[0])
            jit = random.uniform(-0.03, 0.03)
            for lp in f.loops: lp[col] = (max(0, c[0] + jit), max(0, c[1] + jit), max(0, c[2] + jit * 0.5), 1)
            f[dl] = 1.0 if horiz else 0.0
        if random.random() < 0.16: edges_for_trees.append(((xk, yk), (xk + KILLA, yk)))
        if random.random() < 0.16: edges_for_trees.append(((xk, yk), (xk, yk + KILLA)))
        yk += KILLA
    xk += KILLA
new_obj('farm', bm, [fm])
# grass with a little life in it for lawns and parks inside the site
for key, a, b2 in (('lawn', '#9DB57A', '#B4C48E'), ('park', '#7FA35A', '#94B76A')):
    m = M[key]; nt = m.node_tree; pb = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.08; n.inputs['Detail'].default_value = 5
    rp = nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = hexc(a); rp.color_ramp.elements[1].color = hexc(b2)
    nt.links.new(t.outputs['Object'], n.inputs['Vector']); nt.links.new(n.outputs['Fac'], rp.inputs['Fac']); nt.links.new(rp.outputs['Color'], pb.inputs['Base Color'])
# asphalt with grain
for key in ('road', 'asphalt'):
    m = M[key]; nt = m.node_tree; pb = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.6; n.inputs['Detail'].default_value = 8
    rp = nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = hexc('#6E7177'); rp.color_ramp.elements[1].color = hexc('#8F9298')
    nt.links.new(t.outputs['Object'], n.inputs['Vector']); nt.links.new(n.outputs['Fac'], rp.inputs['Fac']); nt.links.new(rp.outputs['Color'], pb.inputs['Base Color'])

# hedgerows along field edges and copses in the fields, never on the site or the roads
random.seed(7)
extra = []
for (ax_, ay_), (bx_, by_) in edges_for_trees:
    L_ = math.hypot(bx_ - ax_, by_ - ay_); t = random.uniform(0, 5)
    while t < L_:
        x = ax_ + (bx_ - ax_) * t / L_ + random.uniform(-1, 1); y = ay_ + (by_ - ay_) * t / L_ + random.uniform(-1, 1)
        if not near_site(x, y) and not on_road(x, y):
            extra.append({'x': x, 'y': y, 'r': random.uniform(2.6, 4.2), 'h': random.uniform(7, 11)})
        t += random.uniform(7, 12)
for k in range(140):
    x = random.uniform(X0, X1); y = random.uniform(Y0, Y1)
    if not near_site(x, y) and not on_road(x, y):
        extra.append({'x': x, 'y': y, 'r': random.uniform(3.2, 5.5), 'h': random.uniform(8, 13)})
for k in range(10):
    cx_ = random.uniform(X0, X1); cy_ = random.uniform(Y0, Y1); n = random.randint(6, 22)
    for i in range(n):
        x = cx_ + random.gauss(0, 14); y = cy_ + random.gauss(0, 14)
        if X0 < x < X1 and Y0 < y < Y1 and not near_site(x, y) and not on_road(x, y):
            extra.append({'x': x, 'y': y, 'r': random.uniform(3.0, 5.5), 'h': random.uniform(8, 13)})
# trees along both sides of the highway
for t in range(-1800, 1800, 9):
    for side in (-1, 1):
        o = mid + side * (half_w + random.uniform(7, 11))
        x = d0[0] + nx * o + ux * t + random.uniform(-2, 2); y = d0[1] + ny * o + uy * t + random.uniform(-2, 2)
        if X0 < x < X1 and Y0 < y < Y1 and not near_site(x, y, 6) and random.random() < 0.85:
            extra.append({'x': x, 'y': y, 'r': random.uniform(2.8, 4.6), 'h': random.uniform(8, 12)})
bm = bmesh.new()
for t in extra:
    k = random.choice([0, 1, 2])
    r = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=t['r'])
    sq = random.uniform(0.8, 1.05)
    for v in r['verts']:
        v.co.x += random.uniform(-0.25, 0.25) * t['r'] * 0.3; v.co.z *= sq; v.co += Vector((t['x'], t['y'], t['h'] - t['r'] * 0.3))
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = k
ob = new_obj('hedges', bm, [M['leaf1'], M['leaf2'], M['leaf3']])
for p in ob.data.polygons: p.use_smooth = True
print('extra trees', len(extra), flush=True)

# traffic: cars and trucks on the highway and the internal roads
car_cols = ['#F4F4F2', '#D9DCE0', '#2F3A4A', '#9A2B2B', '#C9CED6', '#1F2328', '#E8E2D4', '#3E5C76']
cm = [mat('car%d' % i, c, 0.3, spec=0.7, coat=0.6) for i, c in enumerate(car_cols)]
bm = bmesh.new()
def vehicle(x, y, ax, ay, lng, wid, hgt, mi):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r['verts']:
        lx, ly, lz = v.co.x * lng, v.co.y * wid, (v.co.z + 0.5) * hgt
        v.co = Vector((x + ax * lx - ay * ly, y + ay * lx + ax * ly, 0.25 + lz))
    for f in {f for v in r['verts'] for f in v.link_faces}: f.material_index = mi
for t in range(-1700, 1700, 1):
    if random.random() < 0.012:
        lane = random.choice([-1, 1]); o = mid + lane * half_w * 0.45
        x = d0[0] + nx * o + ux * t; y = d0[1] + ny * o + uy * t
        if X0 < x < X1 and Y0 < y < Y1:
            big = random.random() < 0.3
            vehicle(x, y, ux, uy, 12 if big else 4.4, 2.5 if big else 1.8, 3.6 if big else 1.5, random.randrange(len(cm)))
RR = rings(L['roads'])
xs = [p[0] for r_ in RR for p in r_]; ys = [p[1] for r_ in RR for p in r_]
placed = 0; tries = 0
while placed < 70 and tries < 40000:
    tries += 1
    x = random.uniform(min(xs), max(xs)); y = random.uniform(min(ys), max(ys))
    if not inside(x, y, RR): continue
    hx = inside(x + 7, y, RR) and inside(x - 7, y, RR); hy = inside(x, y + 7, RR) and inside(x, y - 7, RR)
    if hx == hy: continue
    ax, ay = (1, 0) if hx else (0, 1)
    big = random.random() < 0.25
    vehicle(x, y, ax, ay, 10 if big else 4.3, 2.4 if big else 1.8, 3.4 if big else 1.5, random.randrange(len(cm))); placed += 1
new_obj('traffic', bm, cm)

# a little more variety in house roofs (terraces, water tanks), so the residential grid reads as real homes
M['roof'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = hexc('#E4DED3')
M['roof2'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = hexc('#C9B9A3')

# ---------- light and camera: straight down, orthographic ----------
sun_d = bpy.data.lights.new('sun', 'SUN'); sun_d.energy = 4.2; sun_d.angle = math.radians(2.5); sun_d.color = (1.0, 0.96, 0.9)
sun = bpy.data.objects.new('sun', sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(-135))
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = hexc('#DCE6EE'); bg.inputs['Strength'].default_value = 0.75
cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = A.scale; cam_d.clip_start = 1; cam_d.clip_end = 20000
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
if A.obl > 0:
    # oblique aerial view: a long lens from far away, looking north-east-ish at the township
    cam_d.type = 'PERSP'; cam_d.lens = 85; cam_d.sensor_width = 36
    el = math.radians(A.obl); az = math.radians(A.azim)
    dist = A.scale * 85 / 36 * 0.98
    tgt = Vector((A.cx, A.cy, 0))
    cam.location = tgt + Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))) * dist
    cam.rotation_euler = (math.radians(90) - el, 0, -az)
else:
    cam.location = (A.cx, A.cy, 2500); cam.rotation_euler = (0, 0, 0)

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.render.resolution_x = A.w; sc.render.resolution_y = A.h; sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.image_settings.compression = 15
sc.render.threads_mode = 'AUTO'

ZONES = {'industrial': ['industry'], 'residential': ['houses'], 'commercial': ['sco']}
if A.id:
    blk = bpy.data.materials.new('idblack'); blk.use_nodes = True; nt = blk.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0, 0, 0, 1); nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    wht = blk.copy(); wht.name = 'idwhite'; wht.node_tree.nodes['Emission'].inputs['Color'].default_value = (1, 1, 1, 1)
    keep = set(ZONES[A.id])
    for ob in sc.objects:
        if ob.type != 'MESH': continue
        for i in range(len(ob.material_slots)): ob.material_slots[i].material = wht if ob.name in keep else blk
        for mod in list(ob.modifiers): ob.modifiers.remove(mod)
    sun_d.energy = 0; bg.inputs['Strength'].default_value = 0
    sc.cycles.samples = 2; sc.cycles.use_denoising = False; sc.cycles.max_bounces = 0
    sc.cycles.filter_width = 0.8
    sc.view_settings.view_transform = 'Standard'
else:
    sc.cycles.samples = A.samples; sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
    sc.cycles.max_bounces = 5; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 2
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass

os.makedirs(A.out, exist_ok=True)
tiles = [int(x) for x in A.only.split(',') if x] if A.only else list(range(A.tiles))
tag = (A.tag + '-' if A.tag else '') + (A.id or 'beauty')
for i in tiles:
    if A.tiles > 1:
        sc.render.use_border = True; sc.render.use_crop_to_border = True
        sc.render.border_min_x = 0; sc.render.border_max_x = 1
        sc.render.border_min_y = 1 - (i + 1) / A.tiles; sc.render.border_max_y = 1 - i / A.tiles
    sc.render.filepath = os.path.join(os.path.abspath(A.out), f'{tag}-t{i:02d}.png')
    bpy.ops.render.render(write_still=True)
    print('rendered', tag, i, flush=True)
