

import rdkit
 from rdkit import Chem
 smi = 'CCCCCC'
 m = Chem.MolFromSmiles(smi)
 rdkit.Chem.rdmolops.GetFormalCharge(m)

