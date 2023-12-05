#!/bin/csh

set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 
set amberexe = "$AMBERHOME/bin/sander"

#set seed = "0"
#set seed = "5"
#set seed = "50"
#set seed = "500"
#set seed = "no_restaint_0"

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
 "500"    \
)

foreach chunk ( \
 09md \
 10md \
 11md \
 12md \
 13md \
 14md \
 15md \
 16md \
 17md \
 18md \
)

# one
set mmrc_parm = ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
set mmrc_crd  = ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.rst7

#two
set raf_parm = ${mountdir_ori}/0003md_tleap/raf2.leap.prm7
set raf_crd  = ${mountdir_ori}/0003md_tleap/raf2.leap.rst7

# three
set mmc_parm = ${mountdir_ori}/0003md_tleap/com3.mmc.leap.prm7
set mmc_crd  = ${mountdir_ori}/0003md_tleap/com3.mmc.leap.rst7

# four
set mm_parm = ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
set mm_crd  = ${mountdir_ori}/0003md_tleap/com4.mm.leap.rst7

# five
set m1_parm = ${mountdir_ori}/0003md_tleap/com5.m1.leap.prm7
set m1_crd  = ${mountdir_ori}/0003md_tleap/com5.m1.leap.rst7

# six
set m2_parm = ${mountdir_ori}/0003md_tleap/com6.m2.leap.prm7
set m2_crd  = ${mountdir_ori}/0003md_tleap/com6.m2.leap.rst7

# seven 
set rc_parm = ${mountdir_ori}/0003md_tleap/com7.rc.leap.prm7
set rc_crd  = ${mountdir_ori}/0003md_tleap/com7.rc.leap.rst7

set TASK_DIR = "${mountdir}/0008_mmgbsa_chunk/full_${seed}/${chunk}"

if (-e ${TASK_DIR}) then
   echo "${TASK_DIR} exists. continue..."
   continue
endif

mkdir -p ${TASK_DIR}
cd ${TASK_DIR}
pwd

set mmrc_traj = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/com.1.${chunk}.nowat.mdcrd
set raf_traj  = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/raf.2.${chunk}.mdcrd
set mmc_traj  = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/com.3.${chunk}.mmc.mdcrd
set mm_traj   = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/com.4.${chunk}.mm.mdcrd
set m1_traj   = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/m1.5.${chunk}.mdcrd
set m2_traj   = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/m2.6.${chunk}.mdcrd
set rc_traj   = ${mountdir}/0007.com.rec.lig_${seed}_chunk/${chunk}/com.7.${chunk}.rc.mdcrd

## parameters to add if writing NetCDF -- for production run not visualization (VMD)
# ioutfm=1, # write out NetCDF trajectory
# ntxo = 2, # write out NetCDF restart
# ntrx = 2, # read in NetCDF restart
## we didn't because VMD does not read it in (NetCDF is small in size and has more significant figures).


## equilibration run 01mi-02mi and 01md-08md (see details in comments below)
## production run starts at 09md

## 01mi and 02mi minimize all Hs and waters, restraint in kcal/mol/A^2
cat << EOF1 > ! mmgbsa_cal.in
mmgbsa_cal.in: GBSA single point caclculations.
&cntrl
   imin=5, maxcyc=1,
   ntb=0
   ntpr=1,
   cut=9999.0,
   igb=5,
   gbsa=2,
   surften=1.0,
/
EOF1


  ln -s ${mmrc_parm} ./mmrc.prm7
  ln -s ${mmrc_crd}  ./mmrc.crd
  ln -s ${mmrc_traj} ./mmrc.mdcrd

cat << EOF2 > ! mmgbsa_cal_mmrc.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_mmrc.out -p mmrc.prm7 -c mmrc.crd -y mmrc.mdcrd 
EOF2

  ln -s ${raf_parm} ./raf.prm7
  ln -s ${raf_crd}  ./raf.crd
  ln -s ${raf_traj} ./raf.mdcrd

cat << EOF3 > ! mmgbsa_cal_raf.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_raf.out -p raf.prm7 -c raf.crd -y raf.mdcrd 
EOF3

  ln -s ${mmc_parm} ./mmc.prm7
  ln -s ${mmc_crd}  ./mmc.crd
  ln -s ${mmc_traj} ./mmc.mdcrd

cat << EOF4 > ! mmgbsa_cal_mmc.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_mmc.out -p mmc.prm7 -c mmc.crd -y mmc.mdcrd 
EOF4

  ln -s ${mm_parm} ./mm.prm7
  ln -s ${mm_crd}  ./mm.crd
  ln -s ${mm_traj} ./mm.mdcrd

cat << EOF5 > ! mmgbsa_cal_mm.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_mm.out -p mm.prm7 -c mm.crd -y mm.mdcrd 
EOF5

  ln -s ${m1_parm} ./m1.prm7
  ln -s ${m1_crd}  ./m1.crd
  ln -s ${m1_traj} ./m1.mdcrd

cat << EOF6 > ! mmgbsa_cal_m1.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_m1.out -p m1.prm7 -c m1.crd -y m1.mdcrd 
EOF6

  ln -s ${m2_parm} ./m2.prm7
  ln -s ${m2_crd}  ./m2.crd
  ln -s ${m2_traj} ./m2.mdcrd

cat << EOF7 > ! mmgbsa_cal_m2.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_m2.out -p m2.prm7 -c m2.crd -y m2.mdcrd 
EOF7

  ln -s ${rc_parm} ./rc.prm7
  ln -s ${rc_crd}  ./rc.crd
  ln -s ${rc_traj} ./rc.mdcrd

cat << EOF8 > ! mmgbsa_cal_rc.csh
#!/bin/tcsh
#SBATCH -t 400:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_rc.out -p rc.prm7 -c rc.crd -y rc.mdcrd 
EOF8

sbatch mmgbsa_cal_mmrc.csh 
sbatch mmgbsa_cal_raf.csh
sbatch mmgbsa_cal_mmc.csh 
sbatch mmgbsa_cal_mm.csh 
sbatch mmgbsa_cal_m1.csh 
sbatch mmgbsa_cal_m2.csh 
sbatch mmgbsa_cal_rc.csh 

#end # subtraj
#end # lig in complex
end # chunks
end #seed 
#end # poses
