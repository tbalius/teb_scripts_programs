#! /usr/bin/python
import sys

class PDB_atom_info:
    def __init__(self, chainid, resname, resnum, boolhet):
        self.chainid = chainid
        self.resname = resname
        self.resnum  = resnum
        self.boolhet = boolhet

    def __cmp__(self, other):
        return cmp(self.chainid, other.chainid)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byChainId(x, y):
    return cmp(x.chainid, y.chainid)
        

#################################################################################################################
def chain_info(pdb_file):
    ## reads in pdb id how meny residues are in each chain
    ## if chain has fewer than 10 residues then it is likely a ligand
    max_num_res = 10 
    file1 = open(pdb_file,'r')
   
    pdb_info = []
    lines  =  file1.readlines()
    
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                chainid = line[21];
                resname = line[17:20];
                resnum  = line[23:26];
                boolhet = (linesplit[0] == "HETATM")
                if (ok_residue(resname)): # do not include waters etc.
                   #print resname + " " + str(boolhet)
                   temp_atom_info = PDB_atom_info(chainid,resname,resnum,boolhet)
                   pdb_info.append(temp_atom_info)
                #else: 
                #   print resname + " " + str(boolhet) 
                   


    pdb_info.sort(byChainId)

    current_atom = pdb_info[0]
    curent_chain = pdb_info[0].chainid
    curent_res   = str(pdb_info[0].resname) + str(pdb_info[0].resnum)
    count_chains = 0
    count_res    = 0
    flag_boolhet = 0

    list_Chains = [] # list of chains to be combined into one chain

    for ATOM in pdb_info:
        if ATOM.chainid != curent_chain:
           print str(curent_chain) + " " + str(count_res),
           if flag_boolhet: 
               print " het",
           if (count_res < max_num_res):
               list_Chains.append(current_atom)
               print "likely a ligand"
           else: 
               print ""
           current_atom = ATOM
           curent_chain = ATOM.chainid
           count_res = 0
           flag_boolhet = 0;

        if str(ATOM.resname)+str(ATOM.resnum) != curent_res:
           curent_res = str(ATOM.resname)+str(ATOM.resnum)
           count_res = count_res+1;

        flag_boolhet = flag_boolhet or ATOM.boolhet ## if one atom in the chain is a het then this will be true

    print str(curent_chain) + " " + str(count_res),
    if flag_boolhet: 
        print "  het",
    if (count_res < max_num_res):
        list_Chains.append(ATOM)
        print "likely a ligand"
    else: 
        print ""

    print "done"
    file1.close()
    return list_Chains 


#################################################################################################################
#################################################################################################################
def ok_residue(resname):
    # read in solvent residue types from file.

    if (resname == 'HOH'):
        return False
    if (resname == ' NA'):
        return False

    return True
#################################################################################################################
#################################################################################################################
def write_mod_pdb(pdb_file,pdb_out,list):
    ## reads in pdb id how meny residues are in each chain
    file1 = open(pdb_file,'r')
    file2 = open(pdb_out,'w')
    lines  =  file1.readlines()
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                flag, chainresnum = chain_on_list(list,line[21],line[17:20])
                if (flag):
                      endofline = len(line)
                      file2.write("HETATM" + line[6:17] + "LIG" + line[20:23] + chainresnum + line[26:endofline])
                else:
                      file2.write(line)
 
    file1.close()
    file2.close()
#################################################################################################################
#################################################################################################################
def chain_on_list(list,chainid,resname):
    for ele in list:
        if (ele.chainid == chainid and ok_residue(resname)):
            #print ele.chainid + "==" + chainid
            return True, ele.resnum
    return False, 0

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a pdb file"
        print "and write to standard output the chain id followed by the number of residues in chain"
        print "Writes a new pdbfile with all the small chains combind into one residue per chain with resname LIG"
        print "python pdb_chains_residue_num_combine.py input.pdb output.pdb"
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    list = chain_info(pdb_file)
    if (len(list) > 0):
       write_mod_pdb(pdb_file,pdb_out,list)
    else:
       print "not modified"
    
    
#################################################################################################################
#################################################################################################################
main()
