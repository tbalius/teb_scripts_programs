

#!/bin/csh/prepdir
# This script uses first reduce and then tleap to prepare a receptor for amber.
# The outputs are: parameter topology file (prm7) and a coordinate file (rst7) 
#
# Written by Trent balius
# TEB/ MF comments Feb2017

setenv AMBERHOME /home/baliuste/zzz.programs/amber/amber18
setenv DOCKBASE "/home/baliuste/zzz.github/DOCK"
# CUDA for GPU
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

#set pdb = "5VBE"
set mountdir_ori = `pwd`

  set mut = E37C 
  #set lig = DL2040 
  #set lig = DL2078 
  set lig = DL1314_Protomer1 
  foreach pose (   \
                 1 \
                 2 \
                 3 \
   )

set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
set filedir = $mountdir/0001.pdb_files  ## modify this line!
set parmdir = $mountdir/001_files  ## modify this line!
#set prepdir = $mountdir/002_gtp_prep  ## modify this line!
#set workdir = $mountdir/\${pdb}/003md_tleap
set workdir = $mountdir/003md_tleap
#set workdir = $mountdir/003md_tleap_new
set scriptdir = /home/baliuste/zzz.github/teb_scripts_programs/zzz.scripts 

# copy over disulfide parameters. 
cp -r ${mountdir_ori}/../D153C/DL00329/pose1/001_files/ $mountdir

#set resnum = " 37" 
set resnum = " 38" 
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

#rm -f leap.log  tleap.rec.out tleap.rec.in

## uncomment the next line to include Xtal waters into simulation
#cp $filedir/nearby_waters_aligned.pdb water.pdb
#cp $filedir/5VBE/prep/rec.pdb rec.pdb
#cat $mountdir/5VBE/prep/rec.pdb | grep -v '^.............................................................................H' | grep -v " MG "  > rec.ori.pdb
#cat $mountdir/rosetta_build_loop/rec_loop_add_loop_0001_man.pdb | grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb

#cat $mountdir/rosetta_build_loop/rec_loop_add_loop_0001_man.pdb | grep " MG " > ion.pdb 

#cat $mountdir/5VBE/lig.2.pdb | grep "HETATM" | sed -e 's/HETATM/ATOM  /g' -e 's/92V/LIG/g' | grep -v '^.............................................................................H'   > lig.pdb
#cat $filedir/rec.pdb | grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb
#cat $filedir/rec.pdb | sed -e "s/CD  ILE/CD1 ILE/g" -e "s/OT1/O  /g" -e "s/OT2/OXT/g"| grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb

cp $filedir/rec.pdb .
cat $filedir/ion.pdb | grep " MG " > ion.pdb 

cat $filedir/lig.pdb | grep "HETATM" | sed -e 's/HETATM/ATOM  /g' -e 's/UNK/LIG/g' | grep -v '^.............................................................................H'   > lig.pdb
#cp $filedir/lig.pdb .
#
#sed -i 's/UNK/LIG/g' lig.pdb

#cat $filedir/lig.pdb | sed -e "s/CL1/Cl1/g" -e "s/CL2/Cl2/g" | grep "HETATM" | sed -e 's/HETATM/ATOM  /g' -e 's/UNK/LIG/g' | grep -v '^.............................................................................H'   > lig.pdb

#cp ../wat.pdb .
#cp ../mg2_wat.pdb .
#cp ../mg2.pdb .
#cp ../wat2.pdb .
#python $scriptdir/add.ters.py rec.ori.pdb rec.pdb
#echo "TER" >> rec.pdb
#cat $mountdir/5VBE/prep/rec.pdb | grep " MG " >> rec.pdb 

# 1st: run leap to renumber residues.

# produces tleap input file -- renumbers rec
cat << EOF >! tleap.rec.1.in 
set default PBradii mbondi2
# load the protein force field

source leaprc.protein.ff14SB
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

#cp rec.nowat.3ter.pdb rec.nowat.final.pdb
#
#sed -i "s/ATOM   5004 MG /TER\nATOM   5004 MG /g" rec.nowat.3ter.pdb 

# add TER to file rec.nowat.H_mod2.pdb before HEM
#grep -v "HEM" rec.nowat.H_mod3.pdb >! rec.nowat.H_mod4.pdb
#echo "TER" >> rec.nowat.H_mod4.pdb
#grep "HEM" rec.nowat.H_mod2.pdb >> rec.nowat.H_mod4.pdb
#mv rec.nowat.H_mod3.pdb rec.nowat.H_final.pdb
#mv rec.nowat.3ter.pdb rec.nowat.final.pdb

#cat rec.nowat.3ter.pdb | sed -e 's/CYS    69/CYX    69/g' | grep -v "HG  CYX    69" > rec.nowat.final.pdb
#cat rec.nowat.3ter.pdb | sed -e 's/CYS    ${resnum}/CYX    ${resnum}/g' | grep -v "HG  CYX    ${resnum}" > rec.nowat.final.pdb

python $scriptdir/which_cys_to_lig.py rec.nowat.3ter.pdb lig.pdb rec.lig.ssbond

# add this function to script: 
#cat rec.nowat.3ter.pdb | sed -e 's/CYS   '${resnum}'/CYX   '${resnum}'/g' | grep -v "HG  CYX   ${resnum}" > rec.nowat.final.pdb
#cat rec.nowat.3ter.pdb | sed -e  "s/CYS   ${resnum}/CYX   ${resnum}/g" |     grep -v "HG  CYX   ${resnum}" > rec.nowat.final.pdb

# add this function to script:
 cat rec.nowat.3ter.pdb | sed -e "s/CYS   ${resnum}/CYX   ${resnum}/g" | grep -v "HG  CYX   ${resnum}" > rec.nowat.final.pdb
#

# produces tleap input file in 3 steps, first script based instruction file (loading FF and rec file), then pipes disulphide info into middle and final instructions (write just rec, solvated in TIP3P water box of 10A about rec boundaries, write rec in water-box parameters and coordinates) for complete tleap input file
#loadamberparams ${parmdir}/disulfide.frcmod
cat << EOF >! tleap.rec.in 

set default PBradii mbondi2
# load the protein force field
source leaprc.protein.ff14SB
source leaprc.water.tip3p
source leaprc.gaff2
# load ions
loadAmberParams frcmod.ions234lm_1264_tip3p

# load ligand and covalent parameters.  

loadamberparams ${parmdir}/disulfide.frcmod
loadamberparams ${mountdir}//002_lig_prep/lig.ante.charge.frcmod
loadamberparams ${mountdir}/002_cof_prep/lig.ante.charge_man_mod.frcmod


loadamberprep ${mountdir}/002_lig_prep/lig.ante.charge_mod.prep
loadamberprep ${mountdir}/002_cof_prep/lig.ante.charge.prep



REC = loadpdb rec.nowat.final.pdb
LIG = loadpdb ./lig.pdb
#LIG = loadpdb ${mountdir}/002_lig_prep/lig.ante.pdb
COF = loadpdb ${mountdir}/002_cof_prep/lig.ante.pdb
ION = loadpdb ion.pdb 
EOF

if (-e rec.nowat.2cys.pdb.for.leap ) then
  cat rec.nowat.2cys.pdb.for.leap >> tleap.rec.in
endif

cat << EOF >> tleap.rec.in
COM = combine {REC LIG COF ION} 
RE2 = combine {REC COF ION} 


EOF

cat rec.lig.ssbond.for.leap >> tleap.rec.in

cat << EOF >> tleap.rec.in

saveamberparm COM com.leap.prm7 com.leap.rst7
saveamberparm RE2 rec.leap.prm7 rec.leap.rst7
saveamberparm LIG lig.leap.prm7 lig.leap.rst7
solvateBox COM TIP3PBOX 10.0
saveamberparm COM com.watbox.leap.prm7 com.watbox.leap.rst7
quit
EOF

$AMBERHOME/bin/tleap -s -f tleap.rec.in > ! tleap.rec.out

# for ease of visualization in pymol 
$AMBERHOME/bin/ambpdb -p com.leap.prm7 < com.leap.rst7 > com.leap.pdb

$AMBERHOME/bin/ambpdb -mol2 -p com.leap.prm7 < com.leap.rst7 > com.leap.mol2

echo "Look at com.leap.pdb in pymol. May have to delete last column in pdb file for pymol. "
# may have to remove element column so pymol does not get confused
#

# inspect tleap.rec.out and the leap.log file
# visually inspect (VMD) rec.10wat.leap.prm7, rec.10wat.leap.rst7 and rec.watbox.leap.prm7, rec.watbox.leap.rst7
end # poses
