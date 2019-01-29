

#This script needs internet access to scrap the pdb website to smiles for the ligand bound in the xtal structure

set list = `cat pdblist `
set mountdir = `pwd`
set workdir = "$mountdir/workingdir/smiles"
set dbdir   = "/mnt/nfs/home/tbalius/work/Water_Project_all_in_the_same_frame_ph4/databases"


# this script requiers chemaxon.  
# put it in your path and define the license  
source /nfs/soft/jchem/current/env.csh

# source python
source /nfs/soft/python/envs/complete/latest/env.csh

if (-e $workdir) then
   echo "$workdir exists"
   exit
endif

mkdir $workdir
cd $workdir

touch pdbligands.smi
touch ligcode_to_pdb.txt

foreach pdbname ( $list )

  if ! (-e $mountdir/workingdir/$pdbname/xtal-lig.pdb) then
    echo "$mountdir/workingdir/$pdbname/xtal-lig.pdb does not exist"
    continue 
  endif

  set count = `awk '/ATOM/{print $4}' $mountdir/workingdir/$pdbname/xtal-lig.pdb | sort -u | wc -l`

  if ( $count > 1) then
    echo "Ooh.  there are $count ligand codes (resnames) in the file"
    continue
  endif

  set ligcode = `awk '/ATOM/{print $4}' $mountdir/workingdir/$pdbname/xtal-lig.pdb | sort -u`

  #python $mountdir/search_pdb_lig_code.py $ligcode 
  python $mountdir/search_pdb_lig_code.py $ligcode >> pdbligands.smi

  #set smiles = `python ~/zzz.scripts/search_pdb_lig_code.py $ligcode | awk '{print $1}'`
  set smiles = `tail -1 pdbligands.smi | awk '{print $1}'`

  echo "$pdbname $ligcode $smiles" 
  echo "$pdbname $ligcode"  >> ligcode_to_pdb.txt

end #pdbname

#chemaxon will remove explited hydrogens
 molconvert mol2 pdbligands.smi -Y -o pdbligands.mol2
 molconvert smiles pdbligands.mol2 -Y -o pdbligands_mod.smi
 paste pdbligands_mod.smi pdbligands.smi | awk '{print $1 " " $3}' | sort -u > ! pdbligands_mod2.smi

# get zinc ligands that enrichments are run on
 cp ${dbdir}/ligands/ligands.smi zincligands.smi
 molconvert mol2 zincligands.smi -Y -o zincligands.mol2
 molconvert smiles zincligands.mol2 -Y -o zincligands_mod.smi
 paste zincligands_mod.smi zincligands.smi | awk '{print $1 " " $3}' | sort -u > ! zincligands_mod2.smi
## CAUTION: FOR CHEMBL or DUDE ligands change to $4 to pull out correct CHEMBL name
# paste zincligands_mod.smi zincligands.smi | awk '{print $1 " " $4}' | sort -u > ! zincligands_mod2.smi

