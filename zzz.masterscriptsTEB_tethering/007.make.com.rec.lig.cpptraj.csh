## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set mountdir = `pwd`

   #set seed = "0"
   #set seed = "5"
    set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"

set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId

set workdir  = $mountdir/${pdb}/007.com.rec.lig_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# strip away water and save the full dimer complex
cat << EOF > make.com.nowat.in
parm $jobId/com.watbox.leap.prm7
#trajin $jobId/01md.mdcrd 1 10000
#trajin $jobId/02md.mdcrd 1 10000
#trajin $jobId/03md.mdcrd 1 10000
#trajin $jobId/04md.mdcrd 1 10000
#trajin $jobId/06md.mdcrd 1 10000
#trajin $jobId/07md.mdcrd 1 10000
#trajin $jobId/07.1md.mdcrd 1 10000
#trajin $jobId/07.2md.mdcrd 1 10000
#trajin $jobId/08md.mdcrd 1 10000
trajin $jobId/09md.mdcrd 1 10000
trajin $jobId/10md.mdcrd 1 10000
#trajin $jobId/10md.mdcrd 1 10000 100
trajin $jobId/11md.mdcrd 1 10000
trajin $jobId/12md.mdcrd 1 10000
trajin $jobId/13md.mdcrd 1 10000
trajin $jobId/14md.mdcrd 1 10000
trajin $jobId/15md.mdcrd 1 10000
trajin $jobId/16md.mdcrd 1 10000
trajin $jobId/17md.mdcrd 1 10000
trajin $jobId/18md.mdcrd 1 10000
reference $jobId/com.watbox.leap.rst7 [startframe]
strip :WAT
autoimage :1-183
rms backbone :1-180@CA,N,C,O ref [startframe] out bb_fit.dat
trajout com.nowat.mdcrd nobox novelocity notemperature notime noreplicadim
EOF

$AMBERHOME/bin/cpptraj -i make.com.nowat.in > ! make.com.nowat.log 

# now write out the receptor as dimer
cat << EOF >! make.rec.in
parm ../003md_tleap/com.leap.prm7
trajin ./com.nowat.mdcrd 1 1000000
strip :181
trajout rec.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF
$AMBERHOME/bin/cpptraj -i make.rec.in > ! make.rec.log &

# now write out the receptor as dimer
cat << EOF >! make.lig.in
parm ../003md_tleap/com.leap.prm7
trajin ./com.nowat.mdcrd 1 1000000
strip :1-180,182-183
trajout lig.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF
$AMBERHOME/bin/cpptraj -i make.lig.in > ! make.lig.log &

#end # lig <- this is actually the mutant