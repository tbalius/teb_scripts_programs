#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2015

# TEB, MF comments -- March 2017
#
# This shell script will do the following:
# (1) aligns the ligand file and nearby waters onto MD frame of reference created in previous script [006gist.cpptraj_mk_ref.csh]
# (2) then writes out the aligned ligand and waters which will be used to calculate center of mass which centers the GIST box.
#  Aligned structures are then also useful for visualizing gist.

set mountdir = `pwd`
set workdir  = $mountdir/gist/007align_to_md
rm -rf $workdir
mkdir -p $workdir
cd $workdir

ln -s ${mountdir}/MDrundir/prep/002md_align . 


set ref = "../006ref/ref.pdb"                     # snapshot from simulation
set rec = "002md_align/apo_ref.pdb"               # the receptor given to tleap
set lig = "002md_align/lig_aligned.pdb"           # ligand in the same fram as rec 
set wat = "002md_align/nearby_waters_aligned.pdb" # waters aligned 

set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

#write instruction file for chimera based alignment
cat << EOF > chimera.com
# template #0
open $ref 
# rec #1
open $rec
# xtal-lig
open $lig
# waters
open $wat

# move original to gist. it is harder to move the gist grids. 
mmaker #0 #1 
matrixcopy #1 #2
matrixcopy #1 #3
write format pdb  0 ref.pdb
write format pdb  1 rec_aligned.pdb
write format pdb  2 lig_aligned.pdb
write format mol2 2 lig_aligned.mol2
write format pdb  3 waters_aligned.pdb
EOF
 
${chimerapath} --nogui chimera.com > & chimera.com.out


