#!/bin/csh

# This script creates a log adjusted AUC (ROC) plot with ligand vs decoy results
# need X11 forwarding enabled when running remotely (ssh sgehead -X). 

# TEB/ MF -- March 2017

setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK
source /nfs/soft/python/envs/complete/latest/env.csh


set filedir = `pwd`
set mountdir = $filedir/docking/2runEnrich/
set d37 =  $DOCKBASE/analysis/

cd $mountdir



set dude_dir = "/mnt/nfs/home/tbalius/work/Water_Project_all_in_the_same_frame_ph4/databases"  # should contain decoy.smi and ligand.smi for ROC script 00005...csh

# 
#ln -s $dude_dir/ligands/ligands.smi .
#ln -s $dude_dir/decoys/decoys.smi .

# CHANGE THIS
#set list = "4NVA_gist 4NVA_nogist"
#set list = "4NVA_gist"
#set list = "4NVA_nogist"
#set list = "4NVA_min"
set list = "4NVA_gist_elstat0p9"
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
# for other names e.g. CHEMBL try this instead
#awk '{printf "%9s\n", $3}' $dude_dir/ligands/ligands.smi > ligands.name

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
python ${plots_py} -i . -o . --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 		# to plot logAUC
python ${plots_py} -i . -o auc_plot -n --ligand-file=ligands.name --decoy-file=decoys.name -l $pdbname 	#-n flag to plot "normal" AUC

end   #pbdname

echo " logAUCs > Look at plots: \n eog $mountdir/$list/ROC_ligdecoy/*png \n "
echo "         > Or better for printing: \n gthumb $mountdir/$list/ROC_ligdecoy/*png  \n"
echo "For EF's > see script 015.c.calc_enrichment_factor_gen.py for calculation of EF's \n"

# For AUC's docking/2runEnrich/4NVA_gist/ROC_ligdecoy/roc_own.txt is used for plotting.
# Note that roc_own.txt is for AUC but roc_own.png in /ROC_ligdecoy/ dir contains logAUC plot.

