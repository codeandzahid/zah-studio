#!/usr/bin/env python3
"""Zah Studio — Ship of Theseus, Zack D. style (original remake).

Recreates the Zack D. Films Short "The Ship Of Theseus Paradox"
as an original build: a man on a bright blue background with a
grid floor. His layers come off one by one — skin, then muscle,
then skeleton — and at the end he is put back together.
Vertical 9:16, big word captions, close camera.

Run it:
    blender -b --python build_theseus.py
    DEMO_FRAMES=528 blender -b --python build_theseus.py

Env vars:
    DEMO_FRAMES   total frames (default 528 = 22s at 24fps)
    FRAME_START   first frame (default 1)
    FRAME_END     last frame (default DEMO_FRAMES)
    RENDER_W      width (default 540), RENDER_H height (default 960)

Output: frames/frame_####.png (vertical, Eevee).
Join them with assemble.sh (adds captions + voiceover).
"""
import os
import math
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "frames")

FRAMES = int(os.environ.get("DEMO_FRAMES", "528"))
FRAME_START = int(os.environ.get("FRAME_START", "1"))
FRAME_END = int(os.environ.get("FRAME_END", str(FRAMES)))

# Act boundaries (frames at 24fps): skin | muscle | skeleton | skin back
ACT2 = 131   # muscle appears
ACT3 = 301   # skeleton appears
ACT4 = 461   # skin man returns

# ---------------------------------------------------------------- helpers


def make_material(name, color, roughness=0.6, metallic=0.0, subsurface=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        try:
            bsdf.inputs["Subsurface Weight"].default_value = subsurface
        except Exception:
            pass
    mat.diffuse_color = (*color, 1.0)
    return mat


def shade_smooth(obj):
    if obj.type != 'MESH':
        return
    for poly in obj.data.polygons:
        poly.use_smooth = True


def add_driver(obj, path, index, expr):
    fcurve = obj.driver_add(path, index)
    drv = fcurve.driver
    drv.type = 'SCRIPTED'
    drv.expression = expr
    return fcurve


def add_empty(name, location):
    bpy.ops.object.empty_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def add_cylinder(name, location, radius, depth, mat, rotation=(0, 0, 0),
                 radius_top=None):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    if radius_top is not None:
        mesh = obj.data
        for v in mesh.vertices:
            if v.co.z > 0:
                v.co.x *= radius_top / radius
                v.co.y *= radius_top / radius
    obj.data.materials.append(mat)
    shade_smooth(obj)
    return obj


def add_sphere(name, location, radius, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2, radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    shade_smooth(obj)
    return obj


def add_box(name, location, size, mat, rotation=(0, 0, 0)):
    # primitive_cube_add makes a 2x2x2 cube, so halve the scale
    # to get the intended size.
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    obj.data.materials.append(mat)
    return obj


def add_torus(name, location, major, minor, mat):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    shade_smooth(obj)
    return obj


def join_parts(parent_empty, name):
    """Merge a body's mesh parts into one object (far fewer draw
    calls for Eevee) — keeps all materials as slots."""
    parts = [o for o in bpy.data.objects
             if o.parent == parent_empty and o.type == 'MESH']
    if len(parts) < 2:
        return
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = name
    joined.parent = parent_empty


def limb(parent, prefix, shoulder, mat, r_upper=0.13, r_fore=0.11,
         upper_len=0.55, fore_len=0.5, side=1):
    """One arm: upper arm + forearm + hand, hanging at the side."""
    x, y, z = shoulder
    upper = add_cylinder(prefix + "_upper",
                         (x, y, z - upper_len / 2),
                         r_upper, upper_len, mat)
    upper.parent = parent
    elbow_z = z - upper_len
    fore = add_cylinder(prefix + "_fore",
                        (x, y, elbow_z - fore_len / 2),
                        r_fore, fore_len, mat)
    fore.parent = parent
    hand = add_sphere(prefix + "_hand",
                      (x, y, elbow_z - fore_len - 0.08),
                      0.13, mat, scale=(0.8, 1.1, 1.2))
    hand.parent = parent
    return upper, fore, hand


def leg(parent, prefix, hip, mat, r_thigh=0.16, r_shin=0.13,
        thigh_len=0.6, shin_len=0.55):
    """One leg: thigh + shin + foot."""
    x, y, z = hip
    thigh = add_cylinder(prefix + "_thigh",
                         (x, y, z - thigh_len / 2),
                         r_thigh, thigh_len, mat)
    thigh.parent = parent
    knee_z = z - thigh_len
    shin = add_cylinder(prefix + "_shin",
                        (x, y, knee_z - shin_len / 2),
                        r_shin, shin_len, mat)
    shin.parent = parent
    foot = add_box(prefix + "_foot",
                   (x, y + 0.08, knee_z - shin_len - 0.03),
                   (0.16, 0.30, 0.07), mat)
    foot.parent = parent
    return thigh, shin, foot


# ---------------------------------------------------------------- scene

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Bright blue background, like the reference.
world = bpy.data.worlds.new("World")
world.use_nodes = True
scene.world = world
nt = world.node_tree
bg = nt.nodes.get("Background")
bg.inputs["Color"].default_value = (0.10, 0.28, 0.95, 1.0)
bg.inputs["Strength"].default_value = 0.2

scene.view_settings.view_transform = 'Standard'

# Eevee, fast settings. No cast shadows in the reference — the
# 3D look comes from the skin shading and the soft studio light.
scene.render.engine = 'BLENDER_EEVEE'
eevee = scene.eevee
for attr, val in [("use_soft_shadows", False), ("use_gtao", False),
                 ("use_bloom", False), ("use_ssr", False),
                 ("taa_render_samples", 4)]:
    try:
        setattr(eevee, attr, val)
    except AttributeError:
        pass
scene.render.resolution_x = int(os.environ.get("RENDER_W", "540"))
scene.render.resolution_y = int(os.environ.get("RENDER_H", "960"))
scene.render.fps = 24
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = os.path.join(OUT_DIR, "frame_")

# Soft studio light from the FRONT (camera side), so the skin
# reads warm, not blue. Both lights aim at the man.
light_target = add_empty("LightTarget", (0, 0, 2.06))
bpy.ops.object.light_add(type='SUN', location=(4, 6, 8))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 5.0
sun.data.use_shadow = False
con = sun.constraints.new('TRACK_TO')
con.target = light_target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
bpy.ops.object.light_add(type='AREA', location=(-5, 5, 6))
fill = bpy.context.active_object
fill.name = "Fill"
fill.data.energy = 150.0
fill.data.size = 6.0
fill.data.use_shadow = False
con = fill.constraints.new('TRACK_TO')
con.target = light_target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

# Materials.
skin = make_material("Skin", (0.88, 0.70, 0.58), roughness=0.55,
                     subsurface=0.0)
muscle = make_material("Muscle", (0.62, 0.10, 0.09), roughness=0.5)
muscle_dark = make_material("MuscleDark", (0.40, 0.05, 0.05),
                            roughness=0.5)
bone = make_material("Bone", (0.88, 0.86, 0.78), roughness=0.6)
hair = make_material("Hair", (0.85, 0.85, 0.88), roughness=0.7)
eye_dark = make_material("EyeDark", (0.05, 0.03, 0.02), roughness=0.3)
eye_white = make_material("EyeWhite", (0.95, 0.95, 0.95), roughness=0.2)
iris = make_material("Iris", (0.10, 0.15, 0.20), roughness=0.2)
tag_white = make_material("TagWhite", (0.95, 0.95, 0.95), roughness=0.6)
tag_red = make_material("TagRed", (0.85, 0.15, 0.15), roughness=0.6)
dark = make_material("Dark", (0.08, 0.06, 0.06), roughness=0.7)

# Grid floor — light blue with white grid lines (brick texture).
floor_mat = bpy.data.materials.new("GridFloor")
floor_mat.use_nodes = True
fnt = floor_mat.node_tree
fbsdf = fnt.nodes["Principled BSDF"]
brick = fnt.nodes.new("ShaderNodeTexBrick")
brick.offset = 0
brick.inputs["Scale"].default_value = 40
brick.inputs["Mortar Size"].default_value = 0.02
brick.inputs["Color1"].default_value = (0.62, 0.78, 1.0, 1.0)
brick.inputs["Color2"].default_value = (0.62, 0.78, 1.0, 1.0)
brick.inputs["Mortar"].default_value = (1.0, 1.0, 1.0, 1.0)
fnt.links.new(brick.outputs["Color"], fbsdf.inputs["Base Color"])
fbsdf.inputs["Roughness"].default_value = 0.9
bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "GridFloor"
floor.data.materials.append(floor_mat)

# ---------------------------------------------------------------- the man
# The man faces +Y. Camera sits on the +Y side.

# --- Skin man ---
# Lifted 0.56 so the feet (legs are 1.18 long from the hip at
# z 0.62) land on the floor instead of under it.
skin_man = add_empty("SkinMan", (0, 0, 0.56))

# Legs.
leg(skin_man, "SkinLegL", (-0.20, 0, 0.62), skin)
leg(skin_man, "SkinLegR", (0.20, 0, 0.62), skin)
# Pelvis + abdomen + chest.
pelvis = add_sphere("SkinPelvis", (0, 0, 0.68), 0.30, skin,
                    scale=(1.7, 1.1, 1.2))
pelvis.parent = skin_man
abdomen = add_cylinder("SkinAbdomen", (0, 0, 0.95), 0.42, 0.5, skin,
                       radius_top=0.46)
abdomen.parent = skin_man
chest = add_sphere("SkinChest", (0, 0, 1.45), 0.42, skin,
                   scale=(1.45, 0.85, 1.6))
chest.parent = skin_man
# Arms at the sides.
limb(skin_man, "SkinArmL", (-0.62, 0, 1.62), skin, side=-1)
limb(skin_man, "SkinArmR", (0.62, 0, 1.62), skin, side=1)
# Neck + head.
neck = add_cylinder("SkinNeck", (0, 0, 1.82), 0.17, 0.3, skin)
neck.parent = skin_man
head = add_sphere("SkinHead", (0, 0, 2.02), 0.30, skin,
                  scale=(1.0, 0.95, 1.15))
head.parent = skin_man
# Face: eyes, nose, mouth, ears.
for sx in (-1, 1):
    eye = add_sphere("SkinEye", (sx * 0.13, 0.22, 2.06), 0.04,
                     eye_dark)
    eye.parent = skin_man
    ear = add_sphere("SkinEar", (sx * 0.29, 0, 2.02), 0.07, skin,
                     scale=(0.5, 0.8, 1.0))
    ear.parent = skin_man
nose = add_cylinder("SkinNose", (0, 0.26, 1.94), 0.03, 0.07, skin,
                    rotation=(math.radians(90), 0, 0))
nose.parent = skin_man
mouth = add_box("SkinMouth", (0, 0.26, 1.82), (0.12, 0.02, 0.025),
                muscle_dark)
mouth.parent = skin_man
# White-grey hair cap — a dome on TOP of the head only, so the
# forehead and eyes stay clear.
haircap = add_sphere("SkinHair", (0, -0.05, 2.28), 0.27, hair,
                     scale=(0.95, 0.9, 0.65))
haircap.parent = skin_man
# Name tag on the chest: white card + red strip.
tag = add_box("Tag", (-0.28, 0.36, 1.48), (0.30, 0.02, 0.20), tag_white)
tag.parent = skin_man
tagstrip = add_box("TagStrip", (-0.28, 0.37, 1.55), (0.30, 0.02, 0.06),
                   tag_red)
tagstrip.parent = skin_man
bpy.ops.object.text_add(location=(-0.28, 0.38, 1.46))
tagtext = bpy.context.active_object
tagtext.name = "TagText"
tagtext.data.body = "ZACK\nFILMS"
tagtext.data.size = 0.09
tagtext.data.align_x = 'CENTER'
tagtext.data.align_y = 'CENTER'
tagtext.rotation_euler = (math.radians(90), 0, math.radians(180))
tagtext.data.materials.append(dark)
tagtext.parent = skin_man
join_parts(skin_man, "SkinBody")
# Visible in Act 1 and Act 4 only (hard cut at the act frames).
# Added AFTER the join: the join bakes the parent's scale into
# the geometry, and at frame 1 the driver would make it 0.
skin_expr = "1 if frame < %d else (0 if frame < %d else 1)" % (ACT2, ACT4)
for idx in range(3):
    add_driver(skin_man, "scale", idx, skin_expr)

# Eyeballs that pop out of the face near the end of Act 1.
eyeballs = add_empty("Eyeballs", (0, 0, 0))
eyeballs.parent = skin_man
for sx in (-1, 1):
    ball = add_sphere("Eyeball", (sx * 0.13, 0.24, 2.06), 0.055,
                      eye_white)
    ball.parent = eyeballs
    pupil = add_sphere("Pupil", (sx * 0.13, 0.29, 2.06), 0.02, iris)
    pupil.parent = eyeballs
# They rise out of the sockets and float above the forehead
# between frames 10 and 50 (like the reference), and sink back
# into the sockets when the man is put back together (461-500).
add_driver(eyeballs, "location", 2,
           "0 if frame < 10 else ((frame-10)*0.39/40 if frame < 50 "
           "else (0.39 if frame < 461 else (0 if frame > 500 else "
           "0.39*(500-frame)/39)))")

# --- Muscle man ---
muscle_man = add_empty("MuscleMan", (0, 0, 0.56))
leg(muscle_man, "MuscleLegL", (-0.20, 0, 0.62), muscle)
leg(muscle_man, "MuscleLegR", (0.20, 0, 0.62), muscle)
mpelvis = add_sphere("MusclePelvis", (0, 0, 0.68), 0.29, muscle,
                     scale=(1.7, 1.1, 1.2))
mpelvis.parent = muscle_man
mabdomen = add_cylinder("MuscleAbdomen", (0, 0, 0.95), 0.41, 0.5,
                        muscle, radius_top=0.45)
mabdomen.parent = muscle_man
mchest = add_sphere("MuscleChest", (0, 0, 1.45), 0.41, muscle,
                    scale=(1.45, 0.85, 1.6))
mchest.parent = muscle_man
# Muscle fiber strips across the chest + center line.
for i, z in enumerate([1.30, 1.42, 1.54]):
    strip = add_box("MuscleStrip%d" % i, (0, 0.36, z),
                    (0.55, 0.02, 0.05), muscle_dark)
    strip.parent = muscle_man
center = add_box("MuscleCenter", (0, 0.37, 1.42), (0.04, 0.02, 0.45),
                 muscle_dark)
center.parent = muscle_man
limb(muscle_man, "MuscleArmL", (-0.62, 0, 1.62), muscle, side=-1)
limb(muscle_man, "MuscleArmR", (0.62, 0, 1.62), muscle, side=1)
mneck = add_cylinder("MuscleNeck", (0, 0, 1.82), 0.16, 0.3, muscle)
mneck.parent = muscle_man
mhead = add_sphere("MuscleHead", (0, 0, 2.02), 0.29, muscle,
                   scale=(1.0, 0.95, 1.15))
mhead.parent = muscle_man
# Empty dark eye sockets on the muscle head.
for sx in (-1, 1):
    sock = add_sphere("MuscleSocket", (sx * 0.13, 0.24, 2.06), 0.07,
                      eye_dark)
    sock.parent = muscle_man
join_parts(muscle_man, "MuscleBody")
# Scale driver AFTER the join (see skin man note).
muscle_expr = ("0 if frame < %d else (1 if frame < %d else 0)"
               % (ACT2, ACT3))
for idx in range(3):
    add_driver(muscle_man, "scale", idx, muscle_expr)

# --- Skeleton ---
skel = add_empty("Skeleton", (0, 0, 0.56))
# Legs: thin bones.
leg(skel, "BoneLegL", (-0.20, 0, 0.62), bone, r_thigh=0.07,
    r_shin=0.06)
leg(skel, "BoneLegR", (0.20, 0, 0.62), bone, r_thigh=0.07,
    r_shin=0.06)
# Pelvis.
bpelvis = add_sphere("BonePelvis", (0, 0, 0.68), 0.28, bone,
                     scale=(1.6, 1.0, 1.1))
bpelvis.parent = skel
# Spine.
spine = add_cylinder("BoneSpine", (0, -0.05, 1.15), 0.05, 0.9, bone)
spine.parent = skel
# Ribcage: 4 rings + sternum.
for i, (z, r) in enumerate([(1.05, 0.30), (1.20, 0.35),
                            (1.35, 0.37), (1.50, 0.34)]):
    rib = add_torus("Rib%d" % i, (0, 0, z), r, 0.035, bone)
    rib.parent = skel
sternum = add_box("Sternum", (0, 0.32, 1.28), (0.05, 0.03, 0.5), bone)
sternum.parent = skel
# Arms: thin bones.
limb(skel, "BoneArmL", (-0.60, 0, 1.62), bone, r_upper=0.06,
     r_fore=0.05, side=-1)
limb(skel, "BoneArmR", (0.60, 0, 1.62), bone, r_upper=0.06,
     r_fore=0.05, side=1)
# Skull: white ball, dark eye holes, nose hole, jaw.
skull = add_sphere("Skull", (0, 0, 2.02), 0.28, bone,
                   scale=(0.9, 0.85, 1.0))
skull.parent = skel
for sx in (-1, 1):
    hole = add_sphere("EyeHole", (sx * 0.11, 0.20, 2.06), 0.075,
                      eye_dark)
    hole.parent = skel
nosehole = add_cylinder("NoseHole", (0, 0.22, 1.94), 0.045, 0.10,
                        eye_dark, rotation=(math.radians(90), 0, 0))
nosehole.parent = skel
jaw = add_box("Jaw", (0, 0.12, 1.80), (0.22, 0.16, 0.12), bone)
jaw.parent = skel
join_parts(skel, "SkeletonBody")
# Scale driver AFTER the join (see skin man note).
skel_expr = ("0 if frame < %d else (1 if frame < %d else 0)"
             % (ACT3, ACT4))
for idx in range(3):
    add_driver(skel, "scale", idx, skel_expr)

# Pile of muscle + skin on the floor (Act 3): the removed layers.
# Blob positions are local to the pile empty.
pile = add_empty("Pile", (0.75, 0.45, 0))
blob1 = add_sphere("PileMuscle", (0, 0, 0.12), 0.35, muscle,
                   scale=(1.6, 1.2, 0.5))
blob1.parent = pile
blob2 = add_sphere("PileSkin", (-0.35, 0.25, 0.10), 0.28, skin,
                   scale=(1.4, 1.2, 0.45))
blob2.parent = pile
join_parts(pile, "PileBody")
# Scale driver AFTER the join (see skin man note).
pile_expr = "0 if frame < %d else 1" % ACT3
for idx in range(3):
    add_driver(pile, "scale", idx, pile_expr)

# ---------------------------------------------------------------- camera
# Vertical close-ups with hard cuts between the acts.
rig = add_empty("CamRig", (0, 0, 0))
target = add_empty("CamTarget", (0, 0, 2.46))
bpy.ops.object.camera_add(location=(0, 2.4, 2.56))
cam = bpy.context.active_object
cam.name = "Camera"
cam.data.lens = 35
cam.parent = rig
con = cam.constraints.new('TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'
scene.camera = cam


def set_shot(frame, cam_loc, lens, target_loc):
    cam.location = cam_loc
    cam.data.lens = lens
    target.location = target_loc
    cam.keyframe_insert(data_path="location", frame=frame)
    cam.data.keyframe_insert(data_path="lens", frame=frame)
    target.keyframe_insert(data_path="location", frame=frame)


# Shot 1: close on the face, slow push-in.
set_shot(1, (0, 2.4, 2.56), 35, (0, 0, 2.46))
set_shot(130, (0, 2.2, 2.56), 35, (0, 0, 2.46))
# Shot 2: torso, muscle man.
set_shot(131, (0, 2.4, 2.16), 35, (0, 0, 1.86))
set_shot(300, (0, 2.2, 2.16), 35, (0, 0, 1.86))
# Shot 3: wide, full skeleton + pile.
set_shot(301, (0, 4.9, 2.3), 35, (0, 0, 1.45))
set_shot(460, (0, 4.6, 2.3), 35, (0, 0, 1.45))
# Shot 4: close on the chest + name tag, skin man back.
set_shot(461, (0, 2.5, 2.36), 35, (0, 0, 2.16))
set_shot(528, (0, 2.3, 2.36), 35, (0, 0, 2.16))

os.makedirs(OUT_DIR, exist_ok=True)
bpy.ops.render.render(animation=True)
print("Rendered frames %d-%d into %s" % (FRAME_START, FRAME_END, OUT_DIR))
