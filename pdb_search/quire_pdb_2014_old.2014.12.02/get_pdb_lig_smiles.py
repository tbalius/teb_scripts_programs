

import scrape_pdb_for_lig as spfl
import sys


ligname = sys.argv[1]


smiles = spfl.scrape_pdb_for_lig_smiles(ligname)

#print smiles

