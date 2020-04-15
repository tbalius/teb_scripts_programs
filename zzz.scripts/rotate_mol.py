import mol2  ## this is a libary Trent Balius and Sudipto Mukherjee r. 
import math, sys
import os.path
import gzip
import copy
from math import sqrt

#################################################################################################################
# Written by Trent E Balius, March 2020 FNLCR  
# This script will rotate a molecule around the x,y,z axes
#################################################################################################################


def rotate_x(atoms,cos_t,sign):
#  |x_n|   | 1      0      0      | |x_o|
#  |y_n| = | 0    cos(t)  -sin(t) | |y_o|
#  |z_n|   | 0    sin(t)  cos(t)  | |z_o|

    #print cos_t
    sin_t = sign*math.sqrt((1 - cos_t*cos_t))

    for atom in atoms:
        X = atom.X
        Y = atom.Y
        Z = atom.Z
        #atom.X = atom.X + 0.0 + 0.0
        atom.Y = 0.0 + Y*cos_t - Z*sin_t
        atom.Z = 0.0 + Y*sin_t + Z*cos_t

def rotate_y(atoms,cos_t,sign):
#  |x_n|   | cos(t)  0 sin(t)  | |x_o|
#  |y_n| = |  0      1   0     | |y_o|
#  |z_n|   | -sin(t) 0 cos(t)  | |z_o|

    sin_t = sign*math.sqrt(1 - cos_t*cos_t)
    for atom in atoms:
        X = atom.X
        Y = atom.Y
        Z = atom.Z
        atom.X = X*cos_t + 0.0 + Z*sin_t
        #atom.Y = 0.0 + atom.Y +0.0
        atom.Z = -1.0 * X*sin_t + 0.0 + Z*cos_t

def rotate_z(atoms,cos_t,sign):
#  |x_n|   | cos(t)  -sin(t) 0 | |x_o|
#  |y_n| = | sin(t)  cos(t)  0 | |y_o|
#  |z_n|   |   0       0     1 | |z_o|

    sin_t = sign*math.sqrt(1 - cos_t*cos_t)
    for atom in atoms:
        X = atom.X
        Y = atom.Y
        Z = atom.Z
        atom.X = X *cos_t - Y*sin_t + 0.0
        atom.Y = X*sin_t  + Y*cos_t + 0.0
        #atom.Z = 0.0 +0.0 + atom.Z

def rotate(atoms,M):
# use a matrix
    for atom in atoms:
        X = atom.X
        Y = atom.Y
        Z = atom.Z
        atom.X = X *M[0][0] + Y * M[0][1] + Z *M[0][2]
        atom.Y = X *M[1][0] + Y * M[1][1] + Z *M[1][2]
        atom.Z = X *M[2][0] + Y * M[2][1] + Z *M[2][2]
        #atom.X = atom.X *M[0][0] + atom.Y * M[1][0] + atom.Z *M[2][0]
        #atom.Y = atom.X *M[0][1] + atom.Y * M[1][1] + atom.Z *M[2][1]
        #atom.Z = atom.X *M[0][2] + atom.Y * M[1][2] + atom.Z *M[2][2]
#def rotate(v,M):
#    
#    #v[0] = v[0] *M[0][0] + v[1] * M[0][1] + v[2] *M[0][2]       
#    #v[1] = v[0] *M[1][0] + v[1] * M[1][1] + v[2] *M[1][2]       
#    #v[2] = v[0] *M[2][0] + v[1] * M[2][1] + v[2] *M[2][2]       
#    return v

def translate(mol,xtran,ytran,ztran):
    for i in range(len(mol.atom_list)): 
        mol.atom_list[i].X = mol.atom_list[i].X + xtran
        mol.atom_list[i].Y = mol.atom_list[i].Y + ytran
        mol.atom_list[i].Z = mol.atom_list[i].Z + ztran
    return



#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 6: # if no input
        print (" This script needs the following:")
        print (" (1) input mol2 file"             )
        print (" (2) output mol2 file"            )
        print (" (3-5) x, y, z rotation angles"   )
        print (" rotation order: x, y, then z with be rotated in that order. "   )
        return
    
    mol2file       = sys.argv[1]
    outputfile     = sys.argv[2]
    xangle         = float(sys.argv[3])
    yangle         = float(sys.argv[4])
    zangle         = float(sys.argv[5])

    cos_x = math.cos(xangle)
    xsign = 1.0
    if xangle < 0.0:
       xsign = -1.0

    cos_y = math.cos(yangle)
    ysign = 1.0
    if yangle < 0.0:
       ysign = -1.0

    cos_z = math.cos(zangle)
    zsign = 1.0
    if zangle < 0.0:
       zsign = -1.0

    mols = mol2.read_Mol2_file(mol2file)
    first = True
    for m in mols: 
       center = mol2.centre_of_mass(m) 
       translate(m,-center[0],-center[1],-center[2])
       rotate_x(m.atom_list,cos_x,xsign)
       rotate_y(m.atom_list,cos_y,ysign)
       rotate_z(m.atom_list,cos_z,zsign)
       translate(m,center[0],center[1],center[2])
       if first:
           mol2.write_mol2(m,outputfile)
           first = False
       else: 
           mol2.append_mol2(m,outputfile)

    return 
#################################################################################################################
#################################################################################################################
main()
