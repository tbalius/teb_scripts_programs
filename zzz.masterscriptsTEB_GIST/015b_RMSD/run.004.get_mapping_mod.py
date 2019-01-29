
import sys

def main():
  matrixfile     = sys.argv[1]
  pdbligfile     = sys.argv[2]
  zincnamefile   = sys.argv[3]

  file1 = open(matrixfile,'r')
  file2 = open(pdbligfile,'r')
  file3 = open(zincnamefile,'r')
  pllines = file2.readlines()
  znlines = file3.readlines()

  lines = file1.readlines()
  file1.close()
  file2.close()
  file3.close()

  for i,line in enumerate(lines):
      if "1.00" in line:
          entries = line.strip('\n').split(",") 
          for j,entry in enumerate(entries): 
              #print len(lines)
              #print len(entries)
              if float(entry) == 1.0:
                  #print i,j,entry
                  print pllines[i].strip('\n'),znlines[j].strip('\n')

main()
