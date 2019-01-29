#! /usr/bin/python
import sys, math

### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2012
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

    file1 = open(pdb_file,'r')
   
    temp_atom_list  = []
    chain_list      = []
 
    lines    = file1.readlines()
   
    file1.close()
 
    resstr_cur = ' '
  
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "ATOM"):
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

    return chain_list[0]

#################################################################################################################
#################################################################################################################
def averge_stand_dev(pdbs):

    n = len(pdbs)

    avg_X  = []
    avg_Y  = []
    avg_Z  = []
    var_X  = []
    var_Y  = []
    var_Z  = []
    var_A  = [] # x,y,z averge std
    avg_X2 = []
    avg_Y2 = []
    avg_Z2 = []

    for atom in pdbs[0]:
        avg_X.append(0.0)
        avg_Y.append(0.0)
        avg_Z.append(0.0)
        var_X.append(0.0)
        var_Y.append(0.0)
        var_Z.append(0.0)
        var_A.append(0.0)
        avg_X2.append(0.0)
        avg_Y2.append(0.0) 
        avg_Z2.append(0.0)

    n_pdbatoms = len(pdbs[0])

    for pdb in pdbs:
        print "####"
        if n_pdbatoms != len(pdb): 
            print "n_pdbatoms != len(pdb)", n_pdbatoms, len(pdb) 
            exit()
        for i in range(len(pdb)): # for each atom
            print pdb[i].X,pdb[i].Y,pdb[i].Z
            avg_X[i] = avg_X[i] + pdb[i].X
            avg_Y[i] = avg_Y[i] + pdb[i].Y
            avg_Z[i] = avg_Z[i] + pdb[i].Z
            avg_X2[i] = avg_X2[i] + (pdb[i].X)**2
            avg_Y2[i] = avg_Y2[i] + (pdb[i].Y)**2
            avg_Z2[i] = avg_Z2[i] + (pdb[i].Z)**2
        #print avg_X[5], avg_Y[5], avg_Z[5]

    
    atom_list = []
    # calculate the variance for each atom
    # var[X] = E[X^2] - E[X]^2
    for i in range(len(avg_X)): # for each atom
        avg_X[i] = avg_X[i]/n 
        avg_Y[i] = avg_Y[i]/n 
        avg_Z[i] = avg_Z[i]/n 

        avg_X2[i] = avg_X2[i]/n
        avg_Y2[i] = avg_Y2[i]/n
        avg_Z2[i] = avg_Z2[i]/n

        var_X[i] = avg_X2[i] - (avg_X[i])**2
        var_Y[i] = avg_Y2[i] - (avg_Y[i])**2
        var_Z[i] = avg_Z2[i] - (avg_Z[i])**2

        var_A[i] = (var_X[i]+var_Y[i]+var_Z[i])/3
        print "pdb0 X = ", pdbs[0][i].X, pdbs[0][i].Y, pdbs[0][i].Z
        print "X = ", avg_X[i],  avg_Y[i], avg_Z[i] 
        print "X2 = ", avg_X2[i], avg_Y2[i], avg_Z2[i]
        print "var = ", var_X[i], var_Y[i], var_Z[i], "Ave = ", var_A[i]

        X = avg_X[i]; Y = avg_Y[i]; Z = avg_Z[i]; B = math.sqrt(var_A[i]) * 100.0

        temp_atom_info = PDB_atom_info('',pdbs[0][i].chainid,pdbs[0][i].resname,pdbs[0][i].resnum,pdbs[0][i].atomname,pdbs[0][i].atomnum,X,Y,Z,B,pdbs[0][i].boolhet)
        atom_list.append(temp_atom_info)
        
    return atom_list
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
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a list of pdb stored in a file"
        print "This function takes as outputs a averge pdb file"
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    file = open(pdb_file,'r')

    filelist = []
    for line in file:
         processed_line =  line.split()[0]
         print processed_line
         filelist.append(processed_line)
    file.close()

    pdb_list = []
    for filename in filelist:
         pdb = read_pdb(filename)
         pdb_list.append(pdb)

    ave_pdb = averge_stand_dev(pdb_list) 
    output_pdb(ave_pdb, pdb_out) 
    
#################################################################################################################
#################################################################################################################
main()
