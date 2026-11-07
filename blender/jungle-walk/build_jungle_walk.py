"""Blender demo: low-poly man walking through a jungle, 60 seconds, 24 fps.
Run: blender -b --python build_jungle_walk.py [-- --test]
  --test renders 1 frame to /tmp/blender-demo-test for a quick look/speed check.
Full run renders 1440 frames to ~/workspace/blender-demo/frames/.
"""
import bpy
import math
import random
import sys
import os

TEST = '--test' in sys.argv
TOTAL_FRAMES = int(os.environ.get('DEMO_FRAMES', '1' if TEST else '1440'))
FPS = 24
OUT_DIR = '/tmp/blender-demo-test' if TEST else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames')
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------- clean scene ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.fps = FPS
FRAME_START = int(os.environ.get('FRAME_START', '1'))
FRAME_END = int(os.environ.get('FRAME_END', str(TOTAL_FRAMES)))
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene.render.filepath = os.path.join(OUT_DIR, 'frame_')
scene.render.image_settings.file_format = 'PNG'

shading = scene.display.shading
shading.light = 'STUDIO'
shading.color_type = 'MATERIAL'
shading.show_shadows = True
shading.show_cavity = False
shading.show_object_outline = False

if 'World' in bpy.data.worlds:
    world = bpy.data.worlds['World']
else:
    world = bpy.data.worlds.new('World')
    scene.world = world
world.use_nodes = False
world.color = (0.55, 0.75, 0.95)

# ---------------- materials ----------------
def mat(name, rgb):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1.0)
    return m

SKIN = mat('Skin', (0.90, 0.70, 0.55))
SHIRT = mat('Shirt', (0.10, 0.50, 0.55))
PANTS = mat('Pants', (0.20, 0.35, 0.20))
HAT = mat('Hat', (0.72, 0.62, 0.38))
TRUNK = mat('Trunk', (0.35, 0.22, 0.12))
LEAF = mat('Leaf', (0.15, 0.45, 0.15))
LEAF2 = mat('Leaf2', (0.20, 0.55, 0.18))
GROUND = mat('Ground', (0.25, 0.50, 0.20))
PATH = mat('Path', (0.62, 0.52, 0.32))
ROCK = mat('Rock', (0.45, 0.45, 0.45))
SHOE = mat('Shoe', (0.25, 0.18, 0.12))

# ---------------- helpers ----------------
def box(name, loc, size, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        o.data.materials.append(material)
    return o

def limb(name, loc, size, material):
    """Box whose pivot sits at its top face (joint), hanging down."""
    o = box(name, loc, size, material)
    h = size[2]
    for v in o.data.vertices:
        v.co.z -= h / 2.0
    return o

def parent(child, par):
    bpy.context.view_layer.update()
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()

def add_driver(obj, path, index, expr):
    f = obj.driver_add(path, index)
    f.driver.type = 'SCRIPTED'
    f.driver.expression = expr
    return f

# ---------------- the man (faces +X, walks +X) ----------------
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
root = bpy.context.active_object
root.name = 'ManRoot'

torso = box('Torso', (0, 0, 1.24), (0.24, 0.44, 0.58), SHIRT)
parent(torso, root)

bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.14, location=(0.02, 0, 1.66))
head = bpy.context.active_object
head.name = 'Head'
head.data.materials.append(SKIN)
parent(head, root)

bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.03, location=(0.02, 0, 1.76), vertices=16)
brim = bpy.context.active_object
brim.name = 'HatBrim'
brim.data.materials.append(HAT)
parent(brim, root)

bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.10, location=(0.02, 0, 1.82), vertices=16)
crown = bpy.context.active_object
crown.name = 'HatCrown'
crown.data.materials.append(HAT)
parent(crown, root)

# legs: hip pivots at z=0.98, knee at 0.52, ankle at 0.06
thigh_L = limb('Thigh_L', (0, 0.11, 0.98), (0.17, 0.17, 0.46), PANTS)
thigh_R = limb('Thigh_R', (0, -0.11, 0.98), (0.17, 0.17, 0.46), PANTS)
shin_L = limb('Shin_L', (0, 0.11, 0.52), (0.14, 0.14, 0.46), PANTS)
shin_R = limb('Shin_R', (0, -0.11, 0.52), (0.14, 0.14, 0.46), PANTS)
foot_L = box('Foot_L', (0.05, 0.11, 0.04), (0.26, 0.13, 0.08), SHOE)
foot_R = box('Foot_R', (0.05, -0.11, 0.04), (0.26, 0.13, 0.08), SHOE)
for c, p in [(thigh_L, root), (thigh_R, root), (shin_L, thigh_L), (shin_R, thigh_R),
             (foot_L, shin_L), (foot_R, shin_R)]:
    parent(c, p)

# arms: shoulder pivots at z=1.46, elbow at 1.12, wrist at 0.82
arm_L = limb('Arm_L', (0, 0.27, 1.46), (0.12, 0.12, 0.34), SHIRT)
arm_R = limb('Arm_R', (0, -0.27, 1.46), (0.12, 0.12, 0.34), SHIRT)
fore_L = limb('Fore_L', (0, 0.27, 1.12), (0.10, 0.10, 0.30), SKIN)
fore_R = limb('Fore_R', (0, -0.27, 1.12), (0.10, 0.10, 0.30), SKIN)
for c, p in [(arm_L, root), (arm_R, root), (fore_L, arm_L), (fore_R, arm_R)]:
    parent(c, p)
fore_L.rotation_euler[1] = -0.35
fore_R.rotation_euler[1] = -0.35

# ---------------- walk cycle (24 frames = 1 second, 2 steps) ----------------
W = "2*pi/24"
add_driver(thigh_L, 'rotation_euler', 1, f"0.5*sin(frame*{W})")
add_driver(thigh_R, 'rotation_euler', 1, f"0.5*sin(frame*{W}+pi)")
add_driver(shin_L, 'rotation_euler', 1, f"0.6*sin(frame*{W}-2.0)")
add_driver(shin_R, 'rotation_euler', 1, f"0.6*sin(frame*{W}-2.0+pi)")
add_driver(arm_L, 'rotation_euler', 1, f"0.4*sin(frame*{W}+pi)")
add_driver(arm_R, 'rotation_euler', 1, f"0.4*sin(frame*{W})")
add_driver(torso, 'rotation_euler', 0, f"0.06*sin(frame*{W})")
add_driver(root, 'location', 2, f"0.03*sin(frame*2*{W})")

# man walks 0 -> 120 m over the 60 s (2 m/s), perfectly linear via driver
add_driver(root, 'location', 0, "(frame-1)/24*2.0")

# ---------------- jungle ----------------
random.seed(42)

def tree(x, y, s):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14 * s, depth=1.4 * s,
                                        location=(x, y, 0.7 * s), vertices=8)
    t = bpy.context.active_object
    t.data.materials.append(TRUNK)
    for (r, h, z, m) in [(1.1 * s, 2.2 * s, 2.2 * s, LEAF),
                         (0.8 * s, 1.8 * s, 3.0 * s, LEAF2),
                         (0.5 * s, 1.4 * s, 3.7 * s, LEAF)]:
        bpy.ops.mesh.primitive_cone_add(radius1=r, depth=h, location=(x, y, z), vertices=8)
        c = bpy.context.active_object
        c.data.materials.append(m)

for _ in range(130):
    x = random.uniform(-15, 135)
    side = 1 if random.random() > 0.5 else -1
    # camera sits at y=-5.5: keep camera-side trees behind it (y < -5.5)
    y = random.uniform(3.5, 17) if side > 0 else -random.uniform(7, 17)
    tree(x, y, random.uniform(0.8, 1.7))

for _ in range(18):  # tall background trees
    x = random.uniform(-15, 135)
    side = 1 if random.random() > 0.5 else -1
    y = random.uniform(19, 30) if side > 0 else -random.uniform(19, 30)
    tree(x, y, random.uniform(2.0, 2.8))

for _ in range(40):  # bushes
    x = random.uniform(-10, 130)
    side = 1 if random.random() > 0.5 else -1
    y = random.uniform(2.6, 7) if side > 0 else -random.uniform(6.5, 9)
    s = random.uniform(0.3, 0.6)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=s, location=(x, y, s * 0.6), subdivisions=1)
    b = bpy.context.active_object
    b.data.materials.append(LEAF2)

for _ in range(20):  # rocks
    x = random.uniform(-10, 130)
    side = 1 if random.random() > 0.5 else -1
    y = random.uniform(2.2, 9) if side > 0 else -random.uniform(6.5, 10)
    s = random.uniform(0.15, 0.4)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, s * 0.5))
    r = bpy.context.active_object
    r.scale = (s, s * random.uniform(0.6, 1.2), s * 0.7)
    r.rotation_euler = (0, 0, random.uniform(0, 3.14))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    r.data.materials.append(ROCK)

# ground + dirt path
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(60, 0, 0))
g = bpy.context.active_object
g.name = 'Ground'
g.scale = (220, 70, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
g.data.materials.append(GROUND)

bpy.ops.mesh.primitive_plane_add(size=1.0, location=(60, 0, 0.01))
p = bpy.context.active_object
p.name = 'Path'
p.scale = (170, 3.0, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
p.data.materials.append(PATH)

# sun
bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(55), math.radians(10), math.radians(35))

# ---------------- camera: side tracking shot, follows the man ----------------
bpy.ops.object.camera_add(location=(-3.0, -5.5, 2.4))
cam = bpy.context.active_object
cam.name = 'Camera'
scene.camera = cam
cam.data.lens = 50
con = cam.constraints.new(type='TRACK_TO')
con.target = torso
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
# camera follows the man, 3 m behind, same speed
add_driver(cam, 'location', 0, "(frame-1)/24*2.0-3.0")

# ---------------- save + render ----------------
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jungle_walk.blend'))
bpy.ops.render.render(animation=True)
print('RENDER DONE', TOTAL_FRAMES, 'frames ->', OUT_DIR)
