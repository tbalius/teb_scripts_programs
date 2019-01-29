#!/bin/csh 

# get all xtal strcutures as rmsd references.

setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK"
setenv MSMSPATH  "/nfs/home/tbalius/zzz.programs/msms"

source /nfs/soft/python/envs/complete/latest/env.csh

set path = ( $MSMSPATH $path )

set list = `cat pdblist ` 
#set list = `cat pdblist_all ` 
#set list = '4NVE'

#set mountdir = "/mnt/nfs/work/tbalius/Water_Project/run_DOCK3.7"
set mountdir = `pwd`

# loop over all DUDE systems
foreach pdbname ( $list )

echo " ${pdbname} "

set workdir = ${mountdir}/workingdir/${pdbname}

## so you don't blow away stuff
if ( -s $workdir ) then
   echo "$workdir exits"
   continue # stop. go to the next entry in loop.  
endif

  mkdir -p ${workdir}
  cd ${workdir}
  
  ln -s $MSMSPATH/atmtypenumbers .
  python $DOCKBASE/proteins/pdb_breaker/be_blasti.py --pdbcode $pdbname nocarbohydrate original_numbers | tee -a pdbinfo_using_biopython.log


  if !(-s rec.pdb) then
      echo "rec.pdb is not found"
  endif

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


