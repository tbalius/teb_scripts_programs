#! /bin/tcsh

#set pdb = "5VBE"

set username = `whoami`
set mountdir = `pwd`
#set filedir = "$workdir/$pdb/prep"
set filedir = "$mountdir/0001.chimera"

setenv AMBERHOME /home/${username}/zzz.programs/amber/amber18 

foreach name ( \
ATP_mon1 \
ATP_mon2 \
)

#rm 0002_cof_${name}_prep; mkdir 0002_cof_${name}_prep; cd 0002_cof_${name}_prep
set workdir = ${mountdir}/0002_cof_${name}_prep
rm ${workdir}
mkdir ${workdir}
cd ${workdir}


cat $filedir/${name}.pdb  >> lig.pdb

#set charge = -3
set charge = -4

$AMBERHOME/bin/antechamber -i lig.pdb -fi pdb -o lig.ante.mol2 -fo mol2 

$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2 -o lig.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc $charge
$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2  -o lig.ante.pdb  -fo pdb
$AMBERHOME/bin/antechamber -i lig.ante.charge.mol2 -fi mol2  -o lig.ante.charge.prep -fo prepi
$AMBERHOME/bin/parmchk2 -i lig.ante.charge.prep -f  prepi -o lig.ante.charge.frcmod

end
