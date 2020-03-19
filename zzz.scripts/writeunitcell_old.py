
# Written by Trent Balius, 2020/03/19
# I got this script from here: 
#  https://www.cgl.ucsf.edu/chimera/docs/ProgrammersGuide/faq.html

# Get the Molecule that has already been opened
import chimera
m = chimera.openModels.list()[0]

# Get the symmetry matrices
import PDBmatrices
tflist = PDBmatrices.crystal_symmetry_matrices(m.pdbHeaders)

# Get center of bounding box
import Molecule
center = Molecule.molecule_center(m)

# Get CRYST1 line from PDB headers
cryst1 = m.pdbHeaders['CRYST1'][0]

# Getting crystal parameters
from PDBmatrices import crystal
cp = crystal.pdb_cryst1_parameters(cryst1)
a,b,c,alpha,beta,gamma = cp[:6]

# Adjust matrices to produce close packing.
cpm = PDBmatrices.close_packing_matrices(tflist, center, center, a, b, c, alpha, beta, gamma)

# Apply transformations to copies of Molecule
mlist = []
from PDBmatrices import matrices
path = m.openedAs[0]			# Path to original PDB file
for tf in cpm:
    xf = matrices.chimera_xform(tf)	# Chimera style transform matrix
    m.openState.globalXform(xf)
    mlist.append(m)
    m = chimera.openModels.open(path)[0]	# Open another copy

# Write PDB file with transformed copies of molecule
import Midas
out_path = 'unitcell.pdb'
Midas.write(mlist, None, out_path)

