#!/bin/csh


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 
set amberexe = "$AMBERHOME/bin/sander"

#set pwd = `pwd`

#set seed = "0"
#set seed = "5"
#set seed = "50"
#set seed = "500"
#set seed = "no_restaint_0"

foreach seed ( \
 "0"       \
 "5"       \
 "50"      \
 "500"     \
)

#set ligori = ${lig}
#set lig = ${lig}_${seed}

#set com_parm = ${pwd}/003md_tleap/com.nowat.leap.prm7
#set com_crd  = ${pwd}/003md_tleap/com.nowat.leap.rst7
set com_parm = ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
set com_crd  = ${mountdir_ori}/0003md_tleap/com4.mm.leap.rst7

set rec_parm = ${mountdir_ori}/0003md_tleap/com5.m1.leap.prm7
set rec_crd  = ${mountdir_ori}/0003md_tleap/com5.m1.leap.rst7

set lig_parm = ${mountdir_ori}/0003md_tleap/com6.m2.leap.prm7
set lig_crd  = ${mountdir_ori}/0003md_tleap/com6.m2.leap.rst7


set TASK_DIR = "${mountdir}/008_mmgbsa/full_${seed}"

#if (-e ${TASK_DIR}) then
#   echo "${TASK_DIR} exists. continue..."
#   continue
#endif

mkdir -p ${TASK_DIR}
cd ${TASK_DIR}

#cp /home/baliuste/work/RAS/dimer_6GJ8/003md_tleap/com.watbox.leap.* .

set com_traj = ${mountdir}/007.com.dimer_${seed}/com.nowat.mdcrd 
set rec_traj = ${mountdir}/007.com.dimer_${seed}/hsp83_mon1.mdcrd 
set lig_traj = ${mountdir}/007.com.dimer_${seed}/hsp83_mon2.mdcrd

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
/
EOF1


  ln -s ${lig_parm} ./lig.prm7
  ln -s ${lig_crd}  ./lig.crd
  ln -s ${lig_traj} ./lig.mdcrd

  ln -s ${rec_parm} ./rec.prm7
  ln -s ${rec_crd}  ./rec.crd
  ln -s ${rec_traj} ./rec.mdcrd

  ln -s ${com_parm} ./com.prm7
  ln -s ${com_crd}  ./com.crd
  ln -s ${com_traj} ./com.mdcrd

cat << EOF2 > ! mmgbsa_cal_lig.csh
#!/bin/tcsh
#SBATCH -t 72:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_lig.out -p lig.prm7 -c lig.crd -y lig.mdcrd 
EOF2

cat << EOF3 > ! mmgbsa_cal_rec.csh
#!/bin/tcsh
#SBATCH -t 72:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_rec.out -p rec.prm7 -c rec.crd -y rec.mdcrd 
EOF3

cat << EOF4 > ! mmgbsa_cal_com.csh
#!/bin/tcsh
#SBATCH -t 72:00:00
#SBATCH --output=stdout
  cd ${TASK_DIR}
  $amberexe -O -i mmgbsa_cal.in -o mmgbsa_cal_com.out -p com.prm7 -c com.crd -y com.mdcrd 
EOF4



#exit#sbatch mmgbsa_cal_com.csh 
sbatch mmgbsa_cal_com.csh 
sbatch mmgbsa_cal_rec.csh
sbatch mmgbsa_cal_lig.csh 

#end # subtraj
#end # lig in complex
end #seed 
