#!/bin/csh

#This script provides a alternative way to dock a DUD-e like ligand-decoy-database for the enrichment evaluation of actives over decoys
#It assumes that ligands and decoys have been pre-prepation (see script blablabla_ToDo) which needs to be run in SF.

# TEB/ MF -- March 2017

setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK 

#set indockType = '_gist'
set indockType = '_nogist'

set pwd = `pwd`
#set filedir = "/mnt/nfs/home/jklyu/work/DOCK_tutorial"  #CHANGE THIS
set filedir = ${pwd}/flex/2prep  #CHANGE THIS

# this is where the work is done:
set mountdir = ${pwd}/flex_multpose/3runEnrich   # Might CHANGE THIS
set dude_dir = "/mnt/nfs/home/tbalius/work/Water_Project_all_in_the_same_frame_ph4/databases"  # should contain decoy.smi and ligand.smi for ROC script 00005...csh
  ## TO DO - rename this outside in the dir structure and call in blbalbalbabla script
if (-s $dude_dir) then
 echo " $dude_dir exist"
else
 # this is something to modified in future. 
 # probably better to exit if it is not there.
 echo "databases do not exist. "
 echo "consider making a symbolic link to the database files"
endif

set list = "4NVA"  # CHANGE THIS (pdbname)
foreach pdbname ( $list )
# creates "ligands" and "decoys" and has the aim to dock all of the subsets for those two
foreach db_type ( "ligands" "decoys" )

set workdir1 = "${mountdir}/${pdbname}${indockType}/${db_type}"
echo $workdir1
#
mkdir -p  ${workdir1}
cd  ${workdir1}
#creat dirlist for *.db2.gz files prepared for docking
ls ${dude_dir}/${db_type}/*.db2.gz > ${db_type}_files.txt
#copy the files needed for dock
cp ${filedir}/INDOCK${indockType} ${workdir1}/INDOCK


sed -i 's/number_save                   1/number_save                   10/g' INDOCK
sed -i 's/number_write                  1/number_write                  10/g' INDOCK

cp INDOCK INDOCK_multpose

ln -s ${filedir}/dockfiles/ ${workdir1}
ln -s ${filedir}/gistfiles/ ${workdir1}

#use dirlist to creat chunks for job submission
python $DOCKBASE/docking/setup/setup_db2_zinc15_file_number.py ./ chunk ./${db_type}_files.txt 500  count

csh $DOCKBASE/docking/submit/submit.csh

end # db_type
end # pdbname

echo "When done look at this directory:"
echo "flex/3runEnrich/PDBname_gist/ligands/chunk0000/OUTDOCK"
echo "			   _nogist/decoys/chunk0000/OUTDOCK"
echo "etc. to check whether everything ran properly."
