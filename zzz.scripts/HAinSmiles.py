
import sys, openbabel

## Writen by Trent Balius in the Shoichet Group
## retruns the number of Heavy atoms in Smiles string. 
## note that open babel must be installed to run this script
## take as input a file with smiles.

def numberofHeavyAtoms(SmilesString):

   obConversion = openbabel.OBConversion()
   obConversion.SetInAndOutFormats("smi", "mol2")
   ## mdl = 

   mol = openbabel.OBMol()
   obConversion.ReadString(mol, SmilesString)

   mol.DeleteHydrogens()
   nha = mol.NumAtoms()
   #print nha

   #mol.AddHydrogens()
   #print mol.NumAtoms()
   return nha
   #outMDL = obConversion.WriteString(mol)

def main():
  if len(sys.argv) != 2: # if no input
     print "ERORR"
     return

  smilesfile = sys.argv[1]
  file = open(smilesfile,'r')
  lines = file.readlines()
  file.close()

  for line in lines:
     splitline = line.split()
     if len(splitline) > 1:
        print "ERROR:len(smiles) > 1"
        exit()
     smiles = splitline[0]
     nha = numberofHeavyAtoms(smiles)
     #print "simles = " + str(smiles);
     print "numberofHeavyAtoms = " + str(nha);
 
main()

