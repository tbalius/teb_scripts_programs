#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2015

# TEB, MF comments -- March 2017

# This shell script will do the following:
# (1) aligns the flexible receptor onto the 10th (production) MD frame -- as before for ligand.
# Hence we can make a simlink using that ligand.

set mountdir = `pwd`
set workdir  = $mountdir/flex/01align_to_md
rm -rf $workdir
mkdir -p $workdir
cd $workdir

#ln -s ${mountdir}/MDrundir/prep/002md_align . 


set ref = "$mountdir/gist/006ref/ref.pdb" # snapshot from simulation
set rec = "/mnt/nfs/work/tbalius/Water_Project/structures_from_marcus/APO_rt_consensusloop_new2_tebmod_2.pdb" # rec with flexibility

set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

#write instruction file for chimera based alignment
cat << EOF > chimera.com
# template #0
open $ref 
# rec #1
open $rec

# move original to gist. it is harder to move the gist grids. 
mmaker #0 #1 
write format pdb  0 ref.pdb
write format pdb  1 rec_aligned.pdb
EOF
 
${chimerapath} --nogui chimera.com > & chimera.com.out

# we have already aligned the ligand previously. 
ln -s $mountdir/gist/007align_to_md/lig_aligned.pdb .

