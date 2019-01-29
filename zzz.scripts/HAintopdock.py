import sys, mol2_mod_2012_12

## Writen by Trent Balius in the Shoichet Group
## count numbers of heavy atoms in topdock ligands

def write_sph(filename,mol):
    outsph = open(filename,'w')
    print len(mol.atom_list)
    outsph.write("cluster     1   number of spheres in cluster    %d\n" % len(mol.atom_list))
    for i in range(len(mol.atom_list)): 
	outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d                                \n" % 
                     (i+1,round(mol.atom_list[i].X,3),
                          round(mol.atom_list[i].Y,3),
                          round(mol.atom_list[i].Z,3),0.7,i+1) )

    outsph.close()
    return

def main():
  if len(sys.argv) != 2: # if no input
     print "ERORR"
     retrun
  name_topdock = sys.argv[1]

  mols = mol2_mod_2012_12.read_TOPDOCK_PDB_file(name_topdock)

  for mol in mols:
     num  = mol2_mod_2012_12.Num_heavy_atoms(mol.atom_list)
     print str(num)
  
main()


