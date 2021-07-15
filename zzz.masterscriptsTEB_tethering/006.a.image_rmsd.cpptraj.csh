## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


  set mountdir  = `pwd`

    set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"

set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm $jobId/com.watbox.leap.prm7 
trajin $jobId/01md.mdcrd 1 10000
trajin $jobId/02md.mdcrd 1 10000
trajin $jobId/03md.mdcrd 1 10000
trajin $jobId/04md.mdcrd 1 10000
trajin $jobId/06md.mdcrd 1 10000
#trajin $jobId/07md.mdcrd 1 10000
trajin $jobId/07.0md.mdcrd 1 10000
trajin $jobId/07.1md.mdcrd 1 10000
trajin $jobId/07.2md.mdcrd 1 10000
trajin $jobId/08md.mdcrd 1 10000
trajin $jobId/09md.mdcrd 1 10000
trajin $jobId/10md.mdcrd 1 10000
trajin $jobId/11md.mdcrd 1 10000
trajin $jobId/12md.mdcrd 1 10000
trajin $jobId/13md.mdcrd 1 10000
trajin $jobId/14md.mdcrd 1 10000
trajin $jobId/15md.mdcrd 1 10000
trajin $jobId/16md.mdcrd 1 10000
trajin $jobId/17md.mdcrd 1 10000
trajin $jobId/18md.mdcrd 1 10000
reference $jobId/com.watbox.leap.rst7 [startframe] 
#autoimage :1-169
#autoimage :1-166
autoimage :1-183
strip :WAT
rms backbone :1-180@CA,N,C,O ref [startframe] out bb_fit.dat 
rms receptor :1-180,182 ref [startframe] out rec_nofit.dat nofit 
rms gtp1     :183 ref [startframe] out gtp1.dat nofit
rms lig1     :181 ref [startframe] out lig1.dat nofit
rms lig1f    :181 ref [startframe] out lig1_fit.dat
#trajout ref.pdb pdb
go
EOF

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd.log &

#end
