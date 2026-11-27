"""Builds the FIT township scale model in Blender from layout.json and renders a turntable.
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
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
L = json.load(open(A.layout))
random.seed(11)

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
BASE = 46.0
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
for name in ('houses', 'industry', 'civic'):
    ob = bpy.data.objects[name]
    mod = ob.modifiers.new('bevel', 'BEVEL'); mod.width = 0.18; mod.segments = 1; mod.limit_method = 'ANGLE'

# ---------- light, shadow catcher, camera ----------
sun_d = bpy.data.lights.new('sun', 'SUN'); sun_d.energy = 4.4; sun_d.angle = math.radians(3.5); sun_d.color = (1.0, 0.965, 0.92)
sun = bpy.data.objects.new('sun', sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(54), 0, math.radians(-38))
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = hexc('#F6EFE4'); bg.inputs['Strength'].default_value = 0.6

bpy.ops.mesh.primitive_plane_add(size=9000, location=(0, 0, -BASE - 0.02))
catcher = bpy.context.active_object; catcher.is_shadow_catcher = True

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = A.lens; cam_d.clip_start = 10; cam_d.clip_end = 20000
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
el = math.radians(A.elev)
target = Vector((0, 0, -20))
cam.location = target + Vector((0, -A.dist * math.cos(el), A.dist * math.sin(el)))
cam.rotation_euler = (math.radians(90) - el, 0, 0); cam_d.shift_y = A.shift

# ---------- render settings ----------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = A.samples; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
sc.render.film_transparent = True
sc.render.resolution_x = A.w; sc.render.resolution_y = A.h; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.render.image_settings.compression = 15
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.threads_mode = 'AUTO'

if A.blend: bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(A.blend))
os.makedirs(A.out, exist_ok=True)
frames = [int(x) for x in A.only.split(',') if x] if A.only else [A.still] if A.still >= 0 else list(range(A.first, (A.last if A.last >= 0 else A.frames - 1) + 1))
for i in frames:
    root.rotation_euler = (0, 0, math.radians(A.start_deg + 360.0 * i / A.frames))
    sc.render.filepath = os.path.join(os.path.abspath(A.out), f'f{i:03d}.png')
    bpy.ops.render.render(write_still=True)
    print('rendered', i, flush=True)
