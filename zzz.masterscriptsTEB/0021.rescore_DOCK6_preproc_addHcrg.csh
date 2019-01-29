#!/bin/csh
## Writen by Trent Balius; edited by TEB and Marcus Fischer 
## in the Shoichet Group, 2013
# processing in new workdir that is generated here to add hydrogens, charges and writes out mol2 for receptor (amber charges) and ligand (am1bcc charges)
# takes <1min

set chimerapath = "/nfs/soft/chimera/current/bin/chimera"	#change potentially 
set MFpath = "/mnt/nfs/work/fischer/VDR/masterscriptsTEB"

set  workdir = `pwd`"/DOCK6_pre-processing"

rm -fr   $workdir
mkdir -p $workdir 
cd       $workdir 

cp  ../rec.pdb ../xtal-lig.pdb .

#/sbhome0/sudipto/RCR/projects_BNL/chimera/bin/chimera --nogui chimera.com > & chimera.com.out
#${chimerapath} --nogui chimera.com > & chimera.com.out
${chimerapath} --nogui --script "$MFpath/0021_chimera_dock6prep.py rec.pdb rec_processed" 	#set chimera_dockprep.py link 
${chimerapath} --nogui --script "$MFpath/0021_chimera_dock6prep.py xtal-lig.pdb xtal-lig_processed"

