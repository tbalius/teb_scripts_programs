import sys
import pdb_lib

def replace_chain_name(pdb_mol,new_name):
    for i in range(len(pdb_mol)):
        pdb_mol[i].chainid = new_name;

def append_chain(pdb_mol,chain):
    for i in range(len(pdb_mol)):
        chain.append(pdb_mol[i])

def main():
   filename = sys.argv[1]
   fileprefix = sys.argv[2]
   
   pdbchains = pdb_lib.read_pdb(filename) 
   count = 1
   cat_chains = []
   for pdbmol in pdbchains: 
       replace_chain_name(pdbmol,' ')
       append_chain(pdbmol,cat_chains)
   pdb_lib.output_pdb(cat_chains,'%s.pdb'%(fileprefix)) 
main()
