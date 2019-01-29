import math, sys
import os.path

from math import sqrt

#################################################################################################################
############################################################
##reads in multi-mol2 file (file) and outputs the molicule 
##with the name (name) to the file name.mol2.
############################################################
def read_multi_mol2(filename,molname):
    file1 = open(filename,'r')
    file2 = open(molname+".mol2",'w')
    lines  =  file1.readlines()

    print_flag = False;

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) > 0):
             
             if (linesplit[0] == "##########" and linesplit[1] == "Name:" and linesplit[2] == molname):
             #if (linesplit[0] == "Molecule:" and linesplit[1] == molname):
                print line
                print_flag = True
             elif (print_flag and linesplit[0] == "##########" and  linesplit[1] == "Name:"):
             #elif (print_flag and linesplit[0] == "Molecule:"):
                print_flag = False
             if (print_flag):
                #print line
                file2.write(line);
    file1.close()
    file2.close()
    return;
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print " multi-mol2 file name and mol name you want to search for and output ";
        return

    filename  = sys.argv[1];
    molname   = sys.argv[2];

    print "searching " + filename + " for molecule " + molname

    read_multi_mol2(filename,molname)   

    return; 
#################################################################################################################
#################################################################################################################
main()
