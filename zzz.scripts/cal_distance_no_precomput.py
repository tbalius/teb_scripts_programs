
import sys, os, math
import mol2
#import sph_lib

# This is written by Trent Balius at FNLCR
# written in Nov, 2020

def distance(v1,v2):
    if (len(v1)!=len(v2)):
       print "error" 
       exit()
    dist = 0.0
    for i in range(len(v1)):
        dist = dist + (v1[i]-v2[i])**2.0
    dist = math.sqrt(dist)
    return dist

# two molecules
def cal_min_dist(mol_1,mol_2):
    min_dist = 10000.0
    for atom1 in mol_1.atom_list:
        for atom2 in mol_2.atom_list:
             dist = distance([atom1.X,atom1.Y,atom1.Z],[atom2.X,atom2.Y,atom2.Z])
             if dist < min_dist: 
                 min_dist = dist
    return min_dist

# one atom and a molecule, calc min distance between that atom and the molecule
def cal_min_dist_atom_mol(atom1,mol_2):
    min_dist = 10000.0
    for atom2 in mol_2.atom_list:
         dist = distance([atom1.X,atom1.Y,atom1.Z],[atom2.X,atom2.Y,atom2.Z])
         if dist < min_dist: 
             min_dist = dist
    return min_dist



def main():


   if len(sys.argv) != 6: # if no input
       print ("ERORR:")
       print ("syntex: distance_cal_no_precomput.py mol2_file(docked poses) mol2_file(find poses close to) threshold hname output ")
       return
 

   infilemol2_poses     = sys.argv[1]
   infilemol2_ref       = sys.argv[2]
   dist_threshold       = float(sys.argv[3])
   hname                = sys.argv[4]
   outfile              = sys.argv[5]

   print ("input file (poses)     = ", infilemol2_poses)
   print ("input file (reference) = ", infilemol2_ref)
   print ("threshold =", dist_threshold)
   print ("head_name =", hname)
   print ("outputprefix =", outfile)
   #mol2_vector  = mol2.read_Mol2_file(infilemol2_poses)
   mol2_vector  = mol2.read_Mol2_file_head(infilemol2_poses)
   mol2_ref  = mol2.read_Mol2_file(infilemol2_ref)[0]


   count = 0
   for mol in mol2_vector: 
       min_dist = 100000
       count_atom_lt_thes = 0
       for atom in mol.atom_list: 
           if (atom.type == 'H'): 
               continue
           #dist = cal_dist_closest_grid_point(grid_dist,gridscale,xn,yn,zn,origin,atom)
           #dist = cal_dist_tri_linear(grid_dist,gridscale,xn,yn,zn,origin,atom)
           dist =  cal_min_dist_atom_mol(atom,mol2_ref)
           if dist < min_dist: 
              min_dist = dist
           if dist < dist_threshold: 
               count_atom_lt_thes = count_atom_lt_thes + 1   
       if min_dist < dist_threshold: 
          print("mol %d,dist=%f,num_atom_lt_threshold=%d"%(count,min_dist,count_atom_lt_thes))
          #close_mol2.append(mol)
          mol.header = mol.header+"##########  %s_dist:                    %f\n"%(hname,min_dist)
          mol.header = mol.header+"##########  %s_num_atom_lt_threshold:   %d\n"%(hname,count_atom_lt_thes)
          mol2.append_mol2(mol, outfile+'.mol2')
       count = count + 1
   
   #file1.close()
main()


