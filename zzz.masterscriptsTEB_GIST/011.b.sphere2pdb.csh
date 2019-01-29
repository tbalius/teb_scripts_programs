#!/bin/csh -f

# To run:
# csh 011.b.sphere2pdb.csh docking/1prep/dockfiles/matching_spheres.sph > docking/1prep/dockfiles/matching_spheres.pdb
#
# alternatively can also use:
# $DOCKBASE/proteins/showsphere/doshowsph.csh file.sph 1 file.pdb

awk 'tcsh!~/e/{ \
printf("ATOM  %5d  C   SPH%5d%12.3f%8.3f%8.3f%6.2f%6.2f\nTER\n", $1, $1, $2, $3, $4, 1, $5)}' $1

# Visualize matching spheres and box in receptor context.
# /nfs/soft/chimera/current/bin/chimera docking/1prep/rec.pdb docking/1prep/dockfiles/matching_spheres.pdb docking/1prep/working/box
