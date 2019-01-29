#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013
## modified by Trent Balius and Marcus Fischer 2014. 
## align modified spheres: to move spheres that were successful for one pdb into a different frame of reference for another pdb. 

set mountdir = `pwd`

set workdir = $mountdir/aligned_sph
mkdir $workdir
cd $workdir

### START CHANGE ME #####
set fixed_rec_pdb = "/mnt/nfs/work/fischer/VDR/mimetic_4g2i/4G2I/working/rec.pdb" # protein that is static
set move_rec_pdb = "/mnt/nfs/work/fischer/VDR/tartedHis/working_tart1/rec.pdb" # protein that moves
set move_sph_file = "/nfs/home/tbalius/work/VDR/make_spheres_for_1db1_right_side/combined.sph" # move sph also. (along for the ride) 
### STOP CHANGE ME #####

ln -s $fixed_rec_pdb fixed_rec.pdb
ln -s $move_rec_pdb move_rec.pdb
ln -s $move_sph_file matching_spheres.sph.old

sph2pdb matching_spheres.sph.old > move_sph.pdb

set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

cat << EOF > chimera.align.move_sph.com

open fixed_rec.pdb
open move_rec.pdb
#open move_lig.pdb ## 
open move_sph.pdb

# call match maker to align the receptors
mmaker #0 #1 
# apply the same transfermation to the ligand or spheres
matrixcopy #1 #2

write format pdb 1 aligned_rec.pdb
#write format pdb 2 aligned_lig.pdb
write format pdb 2 aligned_sph.pdb
EOF

#/sbhome0/sudipto/RCR/projects_BNL/chimera/bin/chimera --nogui chimera.com > & chimera.com.out
${chimerapath} --nogui chimera.align.move_sph.com > & chimera.align.move_sph.com.out

sed -i 's/HETATM/ATOM  /g' aligned_sph.pdb 
pdbtosph aligned_sph.pdb matching_spheres.sph


