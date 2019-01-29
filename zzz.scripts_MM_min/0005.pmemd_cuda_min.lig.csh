
#setenv AMBERHOME /nfs/soft/amber/amber14

setenv AMBERHOME /nfs/soft/amber/amber14
setenv LD_LIBRARY_PATH ""
setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

cat << EOF1 > ! 01mi.lig.in
01mi.in: minimization with GB
&cntrl
 imin = 1, maxcyc = 10000, ncyc = 500,  ntmin = 1,
 igb=1,
 ntx = 1, ntc = 1, ntf = 1,
 ntb = 0, ntp = 0,
 ntwx = 1000, ntwe = 0, ntpr = 1000,
 cut = 999.9,
 ntr = 0,
/
EOF1
#restraintmask = '!@H=', 
#restraint_wt = 0.1,


#$AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

set pwd = `pwd`
#cd $pwd

cat << EOF > ! qsub.pmemd.cuda.lig.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q gpu.q 
#\$ -o stdout
#\$ -e stderr

  cd $pwd
  $AMBERHOME/bin/pmemd.cuda -O -i 01mi.lig.in -o 01mi.lig.out -p lig.leap.prm7 -c lig.leap.rst7 -ref lig.leap.rst7 -x 01mi.lig.mdcrd -inf 01mi.lig.info -r 01mi.lig.rst7

EOF

  qsub qsub.pmemd.cuda.lig.csh 
