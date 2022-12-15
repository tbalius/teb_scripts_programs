
# This script was written by Trent Balius in ~ 2014 while in the Shoichet Lab (UCSF).  
# This script is for preparing a molecule for symestry corected RMSD calculation in DOCK6
# It will convert a sybyl atom type to an element.  This is so that if your reference 
# molecule has a different atom type for an atom than your docked pose the RMSD correctly. 
# DOCK 6 uses the Hungarian Algorithm to creat a correspondance amoung poses.  


import math, sys
import os.path

from math import sqrt

# take a sybyl atom type and returns an element.  
# does this by spliting on the dot (.) in the type 
# and returning the chars before the dot.
def sybyl_to_ele(atom_type):
    atom_type=atom_type.replace(" ","")
    ele = atom_type.split('.')[0]
    print(ele)
    return ele


# read in a mol2 file and replace atom type with the element name. 
def read_mol2(filename,text1):
    file1 = open(filename,'r')
    lines  =  file1.readlines()

    atom_flag = False;

    #namestart = 47
    #namestop  = 51

    namestart = 42
    namestop  = 46

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) > 0):
             if (linesplit[0] == "@<TRIPOS>BOND"):
                atom_flag = False
             if (atom_flag):
                #atom_type = line[47:51] 
                atom_type = line[namestart:namestop] 
                print (atom_type)
                ele = sybyl_to_ele(atom_type) 
                #line_mod = '%s%-5s%s\n'%(line[0:47],ele,line[52:-1])
                line_mod = '%s%-5s%s\n'%(line[0:namestart],ele,line[namestop+1:-1])
                #text1 = text1+line
                text1 = text1+line_mod
             elif (not atom_flag):
                text1 = text1+line # add line to text1 for output
             if ( linesplit[0] == "@<TRIPOS>ATOM" ):
                atom_flag =  True
 

    file1.close()
    return text1
#################################################################################################################
#################################################################################################################
def main():
    if (len(sys.argv) != 3): # if no input
        print (" (1) mol2 file name,") 
        print (" (3) output mol2 ")
        return

    filename    = sys.argv[1]
    output      = sys.argv[2]

    text1 = '' # text to be writen to output
    text1 = read_mol2(filename,text1)

    file2 = open(output,'w')
    file2.write(text1)
    file2.close()

    return; 
#################################################################################################################
#################################################################################################################
main()
