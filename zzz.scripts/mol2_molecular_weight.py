
import mol2_python3 as mol2
import sys

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2_removeH.py input_file output_file")

infile = sys.argv[1]
#outfile = sys.argv[2]
mol_list = mol2.read_Mol2_file_head(infile)

avg = 0 
mw_list = []

for mol in mol_list:
    mw = mol2.molecular_weight( mol )
    avg = avg + mw
    mw_list.append(mw)

avg = avg / float(len(mw_list))

print (avg)

