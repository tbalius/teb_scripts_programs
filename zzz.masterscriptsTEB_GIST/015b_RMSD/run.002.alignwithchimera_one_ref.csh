#!/bin/csh 
## this script was written by Trent Balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2014

# This shell script will do the following:
#
# (1) align the each pdb the Gist frame.
#

# here this script is used to in preperatoion for calculating RMSD 


setenv AMBERHOME /nfs/soft/amber/amber14
set chimerapath = "/nfs/soft/chimera/current/bin/chimera"

set mountdir = `pwd`

#set list = `cat pdblist `
set list = `cat pdblist `

cd $mountdir/workingdir


cp $mountdir/../gist/006ref/ref.pdb .  


foreach pdbcode ($list)  # loop over xtal rmsd referemces
echo $pdbcode

set workdir = $mountdir/workingdir/align_${pdbcode}

if (-e $workdir) then 
   echo "$workdir exists"
   continue
endif 

mkdir -p $workdir
cd $workdir



#set file1 = "$filedir/run_amber_with_10waters/ref.pdb"
set file1 = "$mountdir/workingdir/ref.pdb"
set file2 = "$mountdir/workingdir/$pdbcode/rec.pdb"
set file3 = "$mountdir/workingdir/$pdbcode/lig.pdb"

if ! ( -e $file2) then
    echo "Ooh. there is no rec.pdb for $pdbcode ... continue to the next pdb"  
    continue
endif

if ! ( -e $file3) then
    echo "Ooh. there is no ligand for $pdbcode ... continue to the next pdb"  
    continue
endif


cat << EOF > chimera.com
# Gist template #0
open $file1 
# rec
open $file2 
# lig
open $file3 

# move original to gist. it is harder to move the gist grids. 
mmaker #0 #1 
matrixcopy #1 #2

write format pdb  1 aligned.rec.pdb
write format pdb  2 aligned.lig.pdb
write format mol2 2 aligned.lig.mol2
EOF

${chimerapath} --nogui chimera.com > & chimera.com.out

end # conf
#end # pdbcode
