#setenv AMBERHOME /nfs/soft/amber/amber14

#setenv AMBERHOME /nfs/soft/amber/amber14
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"
#setenv LD_LIBRARY_PATH "/nfs/soft/cuda-6.5/lib64/:\$LD_LIBRARY_PATH"

#source ~baliuste/.bashrc.amber 

#set pdb = "5VBE"
#mkdir ${pdb}/004.min
#cd ${pdb}/004.min
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
set pwd = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $pwd

mkdir 004.min
cd 004.min

cp ../003md_tleap/com.leap.* . 

cat << EOF1 > ! 01mi.in
01mi.in: minimization with GB/SA
&cntrl
 imin = 1, maxcyc = 10000, ncyc = 500,  ntmin = 1,
 igb=1, gbsa=1,
 ntx = 1, ntc = 1, ntf = 1,
 ntb = 0, ntp = 0,
 ntwx = 1000, ntwe = 0, ntpr = 1000,
 cut = 999.9,
 ntr = 1,
 restraintmask = '!@H=', 
 restraint_wt = 0.1,
/
EOF1


#$AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7
#$AMBERHOME/bin/sander -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

set pwd = `pwd`
#cd $pwd

#echo "running: sinfo -p gpu"

#sinfo -p gpu

#echo cn072

#SBATCH --nodelist=cn049
#SBATCH --nodelist=cn050
#SBATCH --nodelist=cn051
#SBATCH --nodelist=cn052
#SBATCH --nodelist=cn072
#SBATCH --nodelist=cn073
#SBATCH --nodelist=cn076
#SBATCH --nodelist=cn051
cat << EOF > ! qsub.sander.csh
#!/bin/tcsh
#SBATCH -t 48:00:00
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH --output=stdout

  source ${mountdir_ori}/pickGPU.csh
  echo \${CUDA_VISIBLE_DEVICES}
  cd $pwd
  
  $AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

EOF

  sbatch qsub.sander.csh 

end # poses
