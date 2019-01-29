#! /bin/tcsh


set workdir = `pwd`
cd $workdir


 setenv AMBERHOME /nfs/soft/amber/amber14

rm lig; mkdir lig; cd lig

cp $workdir/xtal-lig.pdb lig.pdb
#cp $workdir/33443.pdb lig.pdb
#sed -i 's/<0> /LIG/g' lig1.mol2

$AMBERHOME/bin/antechamber -i lig.pdb -fi pdb -o lig.ante.mol2 -fo mol2 

$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2 -o lig.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc 2
$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2  -o lig.ante.pdb  -fo pdb
$AMBERHOME/bin/antechamber -i lig.ante.charge.mol2 -fi mol2  -o lig.ante.charge.prep -fo prepi
$AMBERHOME/bin/parmchk -i lig.ante.charge.prep -f  prepi -o lig.ante.charge.frcmod

