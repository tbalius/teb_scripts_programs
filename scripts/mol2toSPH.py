import sys, mol2

## Writen by Trent Balius in the Rizzo Group
## converts a mol2 to spheres. 

def write_sph(filename,mol):
    outsph = open(filename,'w')
    print len(mol.atom_list)
    outsph.write("DOCK spheres generated from ligand heavy atoms\n")
    outsph.write("cluster     1   number of spheres in cluster    %d\n" % len(mol.atom_list))
    for i in range(len(mol.atom_list)): 
	#outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d                                \n" % 
	outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d 0  0\n" % 
                     (i+1,round(mol.atom_list[i].X,3),
                          round(mol.atom_list[i].Y,3),
                          round(mol.atom_list[i].Z,3),0.7,i+1) )

    outsph.close()
    return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  namemol2 = sys.argv[1]
  namesph = sys.argv[2]
  mol  = mol2.remove_hydrogens(mol2.read_Mol2_file(namemol2)[0])
  write_sph(namesph,mol)
main()


