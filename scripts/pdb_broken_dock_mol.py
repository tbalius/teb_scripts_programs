#! /usr/bin/python
import sys

### 
# This programs was writen by Trent E. Balius, the Shoichet Group, UCSF, 2012
###


class PDB_atom_info:
    def __init__(self, molname, chainid, resname, resnum, atomname, atomnum, X, Y, Z, boolhet):
        self.molname  = molname
        self.chainid  = chainid
        self.resname  = resname
        self.resnum   = resnum
        self.atomname = atomname
        self.atomnum  = atomnum
        self.X        = X
        self.Y        = Y
        self.Z        = Z
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
def id_close_atoms_lig(pdb_file, pdb_out):
    
    ## this function will read in a muli-pdb file conatining ligands from docking hits.

    file1 = open(pdb_file,'r')
   
    temp_atom_list  = []
    mol_list        = []
 
    lines    = file1.readlines()
   
    file1.close()
 
    resstr_cur = ' '
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "COMPND"):
                  molname = linesplit[2]
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
                   temp_atom_info = PDB_atom_info(molname,chainid,resname,resnum,atomname,atomnum,X,Y,Z,boolhet)
                   temp_atom_list.append(temp_atom_info)
            elif (linesplit[0] == "TER"):
                   mol_list.append(temp_atom_list)
                   temp_atom_list = []
    count = 0;        
    for mol in mol_list:
       #print count
       dist_mol(mol,0.5,1.8)  
       count = count + 1

    print "done"
    return 

#################################################################################################################
#################################################################################################################
def dist_mol(mol,di,dj):

    # this function calculates the all distances 
    # Curently this function will detect if an atom is conected to no other atom and will report it
    # we may want to expand this to detect improper conectivity but this is more 
    # difficult
    # C    4, 3, 2,
    # 
    if (len(mol) == 0 ):
       print "len(mol) == 0 "
       return False


    count = 0 # count the number of contact points 
    count_atom = 0 # count the number of contact points 
    count_clash = 0 # count the number of contact points 
    for i in range(len(mol)):
        count_atom = 0 # count the number of contact points 
        for j in range(len(mol)):
            if (i == j):
               continue
            atom1  = mol[i]
            atom2  = mol[j]

            di2       = di**2
            dj2       = dj**2

            X_diff_2 = (atom1.X - atom2.X)**2.0
            Y_diff_2 = (atom1.Y - atom2.Y)**2.0
            Z_diff_2 = (atom1.Z - atom2.Z)**2.0
            dist2    = (X_diff_2 + Y_diff_2 + Z_diff_2)

            if ( dist2 < dj2):
                #print "Atoms are close" + " dist2 = " + str(dist2)
                #print "likely bond::" + atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
                count =  count + 1
                count_atom =  count_atom + 1

            if (dist2 < di2):
                print "Warning: Atoms are too close," + " dist2 = " + str(dist2)
                count_clash = count_clash + 1
        if (count_atom == 0):
           print "there is an atom that has no connections "
           print atom1.molname + " :: " + " atom " + str(i) + " " + atom1.atomname + " " + atom1.atomnum #+ " " +  atom1.resname + " " + atom1.resnum + " " + atom1.chainid

    if (count_clash > 0):
       print "internal clash"

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a pdb file"
        print "id connected residues"
        print "writes a modified pdbfile with hetatoms combinded into redidue if short bond."
        print "python pdb_het_res_bonds_combine.py IN.pdb OUT.pdb CM"
        print "  IN.pdb -- input pdb file.  OUT.pdb -- output pdbfile."
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    id_close_atoms_lig(pdb_file,pdb_out)
    
    
#################################################################################################################
#################################################################################################################
main()
