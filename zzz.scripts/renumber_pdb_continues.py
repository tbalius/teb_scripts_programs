import sys
import pdb_lib

def renumber_residue_continuous(pdb_mol,val):
    count = int(pdb_mol[0].resnum) + int(val)
    old   = pdb_mol[0].resnum
    for i in range(len(pdb_mol)):
        ori = pdb_mol[i].resnum
        if (old != ori):
           count = count + 1
           old = ori
        pdb_mol[i].resnum = str(count)


def main():
   filename = sys.argv[1]
   intval   = int(sys.argv[2])
   fileprefix = sys.argv[3]
   
   pdbchains = pdb_lib.read_pdb(filename) 
   count = 1
   for pdbmol in pdbchains: 
       renumber_residue_continuous(pdbmol,intval) 
       pdb_lib.output_pdb(pdbmol,'%s_%i.pdb'%(fileprefix,count)) 
       count=count+1
main()
