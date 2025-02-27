# TEB/ MF comments -- March2017
# modified by TEB in 2020.
# This script changes an atom from one element to another and adjusts the name accordingly.

import sys, os

print "This script reads in a pdb file"
print "Written by Trent E. Balius, 2020/04/14"

print "syntax: python replace_atom_ele.py input name ele_ori ele_fin output_prefix"

infile     = sys.argv[1]
name       = sys.argv[2]
ele_ori    = sys.argv[3]
ele_fin    = sys.argv[4]
out_prefix = sys.argv[5]

outfile = out_prefix+".pdb"

print("  input = %s\n  name = %s\n  output prefix = %s\n"%(infile,name,out_prefix))

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()

name_line = ''

fileout = open(outfile,'w')

for line in lines:
    #if line[0:4] == 'ATOM':
    #if line[0:6] == 'HETATM':
    if line[0:6] == 'HETATM' or line[0:6] == 'ATOM  ':
      #print line[13:16], line[23:26], line[17:20]
      if line[13:16] == name:
        print "line:"+line
        name_line = line 
        line = line[0:13]+ name.replace(ele_ori,ele_fin)+line[16:76]+" %s"%(ele_fin)+'\n'
        print(name_line)
        print(line)
      fileout.write(line)

fileout.close()


