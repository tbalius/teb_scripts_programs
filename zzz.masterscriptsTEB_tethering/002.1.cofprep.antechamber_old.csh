#! /bin/tcsh

#set pdb = "5VBE"

set workdir = `pwd`
#set filedir = "$workdir/$pdb/prep"
set filedir = "$workdir/0001.pdb_files"
#cd $workdir/$pdb/


setenv AMBERHOME /home/baliuste/zzz.programs/amber/amber18 

rm 002_cof_prep; mkdir 002_cof_prep; cd 002_cof_prep


#cp $workdir/xtal-lig.pdb lig.pdb
#cp $filedir/lig_aduct_mod.pdb lig.pdb
#grep GDP $filedir/cof_man.pdb >> lig.pdb
grep GCP $filedir/cof.pdb >> lig.pdb
#grep GNP $filedir/cof.pdb >> lig.pdb
#sed -i 's/<0> /LIG/g' lig1.mol2

set charge = -3
#set charge = -4

$AMBERHOME/bin/antechamber -i lig.pdb -fi pdb -o lig.ante.mol2 -fo mol2 

$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2 -o lig.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc $charge
$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2  -o lig.ante.pdb  -fo pdb
$AMBERHOME/bin/antechamber -i lig.ante.charge.mol2 -fi mol2  -o lig.ante.charge.prep -fo prepi
$AMBERHOME/bin/parmchk2 -i lig.ante.charge.prep -f  prepi -o lig.ante.charge.frcmod

#diff 002_cof_prep/lig.ante.charge.frcmod 002_cof_prep/lig.ante.charge_man_mod.frcmod
#16c16
#< cd-hn-nh-hn         1.1          180.0         2.0          Same as X -X -na-hn, penalty score= 41.2 (use general term))
#---
#> cd-hn-nh-hn        10.5          180.0         2.0          Same as X -X -na-hn, penalty score= 41.2 (use general term))
#>

# replace force constant. 
sed -e 's/cd-hn-nh-hn         1.1/cd-hn-nh-hn        10.5/g' lig.ante.charge.frcmod > lig.ante.charge_man_mod.frcmod

