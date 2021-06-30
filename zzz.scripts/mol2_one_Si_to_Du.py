#import mol2  ## this is a libary Trent Balius and Sudipto Mukherjee r. 
import mol2_python3 as mol2 ## this is a libary Trent Balius and Sudipto Mukherjee r. 
import math, sys
import os.path
import gzip
import copy
from math import sqrt

#################################################################################################################
# Written by Trent E Balius, March 2020 FNLCR  
# This script will modify the the mol2 file it will search for Si. 
# Remove the hydrogen that are connected to the Si atoms.
# There must be exactly one Si atom in the molecule.  
#################################################################################################################


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


#################################################################################################################
#################################################################################################################
def modify_mol2_file(mol2file, outputprefix):
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

       #if len(Si_atoms_index) != 2:
       if len(Si_atoms_index) != 1:
           print ("error")
           exit()

       count_h = [0,0] # remember how meny atoms are connected to the both Si
       Hlist = []  # remember which the atom index that are the connected bonds. 
       Si1 = Si_atoms_index[0]
       #Si2 = Si_atoms_index[1]
       for bond in mol.bond_list:
           if bond.a1_num-1 == Si1: 
              if (mol.atom_list[bond.a2_num-1].type == 'H'):
                  count_h[0]=count_h[0]+1
                  Hlist.append(bond.a2_num)
           if bond.a2_num-1 == Si1:
              if (mol.atom_list[bond.a1_num-1].type == 'H'):
                  count_h[0]=count_h[0]+1
                  Hlist.append(bond.a1_num)
           #if bond.a1_num-1 == Si2:
           #   if (mol.atom_list[bond.a2_num-1].type == 'H'):
           #       count_h[1]=count_h[1]+1
           #       Hlist.append(bond.a2_num)
           #if bond.a2_num-1 == Si2:
           #   if (mol.atom_list[bond.a1_num-1].type == 'H'):
           #       count_h[1]=count_h[1]+1
           #       Hlist.append(bond.a1_num)
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
                 #atom.name = 'D2'
                 atom.name = 'D1'
              elif count_h[0] == 2:
                 #atom.name = 'D1'
                 print ("error")
                 exit()
#          if atom.num-1 == Si2: 
#             atom.type = 'Du'
#             atom.Q = 0.0
#             if count_h[1] == 3: 
#                atom.name = 'D2'
#             elif count_h[1] == 2: # 
#                atom.name = 'D1'
           
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
    #if len(sys.argv) != 4: # if no input
    if len(sys.argv) != 3: # if no input
        print (" This script needs the following:")
        print (" (1) input mol2 file"             )
        print (" (2) output mol2 file"            )
        return

    mol2file       = sys.argv[1]
    mol2output     = sys.argv[2]

    modify_mol2_file(mol2file, mol2output) 

    return 
#################################################################################################################
#################################################################################################################
main()
