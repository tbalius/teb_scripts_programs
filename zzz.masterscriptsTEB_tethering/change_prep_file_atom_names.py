# TEB/ MF comments -- March2017
# This script renames CYS according to reduce protonation as required by tleap/ amber.
# this is when the atoms that you want to remove are at the end or atleast not at the begining ...

import sys, os

print "This script reads in a parm file produced by Antichamber.  It will remove the cys atoms.  for covalent MD"
print "Written by Trent E. Balius, 2020/05/23"

print "syntax: python script.py input output_prefix"

infile     = sys.argv[1]
out_prefix = sys.argv[2]

outfile  = out_prefix+"_mod.prep"

print("  input = %s\n output prefix = %s\n"%(infile,out_prefix))

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()

newline=''
#count = 0;
charge = 0.0
fileout = open(outfile,'w')
new_lines = []
for line in lines:
    name = line[6:11].strip()
    print name
    #if count == 10:
        #replacement = line[20:37] 
        #charge = float(line[63:-1])
        #count = count + 1
        #continue
    if name == "SG" or name == "CB" or name == "HB1" or name == "HB2" or name == "HB3": 
        #count = count + 1
        charge = charge + float(line[63:-1])
        continue
    new_lines.append(line)
      #print line[13:16], line[23:26], line[17:20]
for line in new_lines:
    name = line[6:11].strip()
    if name == "S1":  
        #line = line.strip()
        print("charge = %6.4f"%charge)
        newcharge = charge + float(line[63:-1])
        #newline = line[0:20]+replacement+line[37:63]+"%8.6f"%newcharge+'\n' 
        newline = line[0:63]+"%8.6f"%newcharge+'\n' 
        print(newline)
        fileout.write(newline)
        newline = ''
    else: 
        fileout.write(line)
    #count = count + 1
fileout.close()


