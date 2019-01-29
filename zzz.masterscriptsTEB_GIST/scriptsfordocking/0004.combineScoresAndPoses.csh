#!/bin/csh

# This script combines the results from the ligand-decoy run 0003 (all chunks) into a combine file containing dock scores from OUTDOCK files
# Three files are produced (one for lig, decoy and both) 
# and: a file which has top poses as specified (e.g. top 1000 molecules with 2 poses each); two files (for lig and for decoys)


# to remove dir
# rm -fr pdbs/3O1D/ligands-decoys/ligands/allChunksCombined/ pdbs/3O1D/ligands-decoys/decoys/allChunksCombined/ pdbs/3O1D/ligands-decoys/dockedLigDecoyCombined/

set filedir = "/mnt/nfs/work/users/fischer/VDR/gemini_3O1D"
set mountdir = "/mnt/nfs/work/users/fischer/VDR/gemini_3O1D"
set d37 =  $DOCK_BASE/src/dock37tools

cd $mountdir

set list = "3O1D"
#set list = `cat filename`
#set list = `cat $1`

foreach pdbname ( $list )
  
foreach db_type ( "ligands" "decoys" )

set workdir = ${mountdir}/${pdbname}/ligands-decoys/${db_type}/allChunksCombined

echo $pdbname

#ls -l ${mountdir}/${pdbname}/${db_type}/


mkdir -p ${workdir}
cd ${workdir}



# creates a file called dirlist that contains the full path of all directories with docked runs (chunks)
ls -ld ${mountdir}/${pdbname}/ligands-decoys/${db_type}/* | awk '/chunk/{print $9}' > dirlist 

#ls -ld ${mountdir}/${pdbname}/ligands-decoys/${db_type}/*

# for debuging
#echo "print $db_type dirlist:"
#cat dirlist

# script extracts scores from all docking runs specified in dirlist
$d37/extract_all.py 
# script gets poses for top scoring molecules and produces poses.mol2 (default name)
$d37/getposes.py -d ${mountdir}/${pdbname}/ligands-decoys/${db_type}

end # db_type

## combine decoyes and actives
set workdir =  ${mountdir}/${pdbname}/ligands-decoys/dockedLigDecoyCombined

rm -rf ${workdir}
mkdir -p ${workdir}
cd ${workdir}
 
cat ${mountdir}/${pdbname}/ligands-decoys/ligands/allChunksCombined/dirlist ${mountdir}/${pdbname}/ligands-decoys/decoys/allChunksCombined/dirlist > dirlist

# for debuging
#echo "print ALL dirlist"
#cat dirlist

$d37/extract_all.py 
#$d37/getposes.py -d ${mountdir}/${pdbname} 	# doesn't work yet; not really needed
#getposes.py -z -l 1000 -x 2 -f extract_all.sort.uniq.txt -o ligands.1000.mol2 -d /mnt/nfs/work/users/fischer/VDR/27Jan2014_learningDOCKrgc/Enrichment/1DB1/DOCKING/ligands

end # pdbname


