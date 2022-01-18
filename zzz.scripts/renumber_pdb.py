import sys
import pdb_lib

def main():
   filename = sys.argv[1]
   intval   = int(sys.argv[2])
   fileprefix = sys.argv[3]
   
   pdbchains = pdb_lib.read_pdb(filename) 
   count = 1
   for pdbmol in pdbchains: 
       pdb_lib.renumber_residue(pdbmol,intval) 
       pdb_lib.output_pdb(pdbmol,'%s_%i.pdb'%(fileprefix,count)) 
       count=count+1
main()
