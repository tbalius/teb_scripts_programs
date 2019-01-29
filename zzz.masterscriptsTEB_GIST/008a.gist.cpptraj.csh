# TEB/ MF comments -- March2017

## This script runs GIST. It
# 1) calculates the c.o.m. of the aligned ligand to use those coords as gist box center
# 2) reads in all frames (1-5000) of each trajectory
# 3) makes a GIST box of 40x40x40 voxels with a gridspacing of 0.50A aka a box with the dimensions of 20A in xyz directions.
# 4) submits 1 job to queue and runs ccptraj (with input script we created)

set mountdir = `pwd`
set workdir  = $mountdir/gist/008a.full_gist
rm -rf $workdir
mkdir -p $workdir
cd $workdir

set jobId = "5609039"

ln -s ${mountdir}/MDrundir/MDrun/${jobId} .
ln -s ${mountdir}/gist/007align_to_md/lig_aligned.mol2 .

#copy scrips from web
curl http://docking.org/~tbalius/code/for_dock_3.7/mol2.py > mol2.py
curl http://docking.org/~tbalius/code/for_dock_3.7/mol2_center_of_mass.py > mol2_center_of_mass.py

python ./mol2_center_of_mass.py lig_aligned.mol2 centermol.txt

set center = `cat centermol.txt`


#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
## reads in trajectories from 1 to 5000 (10k is picked since > 5000).
cat << EOF >! gist.in
#parm rec.watbox.leap.prm7 
parm ${jobId}/rec.watbox.leap.prm7
trajin ${jobId}/09md.mdcrd 1 10000
trajin ${jobId}/10md.mdcrd 1 10000
trajin ${jobId}/11md.mdcrd 1 10000  
trajin ${jobId}/12md.mdcrd 1 10000 
trajin ${jobId}/13md.mdcrd 1 10000 
trajin ${jobId}/14md.mdcrd 1 10000 
trajin ${jobId}/15md.mdcrd 1 10000 
trajin ${jobId}/16md.mdcrd 1 10000 
trajin ${jobId}/17md.mdcrd 1 10000
trajin ${jobId}/18md.mdcrd 1 10000
gist doorder gridcntr ${center} griddim 40 40 40 gridspacn 0.50 
go
EOF
#gist doorder doeij gridcntr 35.759163 33.268703 31.520596 griddim 40 40 40 gridspacn 0.50 out gist.out


#ln -s ../*.mdcrd .
#ln -s ../rec_h.wat.leap.prm7 .

cat << EOF > qsub_fullgist.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q all.q
#\$ -o stdout
#\$ -e stderr

cd $workdir

/nfs/soft/amber/amber14/bin/cpptraj -i gist.in > ! gist.log 

EOF

qsub qsub_fullgist.csh

#/nfs/soft/amber/amber14/bin/cpptraj -i gist.in > ! gist.log &

