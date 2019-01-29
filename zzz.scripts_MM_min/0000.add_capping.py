
import sys

print "This script requires a complete pdb with only protein"
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
dic_V = {}
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
#        print [x,y,z]
        dic_C[line[17:26]] = [x,y,z]
        resid.append(line[17:26])
        dic_V[line[17:26]] = [ (dic_N[line[17:26]][0] - dic_C[line[17:26]][0]), (dic_N[line[17:26]][1] - dic_C[line[17:26]][1]), (dic_N[line[17:26]][2] - dic_C[line[17:26]][2])]
#        print "N", dic_N[line[17:26]]
#        print "C", dic_C[line[17:26]]
#        print "V", dic_V[line[17:26]]
      if line[13:16] == 'N  ' :
        x = float(line[31:39])
        y = float(line[39:46])
        z = float(line[46:54])
#        print [x,y,z]
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
           dic_bool[key2] = True
        #else:
        #   dic_bool[key2] = False


flag_end   = False # this is true when we are at the end of the residue before the ter
last       = ''    # this is to remember what the last residue was.
keys = dic_bool.keys()

flag     = False

book_ACE = True

for j in range(1,len(lines)):
        line = lines[j]
        line2 = lines[j-1]
        key = line[17:26]
        key2 = line2[17:26]
        if key in keys:
           if dic_bool[key]:
              flag = True
              dic_bool[key] = False
        if (last != key and flag): 
            #print "I AM HERE"
            flag_end = True
        if (flag_end):
           print "cap NME"
           fileout.write(line2[0:13])
           fileout.write("C   NME")
           fileout.write(line2[20:31])

           #for i in range(0,3):
           #   val = dic_N[line[17:26]][i]+dic_V[line[17:26]][i]
           #   fileout.write(' %6.3f'%val)
           val = dic_N[key2][0]+dic_V[key2][0]
           fileout.write(' %6.3f'%val)
           val = dic_N[key2][1]+dic_V[key2][1]
           fileout.write(' %6.3f'%val)
           val = dic_N[key2][2]+dic_V[key2][2]
           fileout.write(' %7.3f'%val)
           fileout.write(line2[54:len(line2)-2])
           fileout.write("C\n")
           fileout.write("TER\n")
           #fileout.write("TER\n")
           book_ACE = True
           flag_end = False
           flag     = False
        if (book_ACE):
           #print "cap ACE"
           #fileout.write("ACE")
           #for i in range(0,3):
           #   val = dic_C[line[17:26]][i]-dic_V[line[17:26]][i]
           #   #fileout.write(val)
           #   fileout.write(' %f '%val)
           print "cap ACE"
           fileout.write(line[0:13])
           fileout.write("C   ACE")
           fileout.write(line[20:31])
           val = dic_C[key][0]-dic_V[key][0]
           fileout.write(' %6.3f'%val)
           val = dic_C[key][1]-dic_V[key][1]
           fileout.write(' %6.3f'%val)
           val = dic_C[key][2]-dic_V[key][2]
           fileout.write(' %7.3f'%val)
           fileout.write(line[54:len(line)-2])
           fileout.write("C\n")
           #fileout.write("TER\n")

           book_ACE = False
           #fileout.write("\n")
        last = key
        #print last
        fileout.write(line)
print "cap NME"
fileout.write(line[0:13])
fileout.write("C   NME")
fileout.write(line[20:31])

#for i in range(0,3):
#   val = dic_N[line[17:26]][i]+dic_V[line[17:26]][i]
#   fileout.write(' %6.3f'%val)
val = dic_N[key][0]+dic_V[key][0]
fileout.write(' %6.3f'%val)
val = dic_N[key][1]+dic_V[key][1]
fileout.write(' %6.3f'%val)
val = dic_N[key][2]+dic_V[key][2]
fileout.write(' %7.3f'%val)
fileout.write(line[54:len(line)-2])
fileout.write("C\n")
fileout.write("TER\n")

fileout.close()

