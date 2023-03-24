#!/bin/csh

set amberexe = "$AMBERHOME/bin/sander"

#set pwd = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
set lig = DL2078 
#set lig = DL1314_Protomer1 

foreach pose (   \
#               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $mountdir
set pwd = $mountdir

#set seed = "0"
#set seed = "5"
#set seed = "50"
#set seed = "500"
#set seed = "no_restaint_0"

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
#"mod_0"  \
#"mod_5"  \
#"mod_50" \
)

#set ligori = ${lig}
#set lig = ${lig}_${seed}

#set com_parm = ${pwd}/003md_tleap/com.nowat.leap.prm7
#set com_crd  = ${pwd}/003md_tleap/com.nowat.leap.rst7
set com_parm = ${pwd}/003md_tleap/com.leap.prm7
set com_crd  = ${pwd}/003md_tleap/com.leap.rst7

set rec_parm = ${pwd}/003md_tleap/rec.leap.prm7
set rec_crd  = ${pwd}/003md_tleap/rec.leap.rst7

set lig_parm = ${pwd}/003md_tleap/lig.leap.prm7
set lig_crd  = ${pwd}/003md_tleap/lig.leap.rst7


set TASK_DIR = "${pwd}/008_mmgbsa/full_${seed}"

if (-e ${TASK_DIR}) then
   echo "${TASK_DIR} exists. continue..."
   continue
endif

mkdir -p ${TASK_DIR}
cd ${TASK_DIR}
pwd

#cp /home/baliuste/work/RAS/dimer_6GJ8/003md_tleap/com.watbox.leap.* .

set com_traj = ${pwd}/007.com.rec.lig_${seed}/com.nowat.mdcrd 
set rec_traj = ${pwd}/007.com.rec.lig_${seed}/rec.mdcrd 
set lig_traj = ${pwd}/007.com.rec.lig_${seed}/lig.mdcrd

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



#exit
sbatch mmgbsa_cal_com.csh 
sbatch mmgbsa_cal_rec.csh
sleep 5 
sbatch mmgbsa_cal_lig.csh 

#end # subtraj
#end # lig in complex
end #seed 
end # poses
