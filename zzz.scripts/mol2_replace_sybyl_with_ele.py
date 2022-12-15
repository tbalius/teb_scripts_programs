
import mol2
import sys

# take a sybyl atom type and returns an element.
# does this by spliting on the dot (.) in the type
# and returning the chars before the dot.
def sybyl_to_ele(atom_type):
    atom_type=atom_type.replace(" ","")
    ele = atom_type.split('.')[0]
    print(ele)
    return ele


print "this file requiers the mol2 libary writen by trent balius and sudipto mukherjee"

print "syntex: mol2_replace_sybyl_to_ele.py input_file output_file"

infile = sys.argv[1]
outfile = sys.argv[2]
mols = mol2.read_Mol2_file(infile)
#print len(mol_list)
#mol = mol2.remove_hydrogens( mol_list[0] )
first = True
for mol in mols:

   for i in range(len(mol.atom_list)):
       atomtype = mol.atom_list[i].type 
       atomele = sybyl_to_ele(atomtype)
       mol.atom_list[i].type = atomele
   if first:
       mol2.write_mol2(mol,outfile)
       first=False
   else:
       mol2.append_mol2(mol,outfile)

