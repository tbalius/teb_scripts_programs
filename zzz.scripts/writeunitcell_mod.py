
# Written by Trent Balius, 2020/03/19, I took/modified most of the code from two locations 
# I got this script from here: 
# https://www.cgl.ucsf.edu/chimera/docs/ProgrammersGuide/faq.html
# Barrowed and modified code from here: Chimera/chimera-1.13.1/share/UnitCell/__init__.py


print ("\n example, how to run: \n\n ~/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script ~/zzz.github/teb_scripts_programs/writeunitcell_mod.py 6GJ8.pdb\n\n")

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
#from PDBmatrices import matrices
#path = m.openedAs[0]			# Path to original PDB file
#for tf in cpm:
#    xf = matrices.chimera_xform(tf)	# Chimera style transform matrix
#    m.openState.globalXform(xf)
#    mlist.append(m)
#    m = chimera.openModels.open(path)[0]	# Open another copy


# Adjust transforms so centers of models are in unit cell box
import Crystal
from Molecule import unit_cell_parameters, molecule_center
molecule = m
cp = unit_cell_parameters(molecule)
uc = cp[:6] if cp else None

gorigin = (0,0,0)

mc = molecule_center(molecule)
tflist = Crystal.pack_unit_cell(uc, gorigin, mc, tflist)

# Make multiple unit cells
#nc = self.number_of_cells()
nc = (3,3,3)
#if nc != (1,1,1) and uc:
# Compute origin.
oc_val = (1,1,1)        
oc = tuple((((o+n-1)%n)-(n-1)) for o,n in zip(oc_val, nc))
tflist = Crystal.unit_cell_translations(uc, oc, nc, tflist)

from Molecule import copy_molecule, transform_atom_positions
from Matrix import is_identity_matrix
for i,tf in enumerate(tflist):
  if is_identity_matrix(tf):
    continue
  name = m.name + (' #%d' % (i+1))
  c = copy_molecule(m)
  c.name = name
  c.unit_cell_copy = m
  transform_atom_positions(c.atoms, tf)
  chimera.openModels.add([c])
 # else:
 #  transform_atom_positions(c.atoms, tf, m.atoms)
  c.openState.xform = m.openState.xform
  mlist.append(c)



# Write PDB file with transformed copies of molecule
import Midas
out_path = 'unitcell.pdb'
Midas.write(mlist, None, out_path)

