
#setenv AMBERHOME /nfs/soft/amber/amber14

setenv AMBERHOME /nfs/soft/amber/amber14
setenv LD_LIBRARY_PATH ""
setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

cat << EOF1 > ! 01mi.in
01mi.in: minimization with GB
&cntrl
 imin = 1, maxcyc = 10000, ncyc = 500,  ntmin = 1,
 igb=1,
 ntx = 1, ntc = 1, ntf = 1,
 ntb = 0, ntp = 0,
 ntwx = 1000, ntwe = 0, ntpr = 1000,
 cut = 999.9,
 ntr = 1,
 restraintmask = '!@H=', 
 restraint_wt = 0.1,
/
EOF1


cat << EOF2 > ! 02mi.in
01mi.in: minimization with GB
&cntrl
 imin = 1, maxcyc = 10000, ncyc = 500,  ntmin = 1,
 igb=1,
 ntx = 1, ntc = 1, ntf = 1,
 ntb = 0, ntp = 0,
 ntwx = 1000, ntwe = 0, ntpr = 1000,
 cut = 999.9,
 ntr = 1,
 restraintmask = '@CA', 
 restraint_wt = 0.1,
/
EOF2


#$AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

set pwd = `pwd`
#cd $pwd

cat << EOF > ! qsub.pmemd.cuda.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q gpu.q
#\$ -o stdout
#\$ -e stderr

  cd $pwd
  $AMBERHOME/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

  $AMBERHOME/bin/pmemd.cuda -O -i 02mi.in -o 02mi.out -p com.leap.prm7 -c 01mi.rst7 -ref 01mi.rst7 -x 02mi.mdcrd -inf 02mi.info -r 02mi.rst7
EOF

  qsub qsub.pmemd.cuda.csh 
