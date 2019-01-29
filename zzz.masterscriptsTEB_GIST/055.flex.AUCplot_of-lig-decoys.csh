#!/bin/csh

# TEB/ MF -- March 2017

# This script creates a log adjusted AUC (ROC) plot with ligand vs decoy results
# need X11 forwarding enabled when running remotely (ssh sgehead -X). 

setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK
source /nfs/soft/python/envs/complete/latest/env.csh


set filedir = `pwd`
#set mountdir = $filedir/flex/3runEnrich/  # CHANGE THIS
set mountdir = $filedir/flex_multpose/3runEnrich/  # CHANGE THIS
set d37 =  $DOCKBASE/analysis/

cd $mountdir


# might need to CHANGE THIS
set dude_dir = "/mnt/nfs/home/tbalius/work/Water_Project_all_in_the_same_frame_ph4/databases"  # should contain decoy.smi and ligand.smi for ROC script 00005...csh

# 
#ln -s $dude_dir/ligands/ligands.smi .
#ln -s $dude_dir/decoys/decoys.smi .

# CHANGE THIS
#set list = "4NVA_gist 4NVA_nogist 4NVA_gist_m1.0"
set list = "4NVA_gist 4NVA_nogist"
#set list = "4NVA_gist"
#set list = "4NVA_nogist"
#set list = `cat filename`
#set list = `cat $1`

foreach pdbname ( $list )

set workdir = ${mountdir}/${pdbname}/ROC_ligdecoy/

# This script will not work without the following line:
echo "HERE is the HAWK" 

# checks that previous script 0003 has produced mol2 files
if (! ( -s $mountdir/${pdbname}/decoys/allChunksCombined/poses.mol2) && ! (-s $mountdir/${pdbname}/ligands/allChunksCombined/poses.mol2 )) then
   ls -l $mountdir/${pdbname}/decoys/allChunksCombined/poses.mol2 
   ls -l $mountdir/${pdbname}/ligands/allChunksCombined/poses.mol2
   echo "skipping ${pdbname}. cannot generate ROC"
   continue
endif


rm -rf $workdir
mkdir -p $workdir
cd $workdir

#wget http://dude.docking.org/targets/aa2ar/actives_final.ism

# reads ZINC ids (ligand or decoy molecule names)
# everything
awk '{print $2}' $dude_dir/decoys/decoys.smi > decoys.name
awk '{printf "%9s\n", $2}' $dude_dir/ligands/ligands.smi > ligands.name

cat ${mountdir}/${pdbname}/ligands/allChunksCombined/dirlist ${mountdir}/${pdbname}/decoys/allChunksCombined/dirlist > dirlist

#which enrich.py
set enrich_py = $d37/enrich.py
set plots_py = $d37/plots.py

# 
# calculates AUCs, stores in txt file which is then plotted for all ligands and decoys
# - i is the flag for the input directory, this dir should contain the extract_all.sort.uniq.txt. 
#  the scripts enrich_py and plots_py will go through the extract file and look for the ligand and decoy names.
#  when it finds them it will populate the ROC cruve. these values are devied by the total number of ligand or decoys.
#  note that ofen not all ligands and not all decoy finish so the point (1,1) is always included and interpolations is performed . . . 
#
#python ${enrich_py} -i $mountdir/${pdbname}/dockedLigDecoyCombined/ -o . --ligand-file=ligands.name --decoy-file=decoys.name 
#python ${plots_py} -i $mountdir/${pdbname}/dockedLigDecoyCombined/ -o . --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 
python ${enrich_py} -i . -o . --ligand-file=ligands.name --decoy-file=decoys.name 
python ${plots_py} -i . -o . --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 

end   #pbdname

echo "To visualize plots run something like this \n eog flex/3runEnrich/PDBname_*/ROC_ligdecoy/*png"


