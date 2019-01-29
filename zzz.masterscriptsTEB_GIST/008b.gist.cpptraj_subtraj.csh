# TEB/ MF comments -- March2017

## This script does the same as 008a but for each individual subtrajectory.
## Run this after you started the 008a script since that takes much longer. Then submit 008b.
## When these runs finish - look at the results and if sth is wrong qdel the full gist run if necessary.

# 1) calculates the c.o.m. of the aligned ligand to use those coords as gist box center
# 2) for each individual subtrajectory -- reads in all frames and saves output to separate subdirectory within "008b.subtraj_gist/$subtraj"
# 3) makes a GIST box of 40x40x40 with a gridspacing of 0.50A aka 20A in xyz
# 4) submits all individual subtraj jobs to the queue and runs ccptraj (with input script we created)

set mountdir = `pwd`

foreach subtraj ( \
  09md \
  10md \
  11md \
  12md \
  13md \
  14md \
  15md \
  16md \
  17md \
  18md \
)

set workdir  = $mountdir/gist/008b.subtraj_gist/$subtraj

rm -rf $workdir
mkdir -p $workdir
cd $workdir

set jobId = "5609039"

ln -s ${mountdir}/MDrundir/MDrun/${jobId} . # for subtraj we could make links to two files insted of the directory
ln -s ${mountdir}/gist/007align_to_md/lig_aligned.mol2 .

#copy scrips from web
curl http://docking.org/~tbalius/code/for_dock_3.7/mol2.py > mol2.py
curl http://docking.org/~tbalius/code/for_dock_3.7/mol2_center_of_mass.py > mol2_center_of_mass.py

python ./mol2_center_of_mass.py lig_aligned.mol2 centermol.txt

set center = `cat centermol.txt`


#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! gist.in
#parm rec.watbox.leap.prm7 
parm ${jobId}/rec.watbox.leap.prm7
trajin ${jobId}/$subtraj.mdcrd 1 10000
gist doorder gridcntr ${center} griddim 40 40 40 gridspacn 0.50 
go
EOF
#gist doorder doeij gridcntr 35.759163 33.268703 31.520596 griddim 40 40 40 gridspacn 0.50 out gist.out


#ln -s ../*.mdcrd .
#ln -s ../rec_h.wat.leap.prm7 .

cat << EOF > qsub_${subtraj}_gist.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q all.q
#\$ -o stdout
#\$ -e stderr

cd $workdir

/nfs/soft/amber/amber14/bin/cpptraj -i gist.in > ! gist.log 

EOF

qsub qsub_${subtraj}_gist.csh

end
