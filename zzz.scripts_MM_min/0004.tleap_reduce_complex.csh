#!/bin/csh
# This script uses first reduce and then tleap to prepare a receptor for amber.
# The outputs are: parameter topology file (prm7) and a coordinate file (rst7) 
# Written by Trent balius


setenv AMBERHOME /nfs/soft/amber/amber14
setenv LD_LIBRARY_PATH ""
setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

rm -f leap.log  tleap.rec.out tleap.rec.in

# run leap to renumber residues. 
#

# produces tleap input file
cat << EOF >! tleap.rec.1.in 
set default PBradii mbondi2
# load the protein force field
source leaprc.ff14SB

REC = loadpdb rec.pdb

saveamberparm REC rec.1.leap.prm7 rec.1.leap.rst7

quit
EOF

$AMBERHOME/bin/tleap -s -f tleap.rec.1.in > ! tleap.rec.1.out
$AMBERHOME/bin/ambpdb -p rec.1.leap.prm7 < rec.1.leap.rst7 >! rec.1.leap.pdb 

# requires script 0000 to be run first and align/ dir to be present
$DOCKBASE/proteins/Reduce/reduce -HIS -FLIPs rec.1.leap.pdb >! rec.nowat.H_mod.pdb
sed -i 's/HETATM/ATOM  /g' rec.nowat.H_mod.pdb 
grep "^ATOM  " rec.nowat.H_mod.pdb | sed -e 's/   new//g' | sed 's/   flip//g' | grep -v "OXT" | grep -v " 0......HEM" >! rec.nowat.H_mod1.pdb
# grep -v means "everything but"; last grep statement removes inconsistently named HEM hydrogens (for leap to be added back in)

#cp /nfs/home/tbalius/zzz.scripts/replace_his_with_hie_hid_hip.py .
python 0001i.replace_his_with_hie_hid_hip.py rec.nowat.H_mod1.pdb rec.nowat.H_mod2.pdb
python 0001i.replace_cys_to_cyx.py rec.nowat.H_mod2.pdb rec.nowat.H_mod3.pdb
#exit
#python 0001i.add.ters.py rec.nowat.H_mod3.pdb rec.nowat.H_mod4.pdb
python 0001i.add.ters_rm_ter_h.py rec.nowat.H_mod3.pdb rec.nowat.H_mod4.pdb


# add TER to file rec.nowat.H_mod2.pdb before HEM
#grep -v "HEM" rec.nowat.H_mod3.pdb >! rec.nowat.H_mod4.pdb
#echo "TER" >> rec.nowat.H_mod4.pdb
#grep "HEM" rec.nowat.H_mod2.pdb >> rec.nowat.H_mod4.pdb
mv rec.nowat.H_mod4.pdb rec.nowat.H_final.pdb
#mv rec.nowat.H_mod3.pdb rec.nowat.H_final.pdb

# produces tleap input file
cat << EOF >! tleap.rec.in 
set default PBradii mbondi2
# load the protein force field
source leaprc.ff14SB
# load in GAFF
source leaprc.gaff
loadamberparams lig/lig.ante.charge.frcmod
loadamberprep lig/lig.ante.charge.prep

REC = loadpdb rec.nowat.H_final.pdb
WAT = loadpdb waters.pdb
LIG = loadpdb lig/lig.ante.pdb 
COM  = combine {REC LIG WAT} 
EOF

cat rec.nowat.H_mod3.pdb.for.leap >> tleap.rec.in

cat << EOF >> tleap.rec.in

saveamberparm COM com.leap.prm7 com.leap.rst7
solvateBox COM TIP3PBOX 10.0
saveamberparm COM com.watbox.leap.prm7 com.watbox.leap.rst7

quit
EOF


$AMBERHOME/bin/tleap -s -f tleap.rec.in > ! tleap.rec.out

# inspect tleap.rec.out and the leap.log file
# visually inspect (VMD) rec.10wat.leap.prm7, rec.10wat.leap.rst7 and rec.watbox.leap.prm7, rec.watbox.leap.rst7
