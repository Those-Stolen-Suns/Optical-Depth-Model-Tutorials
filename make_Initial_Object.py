### MAKE_INITITAL_OBJECT ###

# program for reading in FARGO3D data and creating the basis for a 3d optical depth model using the Blender Python terminal

# imports

import bpy
import numpy as np

# first want to get all the important variables for the mesh

nx = 100 # azimuthal zones
ny = 200 # radial zones
nz = 40 # colateral zones
lateral_angle = 0.3 # angle subtended laterally by the mesh
rmin = 0.4 # minimum radius
rmax = 2.0 # maximum radius
i = 1000 # frame number
abs_coeff = 1 # absorption coefficient
opt_depth_limit = 0.0001 # optical depth limit

# creating the object

# center the cursor

bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)

# create a circle with triangular slices

mesh1 = bpy.ops.mesh.primitive_circle_add(vertices = nx,radius = rmax,fill_type = 'TRIFAN')

# extrude the outer circle to a smaller inner circle, creating the donut shape we need

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_mode(type = 'FACE')
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(rmin/2, rmin/2, rmin/2))

# delete the excess geometry

bpy.ops.mesh.delete(type='FACE')
bpy.ops.mesh.select_face_by_sides(number = 3)
bpy.ops.mesh.delete(type='FACE')
bpy.ops.mesh.select_all(action = 'SELECT')

# you must do the loopcut using a mouse because the Blender terminal seems a bit dim in this regard
