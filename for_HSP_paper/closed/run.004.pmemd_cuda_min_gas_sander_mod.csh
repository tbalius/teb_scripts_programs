#setenv AMBERHOME /nfs/soft/amber/amber14


set username = `whoami`
#setenv AMBERHOME /nfs/soft/amber/amber14
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"
#setenv LD_LIBRARY_PATH "/nfs/soft/cuda-6.5/lib64/:\$LD_LIBRARY_PATH"

#set pdb = "5VBE"
#mkdir ${pdb}/004.min
#cd ${pdb}/004.min
set pwd = `pwd`
set mol2file = "" 
set workdir = ${pwd}/${mol2file}/0004.min_gas_sander_mod
mkdir ${workdir}
cd ${workdir}

cp ../0003md_tleap/com1.mmrc.leap.* . 

cat << EOF1 > ! 01mi.in
01mi.in: minimization with GAS
&cntrl
 imin = 1, maxcyc = 100, ncyc = 100,  ntmin = 1,
 igb=6,
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

#cd $pwd

#echo "running: sinfo -p gpu"

#sinfo -p gpu

#echo cn072

#SBATCH --nodelist=cn051
#SBATCH -p gpu
#SBATCH --gres=gpu:1
# source ${pwd}/pickGPU.csh
# echo \${CUDA_VISIBLE_DEVICES}
#  $AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com1.mmrc.leap.prm7 -c com1.mmrc.leap.rst7 -ref com1.mmrc.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7
cat << EOF > ! qsub.sander.csh
#!/bin/tcsh
#SBATCH -t 48:00:00
#SBATCH --output=stdout

  cd ${workdir}
  
  /home/${username}/zzz.programs/amber/amber20_src/bin_mod/sander -O -i 01mi.in -o 01mi.out -p com1.mmrc.leap.prm7 -c com1.mmrc.leap.rst7 -ref com1.mmrc.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

EOF

  sbatch qsub.sander.csh 
