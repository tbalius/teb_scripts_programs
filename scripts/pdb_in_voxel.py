#! /usr/bin/python
import sys, math
import pdb_lib 
### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2017
# It counts how meny waters are nearby a extreme point
###


#def cal_dists(atom1,atom2):
#    d2 = (atom1.X - atom2.X)**2 + (atom1.Y - atom2.Y)**2 + (atom1.Z - atom2.Z)**2
#    return math.sqrt(d2)

def in_voxel(atom1,atom2,val):
    boolval = False
    #print math.fabs(atom1.X - atom2.X), val
    if ((math.fabs(atom1.X - atom2.X) <= val) and 
       (math.fabs(atom1.Y - atom2.Y) <= val) and
       (math.fabs(atom1.Z - atom2.Z) <= val)):
        boolval = True
    return boolval
    

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input two pdb files"
        print "calculates distances and writes out a report"
        print len(sys.argv)
        return
    
    pdb_file1  = sys.argv[1]
    pdb_file2  = sys.argv[2]
    #pdb_out   = sys.argv[3]
    print "center of voxal, file 1: " + pdb_file1
    print "list of waters, file 2: " + pdb_file2

    pdb1 = pdb_lib.read_pdb(pdb_file1)
    pdb2 = pdb_lib.read_pdb(pdb_file2)

    atomcount = [] # count how meny atoms are in each voxel    
    # intialize
    for i in range(len(pdb1)):
        atomcount.append(0)

    i = 0
    for voxelatom in pdb1:
        for atom in pdb2:
            #print atom.atomname
            if atom.atomname.replace(" ","") != "O":
                continue 
            if (in_voxel(voxelatom,atom,0.25)):
                atomcount[i] = atomcount[i] + 1
        i = i + 1 

    for i in range(len(pdb1)):
        print "voxel%d, %d"%(i, atomcount[i])
    print len(pdb2)/3
    #output_pdb(ave_pdb, pdb_out) 
    
#################################################################################################################
#################################################################################################################
main()
