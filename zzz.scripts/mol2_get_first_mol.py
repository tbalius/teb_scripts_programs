
#import mol2
import mol2_python3 as mol2
import sys

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_get_frist_mol.py input_file output_file")

infile = sys.argv[1]
outfile = sys.argv[2]
mol_list = mol2.read_Mol2_file(infile)
print (len(mol_list))
#mol = mol2.remove_hydrogens( mol_list[0] )
mol = mol_list[0]
mol2.write_mol2(mol,outfile)

