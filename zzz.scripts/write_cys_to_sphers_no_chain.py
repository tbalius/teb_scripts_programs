# TEB/ MF comments -- March2017
# This script renames CYS according to reduce protonation as required by tleap/ amber.

import sys

print "Written by Trent E. Balius, mod 2022/08/02"

print "syntax: python write_cys_to_sph.py input resname resnum output"

infile = sys.argv[1]
resname = sys.argv[2]
resnum = sys.argv[3]
outfile = sys.argv[4]

print ('resname=\'%s\',resnum=\'%s\'\n'%( resname, resnum  ))

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()

fileout = open(outfile,'w')

# grep "HD1 HIS" rec.nowat.add_h.pdb
# grep "HE2 HIS" rec.nowat.add_h.pdb
#print lines


for line in lines:
   #print line
    if line[0:4] == 'ATOM':
      #print line
      #print line[13:16], line[17:20]
      fatomname = line[13:16]
      fresname  = line[17:20]
      fresnum  = line[23:26]
      if ( resname == fresname and resnum == fresnum ):
         print ('*%s*,*%s*,*%s*\n'%( fatomname, fresname, fresnum  ))
         if fatomname == "CA " or fatomname == "CB " or fatomname == "SG ":
            #fileout.write(line[0:17]+'ALA'+line[20:-1]+'\n')
            fileout.write(line[0:-1]+'\n')

fileout.close()
