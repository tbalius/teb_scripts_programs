#!/bin/csh 

set path = ( /nfs/home/tbalius/zzz.programs/msms $path )

  ln -s /nfs/home/tbalius/zzz.programs/msms/atmtypenumbers .
  #python ~tbalius/zzz.scripts/be_blasti.py --pdbcode $pdbname nocarbohydrate renumber | tee -a pdbinfo_using_biopython.log
  python ~tbalius/zzz.scripts/be_blasti.py --pdbfile complex.pdb nocarbohydrate original_numbers | tee -a pdbinfo_using_biopython.log

  #grep "HOH" complex.pdb > waters.pdb
  grep "^HETATM...........HOH" complex.pdb > waters.pdb

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



