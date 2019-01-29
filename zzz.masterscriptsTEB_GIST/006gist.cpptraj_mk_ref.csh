## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set mountdir = `pwd`
set workdir  = $mountdir/gist/006ref
rm -rf $workdir
mkdir -p $workdir
cd $workdir

set jobId = "5609039"

ln -s ${mountdir}/MDrundir/MDrun/${jobId} .

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! makeref.in 
parm $jobId/rec.watbox.leap.prm7 
trajin $jobId/10md.rst7 1 1 
strip :WAT
trajout ref.pdb pdb
go
EOF

/nfs/soft/amber/amber14/bin/cpptraj -i makeref.in > ! makeref.log &
