import sys
import pdb_lib
import copy

def renumber_residue_continuous(pdb_mol,val):
    count = int(pdb_mol[0].resnum) + int(val)
    old   = pdb_mol[0].resnum
    for i in range(len(pdb_mol)):
        ori = pdb_mol[i].resnum
        if (old != ori):
           count = count + 1
           old = ori
        pdb_mol[i].resnum = str(count)

def replace_chain_name(pdb_mol,new_name):
    for i in range(len(pdb_mol)):
        pdb_mol[i].chainid = new_name;

def append_chain(pdb_mol,chain):
    for i in range(len(pdb_mol)):
        temp = copy.copy(pdb_mol[i])
        chain.append(temp)
        #chain.append(pdb_mol[i])


def main():
   filename = sys.argv[1]
   intval   = int(sys.argv[2])
   fileprefix = sys.argv[3]
   
   pdbchains = pdb_lib.read_pdb(filename) 
   count = 1
   cat_chains =[]
   for pdbmol in pdbchains: 
       replace_chain_name(pdbmol,' ')
       append_chain(pdbmol,cat_chains)
       renumber_residue_continuous(pdbmol,intval) 
       pdb_lib.output_pdb(pdbmol,'%s_%i.pdb'%(fileprefix,count)) 
       count=count+1
   renumber_residue_continuous(cat_chains,intval) 
   pdb_lib.output_pdb(cat_chains,'%s.pdb'%(fileprefix)) 
main()
