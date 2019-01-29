
import sys

print "input file: "+sys.argv[1]
print "output file: "+sys.argv[2]

file1 = open(sys.argv[1],'r')
file2 = open(sys.argv[2],'w')

for line in file1:

    if line[16] != ' ': 
       print line
    newline = line[0:16]+' '+line[17:]
    file2.write(newline)

file1.close()
file2.close()


