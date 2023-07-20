
#import mol2
import mol2_python3 as mol2
import sys

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: multimol2_removeH.py input_file output_file")

infile = sys.argv[1]
outfile = sys.argv[2]

file = open(outfile,'w') # overwrite
file.close()

mol_list = mol2.read_Mol2_file_head(infile)
print (len(mol_list))

for i in range(len(mol_list)):
  print ("mol ", i)
  mol = mol2.remove_hydrogens( mol_list[i] )
  mol2.append_mol2(mol,outfile)



