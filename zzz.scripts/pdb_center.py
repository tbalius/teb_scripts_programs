
#import mol2
import pdb_lib as pdb
import sys

print ("this file requiers the pdb libary writen by trent balius")

print ("syntex: pdb_center.py input_file output_file")

infile = sys.argv[1]
outfile = sys.argv[2]
mol_list = pdb.read_pdb(infile)
cmol = pdb.center( mol_list[0] )

print(cmol)
fh = open(outfile,'w')
fh.write("%f %f %f\n" % (cmol[0],cmol[1],cmol[2]))
print("%f %f %f\n" % (cmol[0],cmol[1],cmol[2]))
fh.close()
