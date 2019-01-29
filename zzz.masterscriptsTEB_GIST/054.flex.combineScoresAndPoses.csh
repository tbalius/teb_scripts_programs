#!/bin/csh

# This script combines the results from the ligand-decoy run 0003 (all chunks) into a combine file containing dock scores from OUTDOCK files
# Three files are produced (one for lig, decoy and both) 
# and: a file which has top poses as specified (e.g. top 1000 molecules with 2 poses each); two files (for lig and for decoys)

# TEB/ MF -- March 2017

# to remove dir
# rm -fr pdbs/3O1D/ligands-decoys/ligands/allChunksCombined/ pdbs/3O1D/ligands-decoys/decoys/allChunksCombined/ pdbs/3O1D/ligands-decoys/dockedLigDecoyCombined/

setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK
source /nfs/soft/python/envs/complete/latest/env.csh


set filedir = `pwd`
#set mountdir = $filedir/flex/3runEnrich/  # CHANGE THIS
set mountdir = $filedir/flex_multpose/3runEnrich/  # CHANGE THIS
set d37 =  $DOCKBASE/analysis/

cd $mountdir

#set list = "4NVA_gist 4NVA_nogist 4NVA_gist_m1.0"
set list = "4NVA_gist 4NVA_nogist"
#set list = "4NVA_gist"
#set list = "4NVA_nogist"
#set list = `cat filename`
#set list = `cat $1`

foreach pdbname ( $list )
  
foreach db_type ( "ligands" "decoys" )

set workdir = ${mountdir}/${pdbname}/${db_type}/allChunksCombined

echo $pdbname


mkdir -p ${workdir}
cd ${workdir}



# creates a file called dirlist that contains the full path of all directories with docked runs (chunks)
ls -ld ${mountdir}/${pdbname}/${db_type}/* | awk '/chunk/{print $9}' > dirlist 

# for debuging
#echo "print $db_type dirlist:"
#cat dirlist

# script extracts scores from all docking runs specified in dirlist
$d37/extract_all.py 
# script gets poses for top scoring molecules and produces poses.mol2 (default name)
$d37/getposes.py -d ${mountdir}/${pdbname}/${db_type}

end # db_type

## combine decoyes and actives
set workdir =  ${mountdir}/${pdbname}/dockedLigDecoyCombined

rm -rf ${workdir}
mkdir -p ${workdir}
cd ${workdir}
 
cat ${mountdir}/${pdbname}/ligands/allChunksCombined/dirlist ${mountdir}/${pdbname}/decoys/allChunksCombined/dirlist > dirlist

# for debuging
#echo "print ALL dirlist"
#cat dirlist

$d37/extract_all.py 
#$d37/getposes.py -d ${mountdir}/${pdbname} 	# doesn't work yet; not really needed
#getposes.py -z -l 1000 -x 2 -f extract_all.sort.uniq.txt -o ligands.1000.mol2 -d /mnt/nfs/work/users/fischer/VDR/27Jan2014_learningDOCKrgc/Enrichment/1DB1/DOCKING/ligands

end # pdbname


