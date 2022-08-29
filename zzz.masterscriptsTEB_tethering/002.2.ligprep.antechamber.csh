#! /bin/tcsh

#set pdb = "5VBE"

#set workdir = `pwd`
#set filedir = "$workdir/$pdb/prep"
#cd $workdir/$pdb
#set filedir = "$workdir/0001.pdb_files"

set pwd = `pwd`
#set workdir = `pwd`
#set filedir = "$workdir/$pdb/prep"

  set mut = E37C
  #set lig = DL2040
  #set lig = DL2078 
  set lig = DL1314_Protomer1 
  foreach pose (  \
                 1\
                 2\
                 3\
 )

  #set workdir = $pwd/${mut}/${lig}/pose${pose}/0001.pdb_files
  set workdir = $pwd/${mut}/${lig}/pose${pose}
  cd $workdir

set filedir = "$workdir/0001.pdb_files"
#cd $workdir/$pdb/



setenv AMBERHOME /home/baliuste/zzz.programs/amber/amber18 

rm -rf 002_lig_prep; mkdir 002_lig_prep; cd 002_lig_prep


#cp $workdir/xtal-lig.pdb lig.pdb
#cp $filedir/lig_aduct_mod.pdb lig.pdb
#grep "LIG" $filedir/lig_aduct_mod.pdb > lig.pdb
#grep "LIG" $filedir/lig_aduct_mod.pdb | grep -v " HG " | grep -v " H1 " > lig.pdb
#grep "LIG" $filedir/lig_aduct_mod.pdb | grep -v " HG " | grep -v " HS1 " > lig.pdb
#cp $filedir/lig_aduct_mod.pdb lig_ori.pdb
#grep -v " HG " lig_ori.pdb | grep -v " SH " | grep "HETATM" > lig.pdb
#echo "CONECT    1    2" >> lig.pdb
#sed -i 's/<0> /LIG/g' lig1.mol2
cp $filedir/lig_aduct_mod.pdb lig.pdb
#~/zzz.programs/openbabel/install/bin/obabel -imol2 $filedir/lig_aduct_modbefore_dockprep.mol2 -opdb -O lig.pdb

set charge = 0.0
#set charge = 1.0

$AMBERHOME/bin/antechamber -i lig.pdb -fi pdb -o lig.ante.mol2 -fo mol2 
#$AMBERHOME/bin/antechamber -i lig.ante.mol2 -fi mol2 -o lig.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc ${charge}
$AMBERHOME/bin/antechamber -dr no -i lig.ante.mol2 -fi mol2 -o lig.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc ${charge}
#exit

$AMBERHOME/bin/antechamber -dr no -i lig.ante.mol2 -fi mol2  -o lig.ante.pdb  -fo pdb
$AMBERHOME/bin/antechamber -dr no -i lig.ante.charge.mol2 -fi mol2  -o lig.ante.charge.prep -fo prepi
$AMBERHOME/bin/parmchk2 -dr no -i lig.ante.charge.prep -f  prepi -o lig.ante.charge.frcmod


#python ${workdir}/change_prep_file.py lig.ante.charge.prep lig.ante.charge
python ${pwd}/change_prep_file_atom_names.py lig.ante.charge.prep lig.ante.charge

end
