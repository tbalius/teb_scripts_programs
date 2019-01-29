#! /usr/bin/python
import sys, math

### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2012
# edited in 2015.
# edited in 2017.
###


class PDB_atom_info:
    def __init__(self, molname, chainid, resname, resnum, atomname, atomnum, X, Y, Z, bfact, boolhet):
        self.molname  = molname
        self.chainid  = chainid
        self.resname  = resname
        self.resnum   = resnum
        self.atomname = atomname
        self.atomnum  = atomnum
        self.X        = X
        self.Y        = Y
        self.Z        = Z
        self.bfact    = bfact
        self.boolhet  = boolhet

    def __cmp__(self, other):
        return cmp(self.chainid, other.chainid)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byResId(x, y):
    str1 = x.resname + x.chainid + x.resnum
    str2 = y.resname + y.chainid + y.resnum
    return cmp(str1,str2)

#################################################################################################################
def read_pdb(pdb_file):
    
    ## this function will read in a muli-pdb file conatining ligands from docking hits.

    #print "read_pdb"
    file1 = open(pdb_file,'r')
   
    temp_atom_list  = []
    chain_list      = []
 
    lines    = file1.readlines()
   
    file1.close()
 
    resstr_cur = ' '

    linesplit = [""]
  
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                   chainid  = line[21]
                   resname  = line[17:20]
                   resnum   = line[23:26]
                   atomname = line[12:16]
                   atomnum  = line[9:12]
                   X        = float(line[30:38])
                   Y        = float(line[38:46])
                   Z        = float(line[46:54])
                   boolhet  = (linesplit[0] == "HETATM")
                   temp_atom_info = PDB_atom_info('',chainid,resname,resnum,atomname,atomnum,X,Y,Z,0.0,boolhet)
                   temp_atom_list.append(temp_atom_info)
            elif (linesplit[0] == "TER" or linesplit[0] == "END"):
                   chain_list.append(temp_atom_list)
                   temp_atom_list = []
    if not (linesplit[0] == "TER" or linesplit[0] == "END"):
       chain_list.append(temp_atom_list)

    return chain_list[0]

#################################################################################################################
#################################################################################################################
def output_pdb(pdb,filename):
#ATOM      1  N   GLY A 107      29.591  15.176   9.090  1.00 16.16           N
#ATOM      2  CA  GLY A 107      28.354  15.043   9.850  1.00 16.60           C
#ATOM      3  C   GLY A 107      27.209  14.507   9.009  1.00 17.59           C
#ATOM      4  O   GLY A 107      27.289  14.440   7.776  1.00 17.22           O
#ATOM      5  N   GLU A 108      26.121  14.116   9.667  1.00 18.40           N
#ATOM      6  CA  GLU A 108      24.934  13.662   8.945  1.00 19.69           C
#ATOM      7  C   GLU A 108      24.330  14.741   8.029  1.00 20.17           C
#ATOM      8  O   GLU A 108      23.772  14.423   6.970  1.00 20.99           O
#ATOM      9  N   THR A 109      24.471  16.007   8.419  1.00     21.05           N
#ATOM     10  CA  THR A 109      23.983  17.112   7.589  1.00 21.72           C
#
    file1 = open(filename,'w')
    for atom in pdb:
        file1.write("ATOM  %5d %2s %3s %1s%4d%12.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (int(atom.atomnum), atom.atomname, atom.resname, atom.chainid, int(atom.resnum), atom.X, atom.Y, atom.Z, 1.00 , atom.bfact, atom.atomname[1:2]) )

    file1.close()

#################################################################################################################
#################################################################################################################

def cal_dists(pdb1,pdb2,t):
    thres = t ** 2.0
    for atom1 in pdb1:
        for atom2 in pdb2:
            d2 = (atom1.X - atom2.X)**2 + (atom1.Y - atom2.Y)**2 + (atom1.Z - atom2.Z)**2
            if d2 < thres:
               print "dist = "+str(d2**(1.0/2.0)) 
               print atom1.resname, atom1.resnum, atom1.atomname, atom1.atomnum 
               print atom2.resname, atom2.resnum, atom2.atomname, atom2.atomnum 


#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print "This function takes as input two pdb files and a theshold"
        print "calculates distances and writes out a report"
        print len(sys.argv)
        return
    
    pdb_file1  = sys.argv[1]
    pdb_file2  = sys.argv[2]
    t          = float(sys.argv[3])
    #pdb_out   = sys.argv[3]
    print "file 1: " + pdb_file1
    print "file 2: " + pdb_file2
    print "threshold: %f"%(t)

    pdb1 = read_pdb(pdb_file1)
    pdb2 = read_pdb(pdb_file2)
    cal_dists(pdb1,pdb2,t)
    
    #output_pdb(ave_pdb, pdb_out) 
    
#################################################################################################################
#################################################################################################################
main()
