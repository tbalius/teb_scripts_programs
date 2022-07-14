import sys


# HETATM   14  N3B GNP D 201     -28.273 -11.284   5.894  1.00 11.46      LIG  N

if (len(sys.argv) != 3): 
   exit()

filenamer = sys.argv[1]
filenamew = sys.argv[2]

print('read %s'%filenamer)
print('write %s'%filenamew)

fhr = open(filenamer,'r')
fhw = open(filenamew,'w')

for line in fhr: 
    #if "N3B" in line: 
    if "C3B" in line: 
        print line
        line = line[:13]+"O3B"+line[16:77] + "O  \n"
    fhw.write(line)
fhr.close()
fhw.close()
