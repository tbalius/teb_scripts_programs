# TEB/ MF comments -- March2017
# This script renames CYS according to reduce protonation as required by tleap/ amber.

import sys

print "This script requires a pdb protonated with reduce"
print "Written by Trent E. Balius, 2015/02/05"

print "syntax: python replace_cys_to_cyx.py input output"
print "get script from webpage via:"
print "curl docking.org/~tbalius/code/waterpaper2017/scripts/replace_cys_to_cyx.py > replace_cys_to_cyx.py"

infile = sys.argv[1]
outfile = sys.argv[2]

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()
fileout = open(outfile,'w')
fileout2 = open(outfile+".for.leap",'w')

# grep "HD1 HIS" rec.nowat.add_h.pdb
# grep "HE2 HIS" rec.nowat.add_h.pdb
#print lines


dic_CYS = {}
dic_RES = {}

# 1) loop over all residues, looks for cys and puts it in python dictionary 
# 2) calculates all cys-cys distances, 
#    if distance < sqrt(5), changes name to cyx and create bond record for tleap
# 3) write file with changed names

# find all cysteines
rescount = 1
for line in lines:
   #print line
    if line[0:4] == 'ATOM':
      #print line
      #print line[13:16], line[17:20]
      if line[13:16] == 'SG ' and line[17:20] == 'CYS':
        #print line
        #print line[31:39]
        #print line[39:46]
        #print line[46:54]
        x = float(line[31:39])
        y = float(line[39:46])
        z = float(line[46:54])
        print [x,y,z]
        dic_CYS[line[17:26]] = [x,y,z]
      if not (line[17:26] in dic_RES.keys()):
        print line[17:26], rescount
        dic_RES[line[17:26]] = rescount
        rescount = rescount + 1

keys = dic_CYS.keys()

dic_CYX = {}

# find cys that need name change by measuring distances
for i in range(0,len(keys)):
    key1 = keys[i]
    xyz1 = dic_CYS[key1]
    for j in range(i+1,len(keys)):
        key2 = keys[j]
        xyz2 = dic_CYS[key2]
        dist2 = (xyz1[0]-xyz2[0])**2 + (xyz1[1]-xyz2[1])**2 + (xyz1[2]-xyz2[2])**2
        #print key1, key2, dist2
        if dist2 < 5: 
           dic_CYX[key1] = 1
           dic_CYX[key2] = 1
           # bond REC.11.SG REC.344.SG
           print str(key1)+" "+str(key2)+" "+str(dist2)
           #print "bond REC.%s.SG REC.%s.SG"%(key1.split()[2],key2.split()[2])
           print "bond REC.%d.SG REC.%d.SG"%(dic_RES[key1],dic_RES[key2])
           #fileout2.write("bond REC.%s.SG REC.%s.SG\n"%(key1.split()[2],key2.split()[2]))
           fileout2.write("bond REC.%d.SG REC.%d.SG\n"%(dic_RES[key1],dic_RES[key2]))
fileout2.close()

# loop over file and replace cys with cyx.
for line in lines:
    N = len(line)
    if line[0:4] == 'ATOM':
       if (line[17:26] in dic_CYX.keys()):
          fileout.write(line[0:17]+'CYX'+line[20:N])
       else:
          fileout.write(line)

fileout.close()

