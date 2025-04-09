#import mol2  ## this is a libary Trent Balius and Sudipto Mukherjee r. 
import mol2_python3 as mol2
import math, sys
import os.path
import gzip
import copy
from math import sqrt

#################################################################################################################
# Written by Trent E Balius, August 2024 FNLCR  
# This script will remove Du atoms from a mol2 file. 
# used code from mol_covalent_Si_to_Du.py
#################################################################################################################


#################################################################################################################
#################################################################################################################
def modify_mol2_file(mol2file, outputprefix):
    ## read in mol2 file
    frist = True
    mollist = mol2.read_Mol2_file(mol2file) 
    for mol in mollist:

       new_atomlist = []
       Dulist = []  # remember which the atom index that are the connected bonds. 
       for atom in mol.atom_list:
           if atom.type == 'Du':
               Dulist.append(atom.num)
           else: 
               new_atomlist.append(atom)
       print (Dulist) 


       # (2) generate mapping from old to new atom numbering to be used in the bond modification. 
       atom_num_map = {}
       for i,atom in enumerate(new_atomlist):
           atom_num_map[atom.num] = i+1
           atom.num = i+1

       # (3) remove bonds that contain any of the removed Du.
       new_bondlist = []
       for i,bond in enumerate(mol.bond_list):
           if bond.a1_num in Dulist or bond.a2_num in Dulist:
              continue  
           new_bondlist.append(copy.copy(bond))

       # (3) renumber the bonds, map old atom numbering to new atom number for bonds
       i = 1
       for bond in new_bondlist:
           bond.num = i
           bond.a1_num = atom_num_map[bond.a1_num]
           bond.a2_num = atom_num_map[bond.a2_num]
           i = i + 1

       mol.atom_list = new_atomlist
       mol.bond_list = new_bondlist

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
