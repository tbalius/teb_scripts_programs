#!/bin/csh
# This script uses first reduce and then tleap to prepare a receptor for amber.
# The outputs are: parameter topology file (prm7) and a coordinate file (rst7) 
#
## it includes the option to include Xtal waters (currently commented out)
#
# Written by Trent balius
# TEB/ MF comments Feb2017

setenv AMBERHOME /nfs/soft/amber/amber14
setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK"
# CUDA for GPU
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

set mountdir = `pwd`
set filedir = $mountdir/MDrundir/prep/002md_align
set workdir = $mountdir/MDrundir/prep/003md_tleap

# check if workdir exists
if ( -s $workdir ) then
   echo "$workdir exits"
   continue
endif
       
# if it exists do this:     rm -rf ${workdir}
mkdir -p ${workdir}
cd ${workdir}

#rm -f leap.log  tleap.rec.out tleap.rec.in

## uncomment the next line to include Xtal waters into simulation
#cp $filedir/nearby_waters_aligned.pdb wat.pdb
cp $filedir/apo_ref.pdb rec.pdb

# get HEME parameters
curl docking.org/~tbalius/code/waterpaper2017/parms/frcmod_teb_mf_mod.hemall > frcmod_teb_mf_mod.hemall
curl docking.org/~tbalius/code/waterpaper2017/parms/heme_all_plus1.in > heme_all_plus1.in

### 1st: run leap just to renumber residues.

# produces tleap input file -- renumbers rec
### draw bond between HIS and HEME with 5 coordinated iron.
##bond REC.175.NE2 REC.293.FE
cat << EOF >! tleap.rec.1.in 
set default PBradii mbondi2
# load the protein force field
source leaprc.ff14SB
loadamberparams frcmod_teb_mf_mod.hemall
loadamberprep heme_all_plus1.in
REC = loadpdb rec.pdb
saveamberparm REC rec.1.leap.prm7 rec.1.leap.rst7
quit
EOF

# runs tleap and converts parameter and coordinate restart file back into pdb file
$AMBERHOME/bin/tleap -s -f tleap.rec.1.in > ! tleap.rec.1.out
$AMBERHOME/bin/ambpdb -p rec.1.leap.prm7 < rec.1.leap.rst7 >! rec.1.leap.pdb 

# nomenclature clean-up
$DOCKBASE/proteins/Reduce/reduce -HIS -FLIPs rec.1.leap.pdb >! rec.nowat.reduce.pdb
sed -i 's/HETATM/ATOM  /g' rec.nowat.reduce.pdb 
# grep -v means "everything but"; last grep statement removes inconsistently named HEM hydrogens (for leap to be added back in)
grep "^ATOM  " rec.nowat.reduce.pdb | sed -e 's/   new//g' | sed 's/   flip//g' | sed 's/   std//g' | grep -v "OXT" | grep -v " 0......HEM" >! rec.nowat.reduce_clean.pdb


curl docking.org/~tbalius/code/waterpaper2017/scripts/replace_his_with_hie_hid_hip.py > replace_his_with_hie_hid_hip.py
curl docking.org/~tbalius/code/waterpaper2017/scripts/replace_cys_to_cyx.py > replace_cys_to_cyx.py
curl docking.org/~tbalius/code/waterpaper2017/scripts/add.ters.py > add.ters.py

# python scripts do these three things: 1) checks his to give protonation specific names; 2) checks for disulphide bonds; 3) checks for missing residues and adds TER flag
python replace_his_with_hie_hid_hip.py rec.nowat.reduce_clean.pdb rec.nowat.1his.pdb
python replace_cys_to_cyx.py rec.nowat.1his.pdb rec.nowat.2cys.pdb
python add.ters.py rec.nowat.2cys.pdb rec.nowat.3ter.pdb

# add TER to file rec.nowat.H_mod2.pdb before HEM
grep -v "HEM" rec.nowat.3ter.pdb >! rec.nowat.4ter.pdb
echo "TER" >> rec.nowat.4ter.pdb
grep "HEM" rec.nowat.3ter.pdb >> rec.nowat.4ter.pdb

# fix wrong his protonation from automated pipeline 
grep -v "HE2 HIE   172" rec.nowat.4ter.pdb | sed -e "s/HIE   172/HID   172/g" > rec.nowat.final.pdb

# if no histidine fix is required uncomment this
#mv rec.nowat.3ter.pdb rec.nowat.final.pdb
# or rec.nowat.4ter.pdb rec.nowat.final.pdb if TER was added before the heme


### 2nd -- re-run tleap to create amber-ready input files (solvated parameter and coordinate protein and instruction file)

# produces tleap input file in 3 steps, first script based instruction file (loading FF and rec file), then pipes disulphide info into middle and final instructions (write just rec, solvated in TIP3P water box of 10A about rec boundaries, write rec in water-box parameters and coordinates) for complete tleap input file
cat << EOF >! tleap.rec2.in 
set default PBradii mbondi2
# load the protein force field
source leaprc.ff14SB
loadamberparams frcmod_teb_mf_mod.hemall
loadamberprep heme_all_plus1.in
REC = loadpdb rec.nowat.final.pdb
EOF

if (-e rec.nowat.2cys.pdb.for.leap ) then 
  cat rec.nowat.2cys.pdb.for.leap >> tleap.rec2.in
endif

cat << EOF >> tleap.rec2.in
# draw bond between HIS and HEME
# 5 coordinated iron.
bond REC.172.NE2 REC.290.FE
## include the following two lines to include Xtal water in MD run
##  XTALWAT = loadpdb wat.pdb
##  RECWAT  = combine {REC XTALWAT}
## also need to change REC to RECWAT in the next 3 lines
saveamberparm REC rec.leap.prm7 rec.leap.rst7
solvateBox REC TIP3PBOX 10.0
saveamberparm REC rec.watbox.leap.prm7 rec.watbox.leap.rst7
quit
EOF

$AMBERHOME/bin/tleap -s -f tleap.rec2.in > ! tleap.rec2.out

# for ease of visualization in pymol 
$AMBERHOME/bin/ambpdb -p rec.leap.prm7 < rec.leap.rst7 > rec.leap.pdb

echo "Look at rec.leap.pdb in pymol. May have to delete last column in pdb file for pymol."
# may have to remove element column so pymol does not get confused

# inspect tleap.rec.out and the leap.log file
# visually inspect (VMD) rec.10wat.leap.prm7, rec.10wat.leap.rst7 and rec.watbox.leap.prm7, rec.watbox.leap.rst7
