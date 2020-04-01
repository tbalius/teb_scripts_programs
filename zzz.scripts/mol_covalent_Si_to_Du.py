import mol2  ## this is a libary Trent Balius and Sudipto Mukherjee r. 
import math, sys
import os.path
import gzip
import copy
from math import sqrt

#################################################################################################################
# Written by Trent E Balius, March 2020 FNLCR  
# This script will modify the the mol2 file it will search for Si. 
# Remove the hydrogen that are connected to the Si atoms.
# There must be exactly two Si atoms in the molecule.  
# the one with 2 hydrogens becomes D1 with type Du.
# the one with 3 hydrogens becomes D2 with type Du.  
# ajusts the bond angle between D1 (S), D2 (CB), and first atom of the ligand. 
#################################################################################################################

def mag(v): 
   mag_v = 0
   for e in v: 
       mag_v = mag_v + e**2.0
   mag_v = math.sqrt(mag_v)
   return mag_v

def normal(v):
    mag_v = mag(v)
    return [v[0]/mag_v,v[1]/mag_v,v[2]/mag_v]

def dot_product(v1,v2):
    
   return (v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2])
   

def cross_product(v1,v2):
    c_x =  v1[1]*v2[2] - v1[2]*v2[1]
    c_y = -v1[0]*v2[2] + v1[2]*v2[0]
    c_z =  v1[0]*v2[1] - v1[1]*v2[0]
    #print v1
    #print v2
    #print c_x,c_y,c_z
    return [c_x,c_y,c_z]

def cross_product_normal(v1,v2):
    n = cross_product(v1,v2)
    mag_n = mag(n)
    return [n[0]/mag_n,n[1]/mag_n,n[2]/mag_n]

def calc_angle(v1, v2):
# this function calculates the cos t = v1 dot v2 / mag|v1| times mag|v2|.  cos t is returned. 
   print("v1 = ",v1)
   print("v2 = ",v2)
   dot = dot_product(v1,v2)
   v1mag = mag(v1)
   v2mag = mag(v2)
   cos_theata = dot/(v1mag*v2mag)
   if cos_theata > 1.0:
       cos_theata = 1.0
   print ('%s=%f,%s=%f,%s=%f,%s=%f\n'%('dot',dot,'mag1',v1mag,'mag2',v2mag,'cos_theta',cos_theata))
   return cos_theata

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

def translate(atoms,x,y,z):

    for atom in atoms:
        atom.X = atom.X + x
        atom.Y = atom.Y + y
        atom.Z = atom.Z + z

    

def make_integer_charge(mol,ori_charge): 
       ori_charge = round(ori_charge)
       N = (len(mol.atom_list) - 2)
       cur_charge = mol2.formal_charge(mol)
       avg_diff = (ori_charge-cur_charge)/N
       print ("current charge may be non-integer: %6.3f"%(mol2.formal_charge(mol)))
       print ("ori charge: %6.3f"%(ori_charge))
       print ("avergy diff charge: %6.3f"%(avg_diff))
       for atom in mol.atom_list:
           if atom.type == 'Du':
              continue
           atom.Q = atom.Q + avg_diff
       print ("forced to be an integer and same as original: %6.3f"%(mol2.formal_charge(mol)))


def print_atom(atom):
    print("%s, %f, %f, %f\n"%(atom.name,atom.X, atom.Y, atom.Z))

def ajust_angle(mol,angle):

    radians_input = angle * math.pi / 180
    for atom in mol.atom_list:
        if atom.name == 'D1':
        #if atom.name == 'D2':
           print (atom.name, atom.type, atom.num)
           atom2_num = atom.num
    connect_atom_nums = [] 
    for bond in mol.bond_list:
        if bond.a1_num == atom2_num:
           connect_atom_nums.append(bond.a2_num)
        if bond.a2_num == atom2_num:
           connect_atom_nums.append(bond.a1_num)

    if (len(connect_atom_nums) != 2):
        print ("Error",len(connect_atom_nums)) 
        exit()

    for num in connect_atom_nums:
        if mol.atom_list[num-1].name == 'D2':
        #if mol.atom_list[num-1].name == 'D1':
           #atom1_num = num
           atom3_num = num
        else:
           #atom3_num = num
           atom1_num = num
    print ("atom1 name = %s, atom2 name = %s, atom3 name = %s\n"%(mol.atom_list[atom1_num-1].name,mol.atom_list[atom2_num-1].name,mol.atom_list[atom3_num-1].name))
    atom1 = mol.atom_list[atom1_num-1]
    atom2 = mol.atom_list[atom2_num-1]
    atom3 = mol.atom_list[atom3_num-1]
    print ("atom1 name = %s, atom2 name = %s, atom3 name = %s\n"%(atom1.name,atom2.name,atom3.name))

    print ("calculate angle")
    v1= [atom1.X-atom2.X,atom1.Y-atom2.Y,atom1.Z-atom2.Z]
    v2= [atom3.X-atom2.X,atom3.Y-atom2.Y,atom3.Z-atom2.Z]
    cos_angle = calc_angle(v1,v2)
    radians = math.acos(cos_angle)
    print cos_angle, radians, 180 * radians / math.pi
    radians_delta = radians_input -radians
    print "delta", radians_delta, 180 * radians_delta / math.pi
    sign = 1.0
    if radians_delta < 0.0: 
       sign = -1.0
       print sign

    three_atoms = [atom1,atom2,atom3]
    for a in three_atoms:
        print_atom(a)

    trans_X = atom2.X
    trans_Y = atom2.Y
    trans_Z = atom2.Z 
    translate(three_atoms,-trans_X,-trans_Y,-trans_Z)
    for a in three_atoms:
        print_atom(a)

    #step one.# make basis set which contains . 
    # project onto the z,y plan.
    n_v1 = normal(v1)
    n_v2 = normal(v2)
    u = cross_product_normal(v1,v2)
    w = cross_product_normal(v1,u)

    mag_v1 = mag(v1)
    n = [v1[0]/mag_v1,v1[1]/mag_v1,v1[2]/mag_v1]

    print ("u = ",u)
    print ("w = ",w)
    print ("n = ",n)

    M = [[w[0],n[0],u[0]], [w[1],n[1],u[1]], [w[2],n[2],u[2]]]   
    inverseM = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
       for j in range(3):
           inverseM[j][i] = M[i][j]

    print (M)
    print (inverseM)
    #rotate(three_atoms,M)
    print "start"
    for a in three_atoms:
        print_atom(a)

    print "rotate"
    rotate(three_atoms,inverseM)
    for a in three_atoms:
        print_atom(a)
    
    #rotate_x([atom3],math.cos(0.35))
    #rotate_y([atom3],math.cos(0.35))
    rotate_z([atom3],math.cos(radians_delta),sign)

    print ("rotate back")
    rotate(three_atoms,M)
    #translate(three_atoms,atom2.X,atom2.Y,atom2.Z)
    translate(three_atoms,trans_X,trans_Y,trans_Z)
    for a in three_atoms:
        print_atom(a)
#    print "rotate agian"
#    rotate(three_atoms,inverseM)
#    for a in three_atoms:
#        print_atom(a)
    print ("calculate angle")
    v1= [atom1.X-atom2.X,atom1.Y-atom2.Y,atom1.Z-atom2.Z]
    v2= [atom3.X-atom2.X,atom3.Y-atom2.Y,atom3.Z-atom2.Z]
    cos_angle = calc_angle(v1,v2)
    radians = math.acos(cos_angle)
    print cos_angle, radians, 180 * radians / math.pi


#################################################################################################################
#################################################################################################################
def modify_mol2_file(mol2file, outputprefix, ang):
    ## read in mol2 file
    frist = True
    mollist = mol2.read_Mol2_file(mol2file) 
    for mol in mollist:
       ori_formal_charge = mol2.formal_charge(mol)
       n = len(mol.atom_list) 
       Si_atoms_index = []
       for i in range(n):
           if mol.atom_list[i].type == 'Si':
              print (mol.atom_list[i].type, mol.atom_list[i].name)
              Si_atoms_index.append(i)

       if len(Si_atoms_index) != 2:
           print ("error")
           exit()

       count_h = [0,0] # remember how meny atoms are connected to the both Si
       Hlist = []  # remember which the atom index that are the connected bonds. 
       Si1 = Si_atoms_index[0]
       Si2 = Si_atoms_index[1]
       for bond in mol.bond_list:
           if bond.a1_num-1 == Si1: 
              if (mol.atom_list[bond.a2_num-1].type == 'H'):
                  count_h[0]=count_h[0]+1
                  Hlist.append(bond.a2_num)
           if bond.a2_num-1 == Si1:
              if (mol.atom_list[bond.a1_num-1].type == 'H'):
                  count_h[0]=count_h[0]+1
                  Hlist.append(bond.a1_num)
           if bond.a1_num-1 == Si2:
              if (mol.atom_list[bond.a2_num-1].type == 'H'):
                  count_h[1]=count_h[1]+1
                  Hlist.append(bond.a2_num)
           if bond.a2_num-1 == Si2:
              if (mol.atom_list[bond.a1_num-1].type == 'H'):
                  count_h[1]=count_h[1]+1
                  Hlist.append(bond.a1_num)
       print (Hlist) 
       print (count_h) 

       # (1) remove 5 hydrogen atoms, 
       # (2) change Si to Du and the atom name, 

       new_atomlist = []
       for i,atom in enumerate(mol.atom_list):
           print(i, atom.num)
           #exit()
           if atom.num in Hlist: 
              continue
           if atom.num-1 == Si1: 
              atom.type = 'Du'
              atom.Q = 0.0
              if count_h[0] == 3: 
                 atom.name = 'D2'
              elif count_h[0] == 2:
                 atom.name = 'D1'
           if atom.num-1 == Si2: 
              atom.type = 'Du'
              atom.Q = 0.0
              if count_h[1] == 3: 
                 atom.name = 'D2'
              elif count_h[1] == 2: # 
                 atom.name = 'D1'
           
           new_atomlist.append(copy.copy(atom))
       # (3) generate mapping from old to new atom numbering to be used in the bond modification. 
       atom_num_map = {}
       for i,atom in enumerate(new_atomlist):
           atom_num_map[atom.num] = i+1
           atom.num = i+1

       # (4) remove bonds that contain any of the removed hydrogens.
       new_bondlist = []
       for i,bond in enumerate(mol.bond_list):
           if bond.a1_num in Hlist or bond.a2_num in Hlist:
              continue  
           new_bondlist.append(copy.copy(bond))

       # (5) renumber the bonds, map old atom numbering to new atom number for bonds
       i = 1
       for bond in new_bondlist:
           bond.num = i
           bond.a1_num = atom_num_map[bond.a1_num]
           bond.a2_num = atom_num_map[bond.a2_num]
           i = i + 1

       mol.atom_list = new_atomlist
       mol.bond_list = new_bondlist

       # ajust Si-Si-C bond angle.  Looks like it is 90 deg. 
       ajust_angle(mol,ang)

       # ajust the partial charge to make it an integer.  
       make_integer_charge(mol, ori_formal_charge)

       #exit()
       filename = outputprefix + '.mol2'
       if frist:
          mol2.write_mol2(mol,filename)
          frist = False
       else:
          mol2.append_mol2(mol,filename)
          
    return
    

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print " This script needs the following:"
        print " (1) input mol2 file"
        print " (2) output mol2 file"
        print " (3) angle"
        return

    mol2file       = sys.argv[1]
    outputprefix   = sys.argv[2]
    angle          = float(sys.argv[3])

    modify_mol2_file(mol2file, outputprefix, angle) 

    return 
#################################################################################################################
#################################################################################################################
main()
