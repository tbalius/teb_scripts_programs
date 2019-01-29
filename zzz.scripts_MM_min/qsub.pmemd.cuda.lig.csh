#$ -S /bin/csh
#$ -cwd
#$ -q gpu.q 
#$ -o stdout
#$ -e stderr

  cd /mnt/nfs/work/alevit/KOR/4DJH_inactive/4DJH_minimization
  /nfs/soft/amber/amber14/bin/pmemd.cuda -O -i 01mi.lig.in -o 01mi.lig.out -p lig.leap.prm7 -c lig.leap.rst7 -ref lig.leap.rst7 -x 01mi.lig.mdcrd -inf 01mi.lig.info -r 01mi.lig.rst7

