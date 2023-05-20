
#import mol2
import mol2_python3 as mol2
import sys

print ("this file requiers the mol2 libary writen by trent balius and sudipto mukherjee")

print ("syntex: mol2.py input_file output_file")

infile = sys.argv[1]
outfile = sys.argv[2]
mol_list = mol2.read_Mol2_file(infile)
cmol = mol2.centre_of_mass( mol_list[0] )

print cmol
fh = open(outfile,'w')
fh.write("%f %f %f\n" % (cmol[0],cmol[1],cmol[2]))
fh.close()
