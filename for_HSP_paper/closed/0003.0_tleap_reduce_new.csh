

#!/bin/csh/prepdir
# This script uses first reduce and then tleap to prepare a receptor for amber.
# The outputs are: parameter topology file (prm7) and a coordinate file (rst7) 
#
# Written by Trent balius
# TEB/ MF comments Feb2017

set username = `whoami`
#setenv AMBERHOME /home/${username}/zzz.programs/amber/amber18
setenv AMBERHOME /home/${username}/zzz.programs/amber/amber20_src
setenv DOCKBASE "/home/${username}/zzz.github/DOCK"
# CUDA for GPU
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

#set pdb = "5VBE"
set mountdir = `pwd`
#set filedir = $mountdir/0001.files  ## modify this line!
set filedir = $mountdir/0001.chimera  ## modify this line!
#set parmdir = $mountdir/001_files  ## modify this line!
#set prepdir = $mountdir/002_gtp_prep  ## modify this line!
#set workdir = $mountdir/\${pdb}/003md_tleap
set workdir = ${mountdir}/0003md_tleap
#set workdir = $mountdir/003md_tleap_new
set scriptdir = /home/${username}/zzz.github/teb_scripts_programs/zzz.scripts 


#set resnum = " 37" 
#set resnum = "153"
#set resnum = "165"
#set resnum = " 65"
#set resnum = " 59"

# check if workdir exists
if ( -s $workdir ) then
   echo "$workdir exits"
   exit
endif
       
# if it exists do this:     rm -rf ${workdir}
mkdir -p ${workdir}
cd ${workdir}

foreach name (\
 mon1_no_ATP \
 mon2_no_ATP \
 RAF         \
 CDC37       \
)
 
set workdir2 =  ${workdir}/${name}
mkdir ${workdir2}
cd ${workdir2}

#cat ${filedir}/${name}_complete_noH.pdb | sed 's/HETATM/ATOM  /g' | grep "^ATOM" > rec.pdb
cat ${filedir}/${name}_complete_noH.pdb | sed 's/HETATM/ATOM  /g' | grep "^ATOM" | grep -v " MG " > rec.pdb
cat ${filedir}/${name}_complete_noH.pdb | sed 's/HETATM/ATOM  /g' | grep "^ATOM" | grep " MG " > ions.pdb

# produces tleap input file -- renumbers rec
cat << EOF >! tleap.rec.1.in 
set default PBradii mbondi2
# load the protein force field

source leaprc.protein.ff14SB
#source leaprc.phosaa10
source leaprc.phosaa14SB
source leaprc.water.tip3p
# load ions
loadAmberParams frcmod.ions234lm_1264_tip3p

REC = loadpdb rec.pdb
saveamberparm REC rec.1.leap.prm7 rec.1.leap.rst7
quit
EOF

# runs tleap and converts parameter and coordinate restart file back into pdb file
$AMBERHOME/bin/tleap -s -f tleap.rec.1.in > ! tleap.rec.1.out
$AMBERHOME/bin/ambpdb -p rec.1.leap.prm7 < rec.1.leap.rst7 >! rec.1.leap.ori.pdb 

# Remove hydrogens before running leap.
grep -v ' H$' rec.1.leap.ori.pdb >! rec.1.leap.pdb

# nomenclature clean-up
$DOCKBASE/proteins/Reduce/reduce -HIS -FLIPs rec.1.leap.pdb >! rec.nowat.reduce.pdb
sed -i 's/HETATM/ATOM  /g' rec.nowat.reduce.pdb 
# grep -v means "everything but"; last grep statement removes inconsistently named HEM hydrogens (for leap to be added back in)
grep "^ATOM  " rec.nowat.reduce.pdb | sed -e 's/   new//g' | sed 's/   flip//g' | sed 's/   std//g' | grep -v "OXT" | grep -v " 0......HEM" >! rec.nowat.reduce_clean.pdb
#grep "^ATOM  " rec.nowat.reduce.pdb | sed -e 's/   new//g' | sed 's/   flip//g' | sed 's/   std//g' | grep -v " 0......HEM" >! rec.nowat.reduce_clean.pdb
# grep -v means "everything but"; last grep statement removes inconsistently named HEM hydrogens (for leap to be added back in)


#curl docking.org/~tbalius/code/waterpaper2017/scripts/replace_his_with_hie_hid_hip.py > replace_his_with_hie_hid_hip.py
#curl docking.org/~tbalius/code/waterpaper2017/scripts/replace_cys_to_cyx.py > replace_cys_to_cyx.py
#curl docking.org/~tbalius/code/waterpaper2017/scripts/add.ters.py > add.ters.py


# python scripts do these three things: 1) checks his to give protonation specific names; 2) checks for disulphide bonds; 3) checks for missing residues and adds TER flag
python $scriptdir/replace_his_with_hie_hid_hip.py rec.nowat.reduce_clean.pdb rec.nowat.1his.pdb
python $scriptdir/replace_cys_to_cyx.py rec.nowat.1his.pdb rec.nowat.2cys.pdb
python $scriptdir/add.ters.py rec.nowat.2cys.pdb rec.nowat.3ter.pdb


cat ions.pdb >> rec.nowat.3ter.pdb
#cp rec.nowat.3ter.pdb rec.nowat.final.pdb
grep -v "^.................NME.........................................................H" rec.nowat.3ter.pdb > rec.nowat.near_final.pdb
sed -e 's/OP1 SEP    12/O1P SEP    12/g' -e 's/OP2 SEP    12/O2P SEP    12/g' rec.nowat.near_final.pdb > rec.nowat.final.pdb
end # name

 cd ${workdir}

#loadamberparams ${parmdir}/disulfide.frcmod
cat << EOF >! tleap.rec.in 

set default PBradii mbondi2
# load the protein force field
source leaprc.protein.ff14SB
#source leaprc.phosaa10
source leaprc.phosaa14SB
source leaprc.water.tip3p
source leaprc.gaff2
# load ions
loadAmberParams frcmod.ions234lm_1264_tip3p

# load cofactor parameters.  

loadamberparams ${mountdir}/0002_cof_ATP_mon1_prep/lig.ante.charge.frcmod

loadamberprep ${mountdir}/0002_cof_ATP_mon1_prep/lig.ante.charge.prep


MO1 = loadpdb mon1_no_ATP/rec.nowat.final.pdb
MO2 = loadpdb mon2_no_ATP/rec.nowat.final.pdb
RAF = loadpdb RAF/rec.nowat.final.pdb
CDC = loadpdb CDC37/rec.nowat.final.pdb
CF1 = loadpdb ${mountdir}/0002_cof_ATP_mon1_prep/lig.ante.pdb
CF2 = loadpdb ${mountdir}/0002_cof_ATP_mon2_prep/lig.ante.pdb
EOF

if (-e mon1_no_ATP/rec.nowat.2cys.pdb.for.leap ) then
  cat mon1_no_ATP/rec.nowat.2cys.pdb.for.leap >> tleap.rec.in
endif
if (-e mon2_no_ATP/rec.nowat.2cys.pdb.for.leap ) then
  cat mon2_no_ATP/rec.nowat.2cys.pdb.for.leap >> tleap.rec.in
endif
if (-e RAF/rec.nowat.2cys.pdb.for.leap ) then
  cat RAF/rec.nowat.2cys.pdb.for.leap >> tleap.rec.in
endif
if (-e CDC37/rec.nowat.2cys.pdb.for.leap ) then
  cat CDC37/rec.nowat.2cys.pdb.for.leap >> tleap.rec.in
endif

cat << EOF >> tleap.rec.in
CO1 = combine {MO1 MO2 RAF CDC CF1 CF2} #1
# 2 is just RAF
CO3 = combine {MO1 MO2 CDC CF1 CF2} #3
CO4 = combine {MO1 MO2 CF1 CF2} #4
CO5 = combine {MO1 CF1} #5 is MO1
CO6 = combine {MO2 CF2} #6 is MO2
CO7 = combine {RAF CDC} #7 is RAF CDC

saveamberparm CO1 com1.mmrc.leap.prm7 com1.mmrc.leap.rst7
saveamberparm RAF raf2.leap.prm7      raf2.leap.rst7
saveamberparm CO3 com3.mmc.leap.prm7  com3.mmc.leap.rst7
saveamberparm CO4 com4.mm.leap.prm7   com4.mm.leap.rst7
saveamberparm CO5 com5.m1.leap.prm7   com5.m1.leap.rst7
saveamberparm CO6 com6.m2.leap.prm7   com6.m2.leap.rst7
saveamberparm CO7 com7.rc.leap.prm7   com7.rc.leap.rst7

solvateBox CO1 TIP3PBOX 10.0
saveamberparm CO1 com1.watbox.leap.prm7 com1.watbox.leap.rst7
quit
EOF

$AMBERHOME/bin/tleap -s -f tleap.rec.in > ! tleap.rec.out

# for ease of visualization in pymol 
$AMBERHOME/bin/ambpdb -p com1.mmrc.leap.prm7 < com1.mmrc.leap.rst7 > com1.mmrc.leap.pdb
$AMBERHOME/bin/ambpdb -p raf2.leap.prm7      < raf2.leap.rst7      > raf2.leap.pdb
$AMBERHOME/bin/ambpdb -p com3.mmc.leap.prm7  < com3.mmc.leap.rst7  > com3.mmc.leap.pdb
$AMBERHOME/bin/ambpdb -p com4.mm.leap.prm7   < com4.mm.leap.rst7   > com4.mm.leap.pdb
$AMBERHOME/bin/ambpdb -p com5.m1.leap.prm7   < com5.m1.leap.rst7   > com5.m1.leap.pdb
$AMBERHOME/bin/ambpdb -p com6.m2.leap.prm7   < com6.m2.leap.rst7   > com6.m2.leap.pdb
$AMBERHOME/bin/ambpdb -p com7.rc.leap.prm7   < com7.rc.leap.rst7   > com7.rc.leap.pdb

#$AMBERHOME/bin/ambpdb -mol2 -p com.leap.prm7 < com.leap.rst7 > com.leap.mol2

echo "Look at com.leap.pdb in pymol. May have to delete last column in pdb file for pymol. "
# may have to remove element column so pymol does not get confused
#

# inspect tleap.rec.out and the leap.log file
# visually inspect (VMD) rec.10wat.leap.prm7, rec.10wat.leap.rst7 and rec.watbox.leap.prm7, rec.watbox.leap.rst7

