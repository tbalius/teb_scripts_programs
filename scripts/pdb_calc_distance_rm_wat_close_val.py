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
    if len(sys.argv) != 5: # if no input
        print "This function takes as input two pdb files, output file name and the value"
        print "read in the ligand (pdb1) and the water positions (pdb2)."
        print "calculates distances and writes out a the overlaping atoms from the second file (water positions)"
        print len(sys.argv)
        return
    
    pdb_file1  = sys.argv[1]
    pdb_file2  = sys.argv[2]
    pdb_out    = sys.argv[3]
    val        = float(sys.argv[4])
    print "file 1: " + pdb_file1
    print "file 2: " + pdb_file2
    print "file out: " + pdb_out
    print "value: " + str(val)

    pdb1 = pdb.read_pdb(pdb_file1)[0]
    pdb2 = pdb.read_pdb(pdb_file2)[0]
    pdb2_close = pdb.cal_dists_close_val(pdb1,pdb2,val**2)
    pdb.output_pdb( pdb2_close, pdb_out) 
    
#################################################################################################################
#################################################################################################################
main()
