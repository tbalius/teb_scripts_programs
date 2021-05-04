# TEB/ MF comments -- March2017
# This script renames CYS according to reduce protonation as required by tleap/ amber.

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
count = 0;
fileout = open(outfile,'w')
for line in lines:
    if count == 10:
        replacement = line[20:37] 
        charge = float(line[63:-1])
        #count = count + 1
        #continue
    elif count > 10 and count < 15: 
        count = count + 1
        charge = charge + float(line[63:-1])
        continue
      #print line[13:16], line[23:26], line[17:20]
    elif count == 15:  
        #line = line.strip()
        print("charge = %6.4f"%charge)
        newcharge = charge + float(line[63:-1])
        newline = line[0:20]+replacement+line[37:63]+"%8.6f"%newcharge+'\n' 
        print(newline)
        fileout.write(newline)
        newline = ''
    else: 
        fileout.write(line)
    count = count + 1
fileout.close()


