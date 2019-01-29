#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013


# open template
# open system, open  2 sets so that we can
# easaly cacluate the transformation matrix.
# Apply transformation matix of one model to anthothr
# matrixcopy #0 #4 moving #1,2,3 
# The latter moves models #1-3 as if rigidly 
# transformed along with #4 if the matrix of #0 
# were applied to #4.
#mmaker #0 #1 ss false iter 2.0

set chimerapath = ""

cat << EOF > chimera.com

open template.rec.min.mol2
open ${system}.rec.min.mol2
open ${system}.lig.min.mol2
open ${system}.lig.ori.mol2
open center.pdb

##write format pdb  4 ${system}.center.pdb

mmaker #0 #1 

matrixcopy #1 #2
matrixcopy #1 #3
matrixcopy #1 #4

write format mol2 1 ${system}.rec.min.fit.mol2

# remove H
del #1@H,H?,H??,H???
# keel only atom within 20 angstroms of ligand
sel #1 & #4z>20
del sel

write format pdb  4 ${system}.center.fit.pdb
write format pdb  1 ${system}.rec.min.fit.noh.pdb

write format mol2 2 ${system}.lig.min.fit.mol2
write format mol2 3 ${system}.lig.ori.fit.mol2
EOF

#/sbhome0/sudipto/RCR/projects_BNL/chimera/bin/chimera --nogui chimera.com > & chimera.com.out
${chimerapath} --nogui chimera.com > & chimera.com.out

