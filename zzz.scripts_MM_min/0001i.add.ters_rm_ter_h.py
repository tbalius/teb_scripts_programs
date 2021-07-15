
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

# grep "HD1 HIS" rec.nowat.add_h.pdb
# grep "HE2 HIS" rec.nowat.add_h.pdb
#print lines


dic_C = {}
dic_N = {}
resid = []

# loop over file and look for HIS that Have HID or HIE hydrogen.  
# put in a dictionaty
for line in lines:
   #print line
    if line[0:4] == 'ATOM':
      if line[13:16] == 'C  ' :
        x = float(line[31:39])
        y = float(line[39:46])
        z = float(line[46:54])
        print [x,y,z]
        dic_C[line[17:26]] = [x,y,z]
        resid.append(line[17:26])
      if line[13:16] == 'N  ' :
        x = float(line[31:39])
        y = float(line[39:46])
        z = float(line[46:54])
        print [x,y,z]
        dic_N[line[17:26]] = [x,y,z]

keys = resid # dic_C.keys()

dic_bool = {}

for i in range(1,len(keys)):
    key1 = keys[i-1]
    key2 = keys[i]
    xyz1 = dic_C[key1]
    xyz2 = dic_N[key2]
    if line[0:4] == 'ATOM':
        dist2 = (xyz1[0]-xyz2[0])**2 + (xyz1[1]-xyz2[1])**2 + (xyz1[2]-xyz2[2])**2
        #print key1, key2, dist2 
        if (dist2>5.0):
           print key1, key2, dist2 
           dic_bool[key1] = True
        #else:
        #   dic_bool[key2] = False


## we needed to delete hydrogens from terminal residues.
## to  do this we remember the residue befor the break.
## we remove the hydrogen
## we then write the ter
## then we remove the second hydrogen
flag_end   = False # this is true when we are at the end of the residue before the ter
last       = ''    # this is to remember what the last residue was.
flag_ter_h = False # this is to note that we are in a terminal residue (before or after).
count      = 0
keys = dic_bool.keys()
for line in lines:
        key = line[17:26]
        if (last != key and flag_ter_h): 
            #print "I AM HERE"
            flag_end = True
            flag_ter_h = False
        if (flag_end):
           fileout.write("TER\n")
           flag_end = False
        if key in keys:
           if dic_bool[key]:
              print key
              flag_ter_h = True
              dic_bool[key] = False
        last = key
        #print last
        if (flag_ter_h):
            if (line[13:16] == 'H  '):
                #print "I AM HERE"
                print line 
                count = count +1
                if (count == 2): # here we count howmeny h we incountered, but this might brake if for some reason the residue after the ter has no h.  
                   flag_ter_h = False
                   count = 0
                continue
        fileout.write(line)

fileout.close()

