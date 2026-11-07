#!/usr/bin/env python3
"""Zah Studio — Zack D.-style 3D scene: the growing money tree.

Builds a 3D scene in Blender and renders it to frames:
a money tree grows on green ground, gold coins appear on its
branches one by one, a man stands watching, and the camera slowly
moves around the tree. The finance metaphor from Zack D. Films
videos, built with Blender only.

Run it:
    blender -b --python build_money_tree.py
    DEMO_FRAMES=240 blender -b --python build_money_tree.py

Env vars:
    DEMO_FRAMES   total frames to render (default 240 = 10s at 24fps;
                  use 1440 for a full 60s video)
    FRAME_START   first frame (default 1)
    FRAME_END     last frame (default DEMO_FRAMES)

Output: frames/frame_####.png (960x540, 24fps, Workbench render).
Join them with assemble.sh.
"""
import os
import math
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "frames")

FRAMES = int(os.environ.get("DEMO_FRAMES", "240"))
FRAME_START = int(os.environ.get("FRAME_START", "1"))
FRAME_END = int(os.environ.get("FRAME_END", str(FRAMES)))

# ---------------------------------------------------------------- helpers


def make_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    # Workbench reads diffuse_color, not the node color.
    mat.diffuse_color = (*color, 1.0)
    return mat


def add_driver(obj, path, index, expr):
    fcurve = obj.driver_add(path, index)
    drv = fcurve.driver
    drv.type = 'SCRIPTED'
    drv.expression = expr
    return fcurve


def pop_in(start, dur=24):
    """Scale 0 -> 1 between frames start and start+dur."""
    return ("0 if frame < %d else (1 if frame > %d else (frame-%d)/%d)"
            % (start, start + dur, start, dur))


def add_empty(name, location):
    bpy.ops.object.empty_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def add_cylinder(name, location, radius, depth, mat, rotation=(0, 0, 0),
                 radius_top=None):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location,
        rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    if radius_top is not None:
        # Taper: scale the top ring. Cylinder vertices are ordered
        # bottom ring first, top ring second.
        mesh = obj.data
        for v in mesh.vertices:
            if v.co.z > 0:
                v.co.x *= radius_top / radius
                v.co.y *= radius_top / radius
    obj.data.materials.append(mat)
    return obj


def add_sphere(name, location, radius, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2, radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_box(name, location, size, mat):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.data.materials.append(mat)
    return obj


# ---------------------------------------------------------------- scene

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Sky background.
world = bpy.data.worlds.new("World")
world.color = (0.75, 0.88, 1.0)
scene.world = world

# Render: fast Workbench, studio light, material colors.
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
try:
    scene.display.shading.show_shadows = True
except AttributeError:
    pass
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.fps = 24
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = os.path.join(OUT_DIR, "frame_")

# Materials.
green = make_material("Grass", (0.30, 0.60, 0.30))
brown = make_material("Trunk", (0.45, 0.30, 0.15))
leaf1 = make_material("Leaf", (0.15, 0.55, 0.20))
leaf2 = make_material("LeafLight", (0.25, 0.70, 0.25))
gold = make_material("Gold", (1.0, 0.75, 0.10))
skin = make_material("Skin", (0.90, 0.75, 0.60))
teal = make_material("Shirt", (0.10, 0.55, 0.55))
pants = make_material("Pants", (0.20, 0.45, 0.25))
tan = make_material("Hat", (0.75, 0.60, 0.35))

# Ground.
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(green)

# The tree grows from this empty (scale Z 0.5 -> 1 over the clip).
tree = add_empty("TreeGrow", (0, 0, 0))
add_driver(tree, "scale", 2,
           "0.5 + 0.5*(frame-1)/%d" % max(FRAMES - 1, 1))

# Trunk.
trunk = add_cylinder("Trunk", (0, 0, 2.5), 0.5, 5.0, brown,
                     radius_top=0.35)
trunk.parent = tree

# Branches.
branch_defs = [
    ((0.9, 0.0, 4.2), (0.0, -0.7, 0.0)),
    ((-0.9, 0.0, 4.5), (0.0, 0.7, 0.0)),
    ((0.0, 0.9, 4.8), (0.7, 0.0, 0.0)),
    ((0.0, -0.9, 4.4), (-0.7, 0.0, 0.0)),
    ((0.5, 0.5, 5.2), (0.5, -0.5, 0.0)),
]
for i, (loc, rot) in enumerate(branch_defs):
    b = add_cylinder("Branch%d" % i, loc, 0.16, 2.4, brown,
                     rotation=rot, radius_top=0.08)
    b.parent = tree

# Leaves — clusters at branch ends and the top.
leaf_defs = [
    ((1.9, 0.0, 4.9), 1.2, leaf1), ((-1.9, 0.0, 5.2), 1.2, leaf2),
    ((0.0, 1.9, 5.5), 1.2, leaf1), ((0.0, -1.9, 5.1), 1.2, leaf2),
    ((1.1, 1.1, 5.9), 1.3, leaf1), ((-1.1, -1.1, 5.8), 1.3, leaf2),
    ((0.0, 0.0, 6.4), 1.4, leaf1), ((1.4, -1.0, 4.6), 1.0, leaf2),
    ((-1.4, 1.0, 4.7), 1.0, leaf1), ((0.8, -1.5, 5.6), 1.1, leaf2),
    ((-0.8, 1.5, 5.7), 1.1, leaf1), ((0.0, 0.0, 5.4), 1.5, leaf2),
]
for i, (loc, radius, mat) in enumerate(leaf_defs):
    leaf = add_sphere("Leaf%d" % i, loc, radius, mat)
    leaf.parent = tree
    expr = pop_in(30 + i * 10)
    for idx in range(3):
        add_driver(leaf, "scale", idx, expr)

# Gold coins — hang OUTSIDE the leaf canopy so they can be seen:
# ring around the tree, below the leaves, slowly spinning.
coin_defs = []
for i, (angle_deg, radius, z) in enumerate([
        (10, 3.4, 4.2), (45, 3.6, 5.0), (80, 3.3, 4.5),
        (115, 3.5, 5.4), (150, 3.4, 4.0), (185, 3.6, 5.2),
        (220, 3.3, 4.4), (255, 3.5, 5.6), (290, 3.4, 4.1),
        (325, 3.6, 5.0), (30, 3.2, 3.8), (140, 3.2, 5.8),
        (200, 3.2, 3.9), (300, 3.2, 5.7),
]):
    a = math.radians(angle_deg)
    coin_defs.append((radius * math.cos(a), radius * math.sin(a), z))
for i, loc in enumerate(coin_defs):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.45, depth=0.08, location=loc)
    coin = bpy.context.active_object
    coin.name = "Coin%d" % i
    coin.data.materials.append(gold)
    coin.parent = tree
    expr = pop_in(60 + i * 10)
    for idx in range(3):
        add_driver(coin, "scale", idx, expr)
    add_driver(coin, "rotation_euler", 2, "(frame-1)*0.03")

# The man, watching the tree.
man = add_empty("Man", (3.5, 1.5, 0))
expr = pop_in(12, 24)
for idx in range(3):
    add_driver(man, "scale", idx, expr)
parts = [
    ("LegL", (-0.18, 0, 0.4), (0.28, 0.28, 0.8), pants, "box"),
    ("LegR", (0.18, 0, 0.4), (0.28, 0.28, 0.8), pants, "box"),
    ("Torso", (0, 0, 1.25), (0.7, 0.45, 0.9), teal, "box"),
    ("ArmL", (-0.48, 0, 1.25), (0.22, 0.22, 0.8), teal, "box"),
    ("ArmR", (0.48, 0, 1.25), (0.22, 0.22, 0.8), teal, "box"),
    ("Head", (0, 0, 2.0), (0.32, 0.32, 0.32), skin, "sphere"),
    ("HatTop", (0, 0, 2.28), (0.38, 0.38, 0.12), tan, "cyl"),
    ("HatBrim", (0, 0, 2.20), (0.52, 0.52, 0.05), tan, "cyl"),
]
for name, loc, size, mat, kind in parts:
    if kind == "box":
        obj = add_box(name, loc, size, mat)
    elif kind == "sphere":
        obj = add_sphere(name, loc, size[0], mat)
    else:
        obj = add_cylinder(name, loc, size[0], size[2], mat)
    obj.parent = man

# Camera: slow orbit around the tree, always looking at it.
# Pulled back so the whole tree AND the man fit in frame.
rig = add_empty("CamRig", (0, 0, 3.5))
add_driver(rig, "rotation_euler", 2,
           "(frame-1)/%d*1.2" % max(FRAMES - 1, 1))
bpy.ops.object.camera_add(location=(15, -15, 4))
cam = bpy.context.active_object
cam.name = "Camera"
cam.data.lens = 35
cam.parent = rig
target = add_empty("TreeTop", (0, 0, 3.5))
con = cam.constraints.new('TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
scene.camera = cam

os.makedirs(OUT_DIR, exist_ok=True)
bpy.ops.render.render(animation=True)
print("Rendered frames %d-%d into %s" % (FRAME_START, FRAME_END, OUT_DIR))
