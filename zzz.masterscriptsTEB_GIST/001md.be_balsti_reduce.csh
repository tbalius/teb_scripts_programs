#!/bin/csh 

# TEB and MF comments
# This script runs beblasti, creates dirs and splits pdb into rec and lig file for running amber MD.

# Setting up necessary environments
source /nfs/soft/python/envs/complete/latest/env.csh
setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK"
# setenv AMBERHOME /nfs/soft/amber/amber14
set path = ( /nfs/home/tbalius/zzz.programs/msms $path )

# list of PDBs
# 4NVA apo with waters, 4NVE ligand
#set list = `cat /nfs/work/users/tbalius/VDR/Enrichment/pdblist_rat `
set list = '4NVE 4NVA'		### CHANGE THIS

#set mountdir = "/mnt/nfs/work/tbalius/Water_Project/run_DOCK3.7"
set mountdir = `pwd`

# loop over all PDBs 
foreach pdbname ( $list )

echo " ${pdbname} "

set workdir = ${mountdir}/MDrundir/prep/${pdbname}

# check if workdir exists
if ( -s $workdir ) then
   echo "$workdir exits"
   continue
endif

# if it exists do this:     rm -rf ${workdir}
  mkdir -p ${workdir}
  cd ${workdir}
  
  ln -s /nfs/home/tbalius/zzz.programs/msms/atmtypenumbers .
  #python ~/zzz.scripts/be_blasti.py --pdbcode $pdbname nocarbohydrate renumber | tee -a pdbinfo_using_biopython.log
  #>> to use e.g. buffer like MES without modifying the beblasti script, rename lig code in pdb file and use next line
  #>> to use pdbfile replace --pdbcode with --pdbfile (filename incl .pdb)
  #python /nfs/home/tbalius/zzz.scripts/be_blasti.py --pdbfile $pdbfile nocarbohydrate original_numbers | tee -a pdbinfo_using_biopython.log
  python /nfs/home/tbalius/zzz.scripts/be_blasti.py --pdbcode $pdbname nocarbohydrate original_numbers | tee -a pdbinfo_using_biopython.log
  
# extracts all waters into separate pdb file
  grep HOH  $workdir/${pdbname}_A.pdb > $workdir/water.pdb

  if !(-s rec.pdb) then
      echo "rec.pdb is not found"
  endif

# nomenclature clean-up.
  mv rec.pdb temp.pdb
  grep -v TER temp.pdb | grep -v END  > rec.pdb
  rm temp.pdb

  if (-s lig.pdb) then
     sed -e "s/HETATM/ATOM  /g" lig.pdb > xtal-lig.pdb
  else if (-s pep.pdb) then ## if no ligand and peptide
     sed -e "s/HETATM/ATOM  /g" pep.pdb > xtal-lig.pdb
  else
     echo "Warning: No ligand or peptid."
  endif

end # system


