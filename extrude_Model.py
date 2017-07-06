# program for reading in blender data and creating a 3d model for a single frame

# imports

import bpy
import numpy as np

# first want to get all the important variables for the mesh

nx = 100 # azimuthal zones
ny = 200 # radial zones
nz = 40 # colateral zones
odl = 1 # optical depth limit
lateral_angle = 0.3
rmin = 0.4 # minimum radius
rmax = 2.0 # maximum radius
i = 100 # frame number
abs_coeff = 1 # absorption coefficient
opt_depth_limit = 0.0001 # optical depth limit

# import fargo data

dat = 'gasdens1000.dat'
data = np.fromfile(dat).reshape(nz,ny,nx)

# what data do we want? We want the optical depth looking from above for each 2d 
# den

# let's do it den by den

def opticaldepthcont(kappa,dz,rho):
    # contribution to the optical depth from a den of absorption coefficient
    # kappa, vertical lateral_angle dz, and density rho
    cont = kappa*dz*rho
    return cont

  
# let's use the cursor to select each face

def denselector(rad,az):
    bpy.ops.mesh.select_all(action = 'DESELECT')
    azstep = 2*np.pi/nx
    radialstep = (rmax-rmin)/ny
    x = (rmin+(radialstep/2)+rad*radialstep)*np.sin((azstep/2)+az*azstep)
    y = (rmin+(radialstep/2)+rad*radialstep)*np.cos((azstep/2)+az*azstep)
    bpy.context.scene.cursor_location = (x, y, 0.0)
    cur = bpy.context.scene.cursor_location
    o   = bpy.context.object
    bpy.ops.object.mode_set(mode = 'OBJECT')
    faceIdx = o.closest_point_on_mesh(cur)[-1]
    if faceIdx != -1:
        o.data.polygons[faceIdx].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
    
# now let's play with the dens, making sure to account for "gaps" in the disc

def denextruder(dz):
    if np.absolute(dz) > 100000:
        bpy.ops.mesh.delete(type = 'FACE')
    else:
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.translate(value = (0,0,dz))            

# need to calculate the vertical thickness of the zones. Note that we use a small angle approximation

def zstep(rnumber, rmax, rmin, ny, nz, lateral_angle):
        # zstep = lateral_angle/nz # option for flattening disc out
        rstep = (rmax-rmin)/ny
        r = rmin + rstep*rnumber
        zheightend = r*np.tan(lateral_angle/2)
        zheight = zheightend*(r/rmax)
        zstep = 2*zheight/nz
        return zstep

# now let's do a main loop

counter = 0
failcounter = 0
n = 0
while n < ny:
    m = 0
    while m < nx:
        denselector(n,m)
        opticaldepth = 0
        counter += 1
        percentage = (counter/(ny*nx))*100
        print(str(round(percentage,2))+"% "+"COMPLETE")
        for i in range(0, nz):
            if opticaldepth < opt_depth_limit:
                opticaldepth += opticaldepthcont(abs_coeff, zstep(n, rmax, rmin, ny, nz, lateral_angle), data[nz-1-i][n][m])
                if i == nz-1:
                    print("There is no calculatable surface boundary")
                    failcounter += 1
                    failpercentage = (failcounter/(ny*nx))*100
                    print(str(round(failpercentage,2))+"% "+"NO BOUNDARY")
                    bpy.ops.mesh.delete(type = 'FACE')
                    
            else:
                rstep = (rmax-rmin)/ny
                r = rmin + rstep*n
                zheightend = r*np.tan(lateral_angle/2)
                zheight = zheightend*(r/rmax)
                zstepvalue = 2*zheight/nz
                zdistance = (2*zheight)-((i)*(zstepvalue))
                break
        m = m+1
        denextruder(zdistance)
    n = n+1
print(str(round(failpercentage,2))+"% "+"NO BOUNDARY")
print("Done!")

# time to render