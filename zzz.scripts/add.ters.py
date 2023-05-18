# TEB/ MF comments -- March2017
# This script adds TER flags into pdb if residues are missing (e.g. backbone breaks) 

import sys

print "This script requires a pdb protonated with reduce"
print "Written by Trent E. Balius, 2015/02/05"

print "syntax: python 0001i.add.ters.py input output"

infile = sys.argv[1]
outfile = sys.argv[2]

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()
fileout = open(outfile,'w')


dic_C = {}
dic_N = {}
resid = []


flagCap = False

# loops over pdb_reduce-file and looks for backbone carbon and nitrogen
# puts it in a dictionary
for line in lines:
   #print line
      if line[13:16] == 'C  ' :
        #if flagCap:  # if we find a 'C' before an 'N' we don't need to skip distance calc 
        #     flagCap = False
        #x = float(line[31:39])
        #y = float(line[39:46])
        #z = float(line[46:54])
        x = float(line[30:38])
        y = float(line[39:45])
        z = float(line[46:53])
        print ([x,y,z])
        dic_C[line[17:26]] = [x,y,z]
        resid.append(line[17:26])
      if line[13:16] == 'N  ' :
        #x = float(line[31:39])
        #y = float(line[39:46])
        #z = float(line[46:54])
        print (line[30:39])
        print (line[30:38])
        x = float(line[30:38])
        y = float(line[39:45])
        z = float(line[46:53])
        print ([x,y,z])
        dic_N[line[17:26]] = [x,y,z]

keys = resid # dic_C.keys()

dic_bool = {}

# comments in loop

for i in range(1,len(keys)):
    key1 = keys[i-1] 		# just looks at neighboring residues to calc distances
    key2 = keys[i]
    if 'NME' in key1 or 'NME' in key2 or 'ACE' in key1 or 'ACE' in key2:
        print ("Cap found ... skip distance calc. ") 
        continue
    xyz1 = dic_C[key1]
    xyz2 = dic_N[key2]
    if line[0:4] == 'ATOM':
        dist2 = (xyz1[0]-xyz2[0])**2 + (xyz1[1]-xyz2[1])**2 + (xyz1[2]-xyz2[2])**2
        #print key1, key2, dist2
# checks whether pairs are above sqrt(5)A threshold and puts them into boolean dictionary 
        if (dist2>5.0):
           print (key1, key2, dist2 )
           dic_bool[key2] = True
        #else:
        #   dic_bool[key2] = False

keys = dic_bool.keys()
for line in lines:
        key = line[17:26]
        if key in keys:
           if dic_bool[key]:
              fileout.write("TER\n")
              dic_bool[key] = False
           if line[13:16] == 'H  ' : # do not write atom H that follows a TER 
              continue
        fileout.write(line)

fileout.close()

