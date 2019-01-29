#!/bin/csh

# This script creates a log adjusted AUC (ROC) plot with ligand vs decoy results
# need X11 forwarding enabled when running remotely (ssh sgehead -X). 

set filedir = "/mnt/nfs/work/users/fischer/VDR/waterchannel_3az2"		#CHANGE THIS
set mountdir = "/mnt/nfs/work/users/fischer/VDR/waterchannel_3az2"		#CHANGE THIS
set d37 =  $DOCK_BASE/src/dock37tools/
set dude_dir = "/mnt/nfs/work/users/fischer/VDR/lig-decoy-db" 	# should contain decoy.smi and ligands.smi

# 
ln -s /mnt/nfs/work/users/fischer/VDR/lig-decoy-db/ligands.mod.smi /mnt/nfs/work/users/fischer/VDR/lig-decoy-db/ligands.smi

# CHANGE THIS
set list = "3AZ2"
#set list = `cat filename`
#set list = `cat $1`

foreach pdbname ( $list )

set workdir = ${mountdir}/${pdbname}/ROC_ligdecoy/

# This script will not work without the following line:
echo "HERE is the HAWK" 

# checks that previous script 0003 has produced mol2 files
if (! ( -s $mountdir/${pdbname}/ligands-decoys/decoys/allChunksCombined/poses.mol2) && ! (-s $mountdir/${pdbname}/ligands-decoys/ligands/allChunksCombined/poses.mol2 )) then
   ls -l $mountdir/${pdbname}/ligands-decoys/decoys/allChunksCombined/poses.mol2 
   ls -l $mountdir/${pdbname}/ligands-decoys/ligands/allChunksCombined/poses.mol2
   echo "skipping ${pdbname}. cannot generate ROC"
   continue
endif


rm -rf $workdir
mkdir -p $workdir
cd $workdir

#wget http://dude.docking.org/targets/aa2ar/actives_final.ism

# reads ZINC ids (ligand or decoy molecule names)
# everything
awk '{print $2}' $dude_dir/decoys.smi > decoys.name
awk '{printf "%9s\n", $2}' $dude_dir/ligands.smi > ligands.name
#things that finished docking
awk '{print $3}' $mountdir/${pdbname}/ligands-decoys/decoys/allChunksCombined/extract_all.sort.uniq.txt > decoys.finished.name
awk '{print $3}' $mountdir/${pdbname}/ligands-decoys/ligands/allChunksCombined/extract_all.sort.uniq.txt > ligands.finished.name

cat ${mountdir}/${pdbname}/ligands-decoys/ligands/allChunksCombined/dirlist ${mountdir}/${pdbname}/ligands-decoys/decoys/allChunksCombined/dirlist > dirlist

#which enrich.py
set enrich_py = $d37/enrich.py
set plots_py = $d37/plots.py

pwd
# calculates AUCs, stores in txt file which is then plotted for finished ligands and decoys
python ${enrich_py} -i .  -o . --ligand-file=ligands.finished.name --decoy-file=decoys.finished.name 
python ${plots_py} -i . -o . --ligand-file=ligands.finished.name --decoy-file=decoys.finished.name -l $pdbname 

mv roc.txt     roc.finished.txt
mv roc_own.txt roc_own.finished.txt 
mv roc_own.png roc_own.finished.png

# 
# calculates AUCs, stores in txt file which is then plotted for all ligands and decoys
# - i is the flag for the input directory, this dir should contain the extract_all.sort.uniq.txt. 
#  the scripts enrich_py and plots_py will go through the extract file and look for the ligand and decoy names.
#  when it finds them it will populate the ROC cruve. these values are devied by the total number of ligand or decoys.
#  note that ofen not all ligands and not all decoy finish so the point (1,1) is always included and interpolations is performed . . . 
#
#python ${enrich_py} -i $mountdir/${pdbname}/ligands-decoys/dockedLigDecoyCombined/ -o . --ligand-file=ligands.name --decoy-file=decoys.name 
#python ${plots_py} -i $mountdir/${pdbname}/ligands-decoys/dockedLigDecoyCombined/ -o . --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 
python ${enrich_py} -i . -o . --ligand-file=ligands.name --decoy-file=decoys.name 
python ${plots_py} -i . -o . --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 

end   #pbdname

