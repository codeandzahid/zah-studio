"""Roblox viral gameplay in Blender: classic blocky noob runs an obby
course over lava. 60s, 24fps, 1440 frames. Camera follows from behind.

Engine: BLENDER_ENGINE env — BLENDER_EEVEE (realistic light) or
BLENDER_WORKBENCH (fast fallback). Render 960x540, upscale to 4K later.
Test: blender -b --python build_roblox_obby.py -- --test  (1 frame)
Full: FRAME_START / FRAME_END env vars split the range into chunks.
"""
import bpy, math, os, random, sys

TEST = '--test' in sys.argv
TOTAL_FRAMES = int(os.environ.get('DEMO_FRAMES', '1' if TEST else '1440'))
ENGINE = os.environ.get('BLENDER_ENGINE', 'BLENDER_WORKBENCH')
FRAME_START = int(os.environ.get('FRAME_START', '1'))
FRAME_END = int(os.environ.get('FRAME_END', str(TOTAL_FRAMES)))
OUT_DIR = '/tmp/roblox-test' if TEST else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames')
os.makedirs(OUT_DIR, exist_ok=True)

SPEED = 4.0          # m/s, one platform per second
COURSE_LEN = 240.0   # 60s * 4 m/s

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = ENGINE
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.fps = 24
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene.render.filepath = os.path.join(OUT_DIR, 'frame_')
scene.render.image_settings.file_format = 'PNG'

# world: bright sky blue
if 'World' in bpy.data.worlds:
    world = bpy.data.worlds['World']
else:
    world = bpy.data.worlds.new('World')
    scene.world = world
world.color = (0.45, 0.72, 0.98)

if ENGINE == 'BLENDER_EEVEE':
    scene.eevee.use_shadows = True
    scene.render.film_transparent = False
else:
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = False
    scene.display.shading.studio_light = 'Default'

# sun
sun_data = bpy.data.lights.new('Sun', 'SUN')
sun_data.energy = 4.0
sun_data.angle = 25
sun = bpy.data.objects.new('Sun', sun_data)
sun.rotation_euler = (math.radians(50), 0, math.radians(30))
scene.collection.objects.link(sun)

# ---------- helpers ----------
def mat(name, rgb, rough=0.55, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*rgb, 1.0)  # Workbench renders this color
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    return m

def box(name, loc, scale, material, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    if parent:
        o.parent = parent
    return o

def add_driver(obj, path, index, expr):
    f = obj.driver_add(path, index)
    f.driver.type = 'SCRIPTED'
    f.driver.expression = expr
    return f

# ---------- materials ----------
YELLOW = mat('NoobYellow', (0.96, 0.80, 0.15), 0.45)
BLUE   = mat('NoobBlue',   (0.05, 0.35, 0.85), 0.45)
GREEN  = mat('NoobGreen',  (0.15, 0.65, 0.20), 0.45)
BLACK  = mat('FaceBlack',  (0.02, 0.02, 0.02), 0.4)
GOLD   = mat('CoinGold',   (1.0, 0.75, 0.1), 0.25, 0.8)
LAVA   = mat('Lava',       (1.0, 0.4, 0.08), 0.6)
LAVA2  = mat('LavaBright', (1.0, 0.65, 0.2), 0.6)
WHITE  = mat('CloudWhite', (1.0, 1.0, 1.0), 0.9)
GREY   = mat('RockGrey',   (0.55, 0.55, 0.58), 0.8)
OBBY_COLORS = [
    mat('ObbyRed',    (0.9, 0.15, 0.15), 0.4),
    mat('ObbyOrange', (1.0, 0.5, 0.05), 0.4),
    mat('ObbyYellow', (1.0, 0.85, 0.1), 0.4),
    mat('ObbyGreen',  (0.15, 0.8, 0.25), 0.4),
    mat('ObbyBlue',   (0.1, 0.45, 1.0), 0.4),
    mat('ObbyPurple', (0.6, 0.2, 0.9), 0.4),
    mat('ObbyPink',   (1.0, 0.4, 0.7), 0.4),
    mat('ObbyCyan',   (0.1, 0.85, 0.9), 0.4),
]

# ---------- lava floor ----------
bpy.ops.mesh.primitive_plane_add(size=600, location=(120, 0, -3.0))
lava = bpy.context.active_object
lava.name = 'LavaFloor'
lava.data.materials.append(LAVA)
# bright lava patches
random.seed(7)
for i in range(60):
    x = random.uniform(-20, 260)
    y = random.uniform(-40, 40)
    s = random.uniform(1.5, 5.0)
    bpy.ops.mesh.primitive_plane_add(size=s, location=(x, y, -2.95))
    p = bpy.context.active_object
    p.name = f'LavaPatch{i}'
    p.data.materials.append(LAVA2)

# ---------- obby course: 60 platforms, 4 m apart ----------
for i in range(61):
    x = i * 4.0
    w = 4.0 if i % 5 else 5.0          # every 5th is a wider rest pad
    d = 4.0
    y = 0.0
    col = OBBY_COLORS[i % len(OBBY_COLORS)]
    if i == 0:
        col = mat('StartGreen', (0.2, 0.9, 0.3), 0.4)
    if i == 60:
        col = mat('FinishGold', (1.0, 0.8, 0.15), 0.25, 0.6)
    plat = box(f'Platform{i:02d}', (x, y, -0.4), (w / 2, d / 2, 0.4), col)

# checkpoint flags every 10 platforms
for i in range(0, 61, 10):
    x = i * 4.0
    pole = box(f'FlagPole{i}', (x, 1.8, 1.2), (0.08, 0.08, 1.2), GREY)
    flag = box(f'Flag{i}', (x + 0.45, 1.8, 2.2), (0.45, 0.05, 0.35),
               OBBY_COLORS[(i // 10) % len(OBBY_COLORS)])

# finish arch at the end
arch_mat = GOLD
box('ArchL', (240, -2.2, 2.0), (0.3, 0.3, 2.0), arch_mat)
box('ArchR', (240, 2.2, 2.0), (0.3, 0.3, 2.0), arch_mat)
box('ArchTop', (240, 0, 4.1), (0.3, 2.5, 0.3), arch_mat)

# spinning gold coins above every 3rd platform
coins = []
for i in range(2, 60, 3):
    x = i * 4.0
    c = box(f'Coin{i}', (x, 0, 2.2), (0.45, 0.45, 0.08), GOLD)
    add_driver(c, 'rotation_euler', 2, 'frame*0.12')
    coins.append(c)

# blocky clouds
random.seed(42)
for i in range(16):
    x = random.uniform(-20, 260)
    y = random.uniform(-45, 45)
    z = random.uniform(18, 30)
    s = random.uniform(3, 7)
    box(f'Cloud{i}', (x, y, z), (s, s * 0.6, s * 0.35), WHITE)

# distant green hills
for i, hx in enumerate((-30, 60, 150, 260)):
    box(f'Hill{i}', (hx, -55, -1), (28, 8, 6), mat(f'Hill{i}', (0.25, 0.6, 0.3), 0.9))
    box(f'HillB{i}', (hx + 20, 55, -1), (28, 8, 5), mat(f'HillB{i}', (0.25, 0.6, 0.3), 0.9))

# ---------- Roblox noob ----------
root = bpy.data.objects.new('NoobRoot', None)
scene.collection.objects.link(root)
root.location = (0, 0, 0)
# runs 4 m/s forward
add_driver(root, 'location', 0, '(frame-1)/24*4.0')
# hop every second: peaks between platforms
add_driver(root, 'location', 2, '1.6*(sin(3.14159*((frame-1)%24)/24))**2')

# torso (blue)
torso = box('Torso', (0, 0, 2.6), (0.9, 0.5, 1.0), BLUE, parent=root)
# head (yellow) + face
head = box('Head', (0, 0, 4.1), (0.55, 0.55, 0.55), YELLOW, parent=root)
box('EyeL', (0, 0.56, 4.25), (0.09, 0.02, 0.14), BLACK, parent=root)
box('EyeR', (0, 0.56, 4.25), (0.09, 0.02, 0.14), BLACK, parent=root)
# fix eye x positions
bpy.data.objects['EyeL'].location.x = -0.22
bpy.data.objects['EyeR'].location.x = 0.22
box('Smile', (0, 0.56, 3.95), (0.3, 0.02, 0.05), BLACK, parent=root)

# arms (yellow) — pivot at shoulder: use empties as pivots
def limb(name, side, z, material):
    piv = bpy.data.objects.new(name + 'Pivot', None)
    scene.collection.objects.link(piv)
    piv.parent = root
    piv.location = (0, side * 1.05, z)
    part = box(name, (0, 0, -0.9), (0.45, 0.45, 0.9), material, parent=piv)
    return piv

armL = limb('ArmL', -1, 3.4, YELLOW)
armR = limb('ArmR', 1, 3.4, YELLOW)
legL = limb('LegL', -1, 1.7, GREEN)
legR = limb('LegR', 1, 1.7, GREEN)

# run cycle: opposite swings, 1 stride per second
add_driver(armL, 'rotation_euler', 0, '0.9*sin(2*3.14159*frame/24)')
add_driver(armR, 'rotation_euler', 0, '-0.9*sin(2*3.14159*frame/24)')
add_driver(legL, 'rotation_euler', 0, '-0.9*sin(2*3.14159*frame/24)')
add_driver(legR, 'rotation_euler', 0, '0.9*sin(2*3.14159*frame/24)')
# torso bob + slight forward lean
add_driver(torso, 'location', 2, '2.6+0.12*abs(sin(2*3.14159*frame/24))')
add_driver(head, 'location', 2, '4.1+0.12*abs(sin(2*3.14159*frame/24))')
add_driver(root, 'rotation_euler', 1, '0.12')

# ---------- camera: follow from behind ----------
cam_data = bpy.data.cameras.new('Camera')
cam_data.lens = 35
cam = bpy.data.objects.new('Camera', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = (-9.0, -11.0, 7.0)
add_driver(cam, 'location', 0, '(frame-1)/24*4.0-9.0')
con = cam.constraints.new(type='TRACK_TO')
con.target = torso
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roblox_obby.blend'))
bpy.ops.render.render(animation=True)
print(f'RENDER DONE {FRAME_END - FRAME_START + 1} frames -> {OUT_DIR}')
