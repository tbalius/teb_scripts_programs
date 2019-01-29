#!/bin/csh 

# this script calls be_blasti.py which creates a receptor and ligand file from a (list of) pdbcode(s).

# msms is a molecular surface generation program needed for be_blasti.py to run
# which is put in your path
set path = ( /nfs/home/tbalius/zzz.programs/msms $path )

set list = "1DB1" # or use `cat filename` to list your pdb codes here from a text file like pdblist_rat, to loop over each variable (pdb code) later
#set list = `cat $1`
#set list = `cat /nfs/work/users/tbalius/VDR/Enrichment/pdblist_rat `

# CHANGE THIS, according to where the magic is going to happen
#set mountdir = "/mnt/nfs/work/users/tbalius/VDR/"
set mountdir = `pwd` 

# loop over pdbnames e.g. 1DB1 or list
foreach pdbname ( $list )

echo " ${pdbname} "

# for each pdb makes a directory with its name
set workdir = ${mountdir}/${pdbname}

## so you don't blow away stuff; continue means STOP here and continue with next pdb from list
if ( -s $workdir ) then
   echo "$workdir exits"
   continue
endif

  mkdir -p ${workdir}
  cd ${workdir}

# the atom type definition is needed for msms which is sym-linked into the cwd
  ln -s /nfs/home/tbalius/zzz.programs/msms/atmtypenumbers .
  #python ~/zzz.scripts/be_blasti.py --pdbcode $pdbname nocarbohydrate renumber | tee -a pdbinfo_using_biopython.log        
# carbs are disregarded as ligands! if it is: carbohydrate instead of nocarbohydrate
# renumber renumbers the residue number
  python ~tbalius/zzz.scripts/be_blasti.py --pdbcode $pdbname nocarbohydrate original_numbers | tee -a pdbinfo_using_biopython.log

# error checking looks for receptor and ligand file which should be produced by be_blasti.py
  if !(-s rec.pdb) then
      echo "rec.pdb is not found"
  endif

  mv rec.pdb temp.pdb
  grep -v TER temp.pdb | grep -v END  > rec.pdb

  rm temp.pdb

# be_blasti.py produces peptide which may be used as a ligand if no other ligand is produced
  if (-s lig.pdb) then
     sed -e "s/HETATM/ATOM  /g" lig.pdb > xtal-lig.pdb
  else if (-s pep.pdb) then ## if no ligand and peptide
     sed -e "s/HETATM/ATOM  /g" pep.pdb > xtal-lig.pdb
  else
     echo "Warning: No ligand or peptid."
  endif

end # system


