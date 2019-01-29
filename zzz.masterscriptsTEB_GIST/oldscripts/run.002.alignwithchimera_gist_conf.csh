#!/bin/csh 
## this script was written by trent balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2014

# This shell script will do the following:
#
# (1) align the original files from marcus to the Gist files.
# (2) align 4NVE of Gist file (lig:BENZIMIDAZOLE) then it will ligand for dock processing. 
#

set mountdir = `pwd`
#set mountdir = "/mnt/nfs/work/tbalius/Water_Project/run_DOCK3.7"
set filedir  = "/mnt/nfs/work/tbalius/Water_Project"


set workdir = $mountdir/workingdir/align_4NVE

rm -rf $workdir
mkdir -p $workdir
cd $workdir


#set file1 = "$filedir/structures_from_marcus/A_waterProj_mod.pdb"
set file1 = "$mountdir/workingdir/align/ref.pdb"
set file2 = "$mountdir/workingdir/4NVE/rec.pdb"
set file3 = "$mountdir/workingdir/4NVE/lig.pdb"


set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

cat << EOF > chimera.com
# Gist template #0
open $file1 
# 4NVE rec
open $file2 
# 4NVE lig
open $file3 

mmaker #0 #1 

matrixcopy #1 #2

write format pdb  0 template.pdb
write format pdb  1 aligned.rec.pdb
write format pdb  2 aligned.lig.pdb
EOF

${chimerapath} --nogui chimera.com > & chimera.com.out


