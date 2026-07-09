
# This script was written by Trent Balius in ~ 2014 while in the Shoichet Lab (UCSF).  
# This script is for preparing a molecule for symestry corected RMSD calculation in DOCK6
# It will convert a sybyl atom type to an element.  This is so that if your reference 
# molecule has a different atom type for an atom than your docked pose the RMSD correctly. 
# DOCK 6 uses the Hungarian Algorithm to creat a correspondance amoung poses.  

# Trent updated on 2026/07/09 to use mol2 libary. this solves some bugs.


import math, sys
import os.path
import mol2_python3 as mol2

from math import sqrt

# take a sybyl atom type and returns an element.  
# does this by spliting on the dot (.) in the type 
# and returning the chars before the dot.
def sybyl_to_ele(atom_type):
    atom_type=atom_type.replace(" ","")
    ele = atom_type.split('.')[0]
    print(ele)
    return ele


#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print (" (1) mol2 file name,") 
        print (" (3) output mol2 ")
        return

    filename    = sys.argv[1]
    output      = sys.argv[2]

    mols = mol2.read_Mol2_file(filename)
    print("num = %d"%len(mols))
    for mol in mols:
        for atom in mol.atom_list:
            atom.type = sybyl_to_ele(atom.type) 

    #file2 = open(output,'w')
        mol2.append_mol2(mol,output)

    return; 
#################################################################################################################
#################################################################################################################
main()
