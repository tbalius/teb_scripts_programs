#! /bin/tcsh

set mountdir = `pwd`
set scriptdir = /home/baliuste/zzz.github/teb_scripts_programs/zzz.scripts
set charge = -4
#set charge = -3

# set list = `ls cof*.pdb` # or use `cat filename` to list your pdb codes here from a text file like pdblist_rat, to loop over each variable (pdb code) later
# loop over pdbnames e.g. 1DB1 or list
# foreach pdbname ( $list )
# set pdb = $pdbname:r
#
#set workdir = ${mountdir}/$pdb/chimera/
set workdir = ${mountdir}/chimera/
cd $workdir


#setenv AMBERHOME /nfs/soft/amber/amber14
#setenv AMBERHOME  /mnt/nasapps/production/amber/amber16 
#setenv AMBERHOME  /opt/nasapps/production/amber/amber16/ 

#if (! $?LD_LIBRARY_PATH) then
#    setenv  LD_LIBRARY_PATH  ""
#    setenv  LD_LIBRARY_PATH  $AMBERHOME/lib:$AMBERHOME/lib64
#else
#    setenv  LD_LIBRARY_PATH  ${LD_LIBRARY_PATH}:$AMBERHOME/lib:$AMBERHOME/lib64
#endif
#

#echo $LD_LIBRARY_PATH

rm cof; mkdir cof; cd cof

#cp $workdir/xtal-cof.pdb lig.pdb
#cp $workdir/cofactor_prot.pdb cof.pdb
#grep -v "H2G" $workdir/cof_addh.pdb | grep HETATM > cof.pdb
grep -v "H3G" $workdir/cof_addh.pdb | grep HETATM > cof.pdb
#sed -i 's/<0> /LIG/g' cof1.mol2

$AMBERHOME/bin/antechamber -i cof.pdb -fi pdb -o cof.ante.mol2 -fo mol2 

#$AMBERHOME/bin/antechamber -i cof.ante.mol2 -fi mol2 -o cof.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc ${charge}
$AMBERHOME/bin/antechamber -i cof.ante.mol2 -fi mol2 -o cof.ante.charge.mol2 -fo mol2 -c bcc -at sybyl -nc ${charge} -s 2
$AMBERHOME/bin/antechamber -i cof.ante.mol2 -fi mol2  -o cof.ante.pdb  -fo pdb
$AMBERHOME/bin/antechamber -i cof.ante.charge.mol2 -fi mol2  -o cof.ante.charge.prep -fo prepi
$AMBERHOME/bin/parmchk2 -i cof.ante.charge.prep -f  prepi -o cof.ante.charge.frcmod

#end
