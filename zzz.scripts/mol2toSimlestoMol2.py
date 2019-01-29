
## uses local version of python on sublime

import sys, pybel,  openbabel

## Writen by Trent Balius in the Shoichet Group
## note that open babel must be installed to run this script
## take as input a mol2file converts it to a  smiles and 
## then converts it back to a mol2.
## this script removes ligand conformation bias

def Mol2ToSimles(file):

   obConversion = openbabel.OBConversion()
   obConversion.SetInAndOutFormats("mol2", "smi")
   mol = openbabel.OBMol()
   obConversion.ReadFile(mol, file) 
   SmilesString = obConversion.WriteString(mol).split()[0]
   #print SmilesString
   #mol.DeleteHydrogens()
   #SmilesString = obConversion.WriteString(mol).split()[0]
   #print SmilesString
   #SmilesString = ''
   return SmilesString

def SimlesToMol2(string,file):
   obConversion = openbabel.OBConversion()
   obConversion.SetInAndOutFormats("smi", "mol2")

   mol = openbabel.OBMol()
   obConversion.ReadString(mol, string)

   mol.AddHydrogens()
   #mol.AddOption("gen3D",GENOPTIONS)
   # get the charges of the atoms
   # Reimplemented in OpenBabel::EEMCharges, OpenBabel::GasteigerCharges, OpenBabel::MMFF94Charges, and OpenBabel::NoCharges.
   #charge_model = openbabel.OBChargeModel.FindType("MMFF94")
   #openbabel.OBBuilder().Build(mol.OBMol)
   builder = openbabel.OBBuilder()
   builder.Build(mol)
   charge_model = openbabel.OBChargeModel.FindType("Gasteiger")
   charge_model.ComputeCharges(mol)
   partial_charges = charge_model.GetPartialCharges() 
   #print partial_charges

   print "charge = %f" % (sum(partial_charges))

   obConversion.WriteFile(mol, file)
 
   return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return

  inmol2file = sys.argv[1]
  outmol2file = sys.argv[2]

  SmilesString = Mol2ToSimles(inmol2file)
  SimlesToMol2(SmilesString,outmol2file) 

  print SmilesString
 
main()

