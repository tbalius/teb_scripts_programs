# TEB/ MF comments -- March2017
# This script renames CYS according to reduce protonation as required by tleap/ amber.

import sys, os

print "This script reads in a pdb file"
print "Written by Trent E. Balius, 2020/04/14"

print "syntax: python script.py input name number output_prefix"

infile     = sys.argv[1]
name       = sys.argv[2]
num        = int(sys.argv[3])
out_prefix = sys.argv[4]

outfile  = out_prefix+"_sph.pdb"
outfile_sph  = out_prefix+"_sph.sph"
outfile2 = out_prefix+"_SG_CB.pdb"

print("  input = %s\n  name = %s\n  num = %d\n  output prefix = %s\n"%(infile,name,num,out_prefix))

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()

sph1_line = ''
sph2_line = ''
sph3_line = ''


for line in lines:
    if line[0:4] == 'ATOM':
      #print line[13:16], line[23:26], line[17:20]
      if line[13:16] == 'SG ' and int(line[23:26])==num and line[17:20] == name:
        print "sph1:"+line
        if sph1_line !='':
           print "UhOh.  sph1 is already defined.  Continue ..."
           continue
        sph1_line = line 
      if line[13:16] == 'CB ' and int(line[23:26])==num and line[17:20] == name:
        print "sph2:"+line
        if sph2_line !='':
           print "UhOh.  sph2 is already defined.  Continue ..."
           continue
        sph2_line = line 
      if line[13:16] == 'CA ' and int(line[23:26])==num and line[17:20] == name:
        print "sph3:"+line
        if sph3_line !='':
           print "UhOh.  sph3 is already defined.  Continue ..."
           continue
        sph3_line = line 

fileout = open(outfile,'w')
fileout.write(sph1_line)
fileout.write(sph2_line)
fileout.write(sph3_line)
fileout.close()

cmd = "$DOCKBASE/proteins/pdbtosph/bin/pdbtosph %s %s"%(outfile,outfile_sph)
os.system(cmd)

fileout2 = open(outfile2,'w')
fileout2.write(sph1_line)
fileout2.write(sph2_line)
fileout2.close()

