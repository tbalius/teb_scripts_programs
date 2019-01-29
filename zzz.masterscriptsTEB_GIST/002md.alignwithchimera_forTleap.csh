#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2015
# TEB, MF comments 2017

# This shell script will do the following:
# (1) align the ligand file onto hydrated apo reference
# (2) then use superposed ligand to id nearby binding site waters in apo structure
# (3) save nearby waters only to pdb

set mountdir = `pwd`

set workdir = $mountdir/MDrundir/prep/002md_align

rm -rf $workdir
mkdir -p $workdir
cd $workdir

# get the right files.      ### CHANGE THIS
set pdb1 = "4NVA"
set pdb2 = "4NVE"

set apo_ref = "../$pdb1/rec.pdb"
set rec_lig = "../$pdb2/rec.pdb"
set lig = "../$pdb2/xtal-lig.pdb" 
set wat = "../$pdb1/water.pdb" 

set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

#write instruction file for chimera based alignment
cat << EOF > chimera.com
# template #0
open $apo_ref 
# rec #1
open $rec_lig
# xtal-lig
open $lig
# waters
open $wat

# move original to gist. it is harder to move the gist grids. 
mmaker #0 #1 
matrixcopy #1 #2
sel #3:HOH & #2 z<8
del #3 & ~sel
write format pdb  0 apo_ref.pdb
write format pdb  1 rec_lig_aligned.pdb
write format pdb  2 lig_aligned.pdb
write format mol2  2 lig_aligned.mol2
write format pdb  3 nearby_waters_aligned.pdb
EOF

${chimerapath} --nogui chimera.com > & chimera.com.out



