#! /usr/bin/python
import sys, math 
import pdb_lib as pdb 

### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2012
# edited in 2015.
###

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input two pdb files"
        print "read in the  xtal waters (pdb1) and the water positions predicted by GIST (pdb2)."
        print len(sys.argv)
        return
    
    pdb_file1  = sys.argv[1]
    pdb_file2  = sys.argv[2]
    #pdb_out   = sys.argv[3]
    print "file 1: " + pdb_file1
    print "file 2: " + pdb_file2

    pdb1 = pdb.read_pdb(pdb_file1)
    pdb2 = pdb.read_pdb(pdb_file2)
    pdb.cal_dists_TP_FP_FN(pdb1,pdb2)
    
#################################################################################################################
#################################################################################################################
main()
