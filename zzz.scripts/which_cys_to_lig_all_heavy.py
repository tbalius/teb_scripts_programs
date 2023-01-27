# TEB/ MF comments -- March2017
# This script finds a renames CYS close to the ligand and write a connect line for amber's Tleap.
# This assumes that it is covalently attached.  

import sys

print "This script requires a pdb protonated with reduce"
print "Written by Trent E. Balius, 2015/02/05"

print "syntax: python which_cys_to_ligand.py input_rec input_lig output.txt"
print "get script from webpage via:"

infile = sys.argv[1]
infile_lig = sys.argv[2]
outfile = sys.argv[3]

filein  = open(infile,'r')
lines_R = filein.readlines()
filein.close()
filein  = open(infile_lig,'r')
lines_L = filein.readlines()
filein.close()
#fileout = open(outfile,'w')
fileout2 = open(outfile+".for.leap",'w')

# grep "HD1 HIS" rec.nowat.add_h.pdb
# grep "HE2 HIS" rec.nowat.add_h.pdb
#print lines

dic_CYS = {}
dic_RES = {}
dic_LIG = {}
dic_LATOM = {}

# 1) loop over all residues, looks for cys and puts it in python dictionary 
# 2) calculates all cys-cys distances, 
#    if distance < sqrt(5), changes name to cyx and create bond record for tleap
# 3) write file with changed names

# find all cysteines
rescount = 1
for line in lines_R:
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

for line in lines_L:
   #print line
#    if line[0:4] == 'ATOM':
      #print line
      #print line[13:16], line[17:20]
      #if line[77:79] == 'S ' and line[17:20] == 'LIG': # all Sulfur atoms 
      if line[77:79] != 'H ' and line[17:20] == 'LIG': # all heavy ligand atoms
        print "*"+line[77:79] +"* #### "+ line[17:20]
        print line[13:16]
        #print line
        #print line[31:39]
        #print line[39:46]
        #print line[46:54]
        x = float(line[31:39])
        y = float(line[39:46])
        z = float(line[46:54])
        print [x,y,z]
        dic_LIG[line[13:26]] = [x,y,z]
        dic_LATOM[line[13:26]] = line[13:16]

keys = dic_CYS.keys()
keys2 = dic_LIG.keys()
print "ligand keys =", keys2
#dic_CYX = {}

# find cys that need name change by measuring distances
for i in range(0,len(keys)):
    key1 = keys[i]
    xyz1 = dic_CYS[key1]
    for j in range(0,len(keys2)): # ligand sulfur or all heavy
        key2 = keys2[j]
        xyz2 = dic_LIG[key2]
        dist2 = (xyz1[0]-xyz2[0])**2 + (xyz1[1]-xyz2[1])**2 + (xyz1[2]-xyz2[2])**2
        print key1, key2, dist2
        if dist2 < 6.0: 
           #dic_CYX[key1] = 1
           #dic_CYX[key2] = 1
           # bond REC.11.SG REC.344.SG
           print str(key1)+" "+str(key2)+" "+str(dist2)
           #print "bond REC.%s.SG REC.%s.SG"%(key1.split()[2],key2.split()[2])
           print("bond COM.%d.SG COM.%d.%s\n"%(dic_RES[key1],rescount,dic_LATOM[key2]))
           #fileout2.write("bond REC.%s.SG REC.%s.SG\n"%(key1.split()[2],key2.split()[2]))
           fileout2.write("bond COM.%d.SG COM.%d.%s\n"%(dic_RES[key1],rescount,dic_LATOM[key2]))
fileout2.close()


