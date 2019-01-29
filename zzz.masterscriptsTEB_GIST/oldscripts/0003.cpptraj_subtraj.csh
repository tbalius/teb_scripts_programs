
set mountdir = `pwd` 


foreach traj ( \
# 09md \
# 10md \
# 11md \
# 12md \
# 13md \
# 14md \
  15md \
  16md \
  17md \
  18md \
)

cd $mountdir

rm -r ${traj}_gist
mkdir ${traj}_gist
cd ${traj}_gist

set workdir = $mountdir/${traj}_gist

#ln -s $mountdir/rec.watbox.leap.prm7 .
ln -s $mountdir/rec_h.wat.leap.prm7 .
ln -s $mountdir/$traj.mdcrd .

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! gist.$traj.in
#parm rec.watbox.leap.prm7 
parm rec_h.wat.leap.prm7
trajin $traj.mdcrd 1 10000
gist doorder doeij gridcntr 41.562  33.784  28.321 griddim 40 40 40 gridspacn 0.50 out gist.out
go
EOF
#gist doorder doeij gridcntr 35.759163 33.268703 31.520596 griddim 40 40 40 gridspacn 0.50 out gist.out

cat << EOF > qsub.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q all.q
#\$ -o stdout
#\$ -e stderr

cd $workdir

/nfs/soft/amber/amber14/bin/cpptraj -i gist.$traj.in > ! gist.$traj.log 

EOF

qsub qsub.csh

end # traj
