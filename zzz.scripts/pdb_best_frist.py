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
    if len(sys.argv) != 4: # if no input
        print "This function takes as input one pdb files (sorted) and starting with the frist atom remove all atoms within a certan distance."
        print len(sys.argv)
        return
    
    pdb_file1   = sys.argv[1]
    dist_thres  = float(sys.argv[2])
    pdb_out     = sys.argv[3]

    print "file 1:    " + pdb_file1
    print "threshold: " + str(dist_thres)
    print "file 2:    " + pdb_out

    pdb1 = pdb.read_pdb(pdb_file1)[0]

    alist = pdb1
    pdbheads = []
    while len(alist) > 0:
       head = alist[0]
       print "\ncluster for atom %s"% head.atomnum
       pdbheads.append(head)
       newlist = []
       for atom in alist: 
           d = pdb.cal_dist(head,atom)
           if d > dist_thres: #threshold: 
              newlist.append(atom)
           else:# else it is removed from list
              print "   member atom %s"%atom.atomnum
       alist = newlist  

    pdb.output_pdb( pdbheads, pdb_out) 
    
#################################################################################################################
#################################################################################################################
main()
