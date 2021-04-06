

from rdkit import Chem
from rdkit.Chem import AllChem


def confgen(smi,num):

  # this includes addtional small ring torsion potentials
  params = AllChem.srETKDGv3()

  # this includes additional macrocycle ring torsion potentials and macrocycle-specific handles
  params = AllChem.ETKDGv3()

  # to use the two in conjunction, do:
  params = AllChem.ETKDGv3()
  params.useSmallRingTorsions = True

  sdf_output_file = "temp.sdf"
  writer = Chem.SDWriter(sdf_output_file)

  # a macrocycle attached to a small ring
  mol = Chem.MolFromSmiles(smi)
  mol = Chem.AddHs(mol)
  molc = AllChem.EmbedMultipleConfs(mol, numConfs = num , params = params)
  print(molc)
  for moln in molc: 
    print(moln)
    writer.write(mol,confId=moln)
  writer.close() 

smi2 = "C(OC(CCCCCCC(OCCSC(CCCCCC1)=O)=O)OCCSC1=O)N1CCOCC1"
num2 = 10
confgen(smi2,num2)

