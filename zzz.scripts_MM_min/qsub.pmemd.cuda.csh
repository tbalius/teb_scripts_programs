#$ -S /bin/csh
#$ -cwd
#$ -q gpu.q
#$ -o stdout
#$ -e stderr

  cd /mnt/nfs/work/alevit/KOR/4DJH_inactive/4DJH_minimization
  /nfs/soft/amber/amber14/bin/pmemd.cuda -O -i 01mi.in -o 01mi.out -p com.leap.prm7 -c com.leap.rst7 -ref com.leap.rst7 -x 01mi.mdcrd -inf 01mi.info -r 01mi.rst7

  /nfs/soft/amber/amber14/bin/pmemd.cuda -O -i 02mi.in -o 02mi.out -p com.leap.prm7 -c 01mi.rst7 -ref 01mi.rst7 -x 02mi.mdcrd -inf 02mi.info -r 02mi.rst7
