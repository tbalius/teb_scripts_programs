
import sys

print "This script requires a pdb protonated with reduce"
print "Written by Trent E. Balius, 2015/02/05"

print "syntax: python replace_his_with_hie_hid_hip.py input output"

infile = sys.argv[1]
outfile = sys.argv[2]

filein  = open(infile,'r')
lines = filein.readlines()
filein.close()
fileout = open(outfile,'w')

# grep "HD1 HIS" rec.nowat.add_h.pdb
# grep "HE2 HIS" rec.nowat.add_h.pdb
#print lines


dic_HID = {}
dic_HIE = {}

# loop over file and look for HIS that Have HID or HIE hydrogen.  
# put in a dictionaty
for line in lines:
   #print line
    if line[0:4] == 'ATOM':
      #print line
      #print line[13:17], line[17:21]
      if line[13:16] == 'HD1' and line[17:20] == 'HIS':
        #print line
        #print line[17:26]
        dic_HID[line[17:26]] = 1
      if line[13:16] == 'HE2' and line[17:20] == 'HIS':
        #print line
        #print line[17:26]
        dic_HIE[line[17:26]] = 1 
      #exit()

# loop over file and replace HIS with HIE(epsilon hydrogen), HID(delta hydrogen), or HIP (both).
for line in lines:
    N = len(line)
    if line[0:4] == 'ATOM':
       if (line[17:26] in dic_HID) and (line[17:26] in dic_HIE):
          #print "HIP"
          fileout.write(line[0:17]+'HIP'+line[20:N])
       elif line[17:26] in dic_HID:
          #print "HID"
          fileout.write(line[0:17]+'HID'+line[20:N])
       elif line[17:26] in dic_HIE:
          #print "HIE"
          fileout.write(line[0:17]+'HIE'+line[20:N])
       else:
          fileout.write(line)

fileout.close()

