

#foreach num ("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
#foreach num ("1" "2" "3" "4" "5" "6" "7" )

set pwd = `pwd`

#2858833   	### CHANGE THIS according to jobID and file from which to extend
#set restart = "/mnt/nfs/work/tbalius/MOR/run_amber/2805311/08md.rst7"
#set restart = "/mnt/nfs/work/tbalius/MOR/run_amber/2807514/14md.rst7"
set restart = "$pwd/5601662/14md.rst7"
set ref     = "$pwd/5601662/07.2md.rst7"
set input   = "$pwd/5601662/09md.in"

#\$ -q gpu.q@n-1-126
#\$ -q gpu.q@n-1-141
#\$ -q gpu.q
cat << EOF >! qsub.amber.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q gpu.q
#\$ -o stdout
#\$ -e stderr

# export CUDA_VISIBLE_DEVICES="0,1,2,3" 
# setenv CUDA_VISIBLE_DEVICES "0,1,2,3"
setenv AMBERHOME /nfs/soft/amber/amber14/ 
set amberexe = "/nfs/ge/bin/on-one-gpu - \$AMBERHOME/bin/pmemd.cuda"

# make a local directory on the server to run calculations
#
set SCRATCH_DIR = /scratch
if ! (-d \$SCRATCH_DIR ) then
    SCRATCH_DIR=/tmp
endif
set username = `whoami`

set TASK_DIR = "\$SCRATCH_DIR/\${username}/\$JOB_ID"
echo \$TASK_DIR

mkdir -p \${TASK_DIR}
cd \${TASK_DIR}
pwd

cp ${pwd}/rec_h.wat.leap.* .
cp ${restart} .
cp ${ref} .
cp ${input} .

cat 09md.in | sed 's/09md/15md/g' | sed 's/34567/151515/g'  > 15md.in #35ns
cat 09md.in | sed 's/09md/16md/g' | sed 's/34567/161616/g'  > 16md.in
cat 09md.in | sed 's/09md/17md/g' | sed 's/34567/171717/g'  > 17md.in
cat 09md.in | sed 's/09md/18md/g' | sed 's/34567/181818/g'  > 18md.in #50ns

set pwd = `pwd`

  # stat production  	### CHANGE THIS to extend MD run 
  
  \$amberexe -O -i 15md.in -o 15md.out -p rec_h.wat.leap.prm7 \
  -c 14md.rst7 -ref 07.2md.rst7 -x 15md.mdcrd -inf 15md.info -r 15md.rst7

  \$amberexe -O -i 16md.in -o 16md.out -p rec_h.wat.leap.prm7 \
  -c 15md.rst7 -ref 07.2md.rst7 -x 16md.mdcrd -inf 16md.info -r 16md.rst7

  \$amberexe -O -i 17md.in -o 17md.out -p rec_h.wat.leap.prm7 \
  -c 16md.rst7 -ref 07.2md.rst7 -x 17md.mdcrd -inf 17md.info -r 17md.rst7

  \$amberexe -O -i 18md.in -o 18md.out -p rec_h.wat.leap.prm7 \
  -c 17md.rst7 -ref 07.2md.rst7 -x 18md.mdcrd -inf 18md.info -r 18md.rst7

mv \$TASK_DIR $pwd 

EOF

qsub qsub.amber.csh 

