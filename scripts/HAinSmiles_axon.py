
import sys,os

## Writen by Trent Balius in the Shoichet Group
## retruns the number of Heavy atoms in Smiles string. 
## note that open babel must be installed to run this script
## take as input a file with smiles.

def numberofHeavyAtoms(SmilesString):
    # write smiles to file
    fh = open("/tmp/tbalius/temp.smi",'w')
    fh.write(SmilesString+'\n')
    fh.close()

    os.popen("/raid3/software/openbabel/openbabel-2.2.1-32/bin/babel -ismi /tmp/tbalius/temp.smi -osdf /tmp/tbalius/temp.sdf -d")
    os.popen("/raid3/software/openbabel/openbabel-2.2.1-32/bin/babel -isdf /tmp/tbalius/temp.sdf -osmi /tmp/tbalius/temp2.smi -d")
    
    comand = "/raid3/software/jchem/jchem-5.5.1/bin/generatemd c /tmp/tbalius/temp2.smi -k Heavy"
    f = os.popen(comand)
    lines = f.read().split('\n')
    #for line in lines:
    #    print line
    #nha = 5
    nha = lines[2].split()[1]
    #f.close()
    #f1.close()
    #f2.close()
    return nha

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return

  smilesfile = sys.argv[1]
  outfile = sys.argv[2]
  file = open(smilesfile,'r')
  lines = file.readlines()
  file.close()

  file1 = open(outfile,'w')
  for line in lines:
     splitline = line.split()
     if len(splitline) > 1:
        print "ERROR:len(smiles) > 1"
        exit()
     smiles = splitline[0]
     #print "simles = " + str(smiles);
     nha = numberofHeavyAtoms(smiles)
     print "numberofHeavyAtoms = " + str(nha);
     file1.write("numberofHeavyAtoms = " + str(nha)+'\n')
  file1.close()
main()

