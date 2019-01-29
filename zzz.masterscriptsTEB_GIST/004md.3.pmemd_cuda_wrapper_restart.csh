

#foreach num ("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
#foreach num ("1" "2" "3" "4" "5" "6" "7" )

set pwd = `pwd`
#set oldjobid = "2805311"
set oldjobid = "5470171"	### CHANGE THIS to old jobID

### CHANGE THIS 
#set restart = "$pwd/$oldjobid/08md.rst7"
set restart = "$pwd/$oldjobid/10md.rst7"
set ref     = "$pwd/$oldjobid/07.2md.rst7"
set input   = "$pwd/$oldjobid/09md.in"
set parm    = ${pwd}/rec_h.wat.leap.prm7 

#\$ -q gpu.q@n-1-126
#\$ -q gpu.q@n-1-141
cat << EOF >! qsub.amber.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q gpu.q@n-1-126
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

cp ${parm} .
cp ${restart} .
cp ${ref} .
cp ${input} .

cat 09md.in | sed 's/09md/11md/g' | sed 's/34567/111/g'     > 11md.in
cat 09md.in | sed 's/09md/12md/g' | sed 's/34567/2121212/g' > 12md.in
cat 09md.in | sed 's/09md/13md/g' | sed 's/34567/131313/g'  > 13md.in
cat 09md.in | sed 's/09md/14md/g' | sed 's/34567/4443/g'    > 14md.in

set pwd = `pwd`

  # stat production    ### CHANGE THIS as necessary
  
#  \$amberexe -O -i 09md.in -o 09md.out -p ${parm} \
#  -c 08md.rst7 -ref 07.2md.rst7 -x 09md.mdcrd -inf 09md.info -r 09md.rst7
  
#  \$amberexe -O -i 10md.in -o 10md.out -p ${parm} \
#  -c 09md.rst7 -ref 07.2md.rst7 -x 10md.mdcrd -inf 10md.info -r 10md.rst7
  
  \$amberexe -O -i 11md.in -o 11md.out -p ${parm} \
  -c 10md.rst7 -ref 07.2md.rst7 -x 11md.mdcrd -inf 11md.info -r 11md.rst7
  
  \$amberexe -O -i 12md.in -o 12md.out -p ${parm} \
  -c 11md.rst7 -ref 07.2md.rst7 -x 12md.mdcrd -inf 12md.info -r 12md.rst7

  \$amberexe -O -i 13md.in -o 13md.out -p ${parm} \
  -c 12md.rst7 -ref 07.2md.rst7 -x 13md.mdcrd -inf 13md.info -r 13md.rst7

  \$amberexe -O -i 14md.in -o 14md.out -p ${parm} \
  -c 13md.rst7 -ref 07.2md.rst7 -x 14md.mdcrd -inf 14md.info -r 14md.rst7

mv \$TASK_DIR $pwd 

EOF

qsub qsub.amber.csh 

