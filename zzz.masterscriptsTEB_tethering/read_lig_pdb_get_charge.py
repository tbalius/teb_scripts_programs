import sys
from rdkit import Chem

## Writen by Trent Balius in the FNLCR, Dec, 2020

file = sys.argv[1]
m = Chem.rdmolfiles.MolFromPDBFile(file)

smi = Chem.MolToSmiles(m)

m2 = Chem.rdmolfiles.MolFromSmiles(smi)
#netcharge2 = rdkit.Chem.rdmolops.GetFormalCharge(m)
#netcharge = rdkit.Chem.rdmolops.GetFormalCharge(m2)
netcharge = Chem.rdmolops.GetFormalCharge(m2)


print('smi=%s\n'%smi)
print('netcharge=%f\n'%netcharge)

