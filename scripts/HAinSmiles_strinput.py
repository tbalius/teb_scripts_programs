
import sys, openbabel

## Writen by Trent Balius in the Shoichet Group
## retruns the number of Heavy atoms in Smiles string. 
## note that open babel must be installed to run this script


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
  smiles = sys.argv[1]
  nha = numberofHeavyAtoms(smiles)
  print "simles = " + str(smiles);
  print "numberofHeavyAtoms = " + str(nha);
 
main()


