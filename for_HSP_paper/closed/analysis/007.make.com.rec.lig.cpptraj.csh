## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

#set mountdir = `pwd`


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
 "500"    \
)

 set pdb = ""
 #set pdb = "_min"

#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
#set temp = `ls ${mountdir}/${pdb}/0004.MDrun_mod_${seed}/*/01mi.rst7 | head -1`
set temp = `ls ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId

set workdir  = $mountdir/${pdb}/0007.com.rec.lig_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .
#ln -s ${mountdir}/${pdb}/0004.MDrun_mod_${seed}/${jobId} .
ln -s ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/${jobId} .

# strip away water and save the full dimer complex
cat << EOF > make.com.1.mmrc.nowat.in
parm $jobId/com1.watbox.leap.prm7
#trajin $jobId/01md.mdcrd 1 1000000
#trajin $jobId/02md.mdcrd 1 1000000
#trajin $jobId/03md.mdcrd 1 1000000
#trajin $jobId/04md.mdcrd 1 1000000
#trajin $jobId/06md.mdcrd 1 1000000
#trajin $jobId/07md.mdcrd 1 1000000
#trajin $jobId/07.1md.mdcrd 1 1000000
#trajin $jobId/07.2md.mdcrd 1 1000000
#trajin $jobId/08md.mdcrd 1 1000000
trajin $jobId/09md.mdcrd 1 1000000
trajin $jobId/10md.mdcrd 1 1000000
#trajin $jobId/10md.mdcrd 1 1000000 100
trajin $jobId/11md.mdcrd 1 1000000
trajin $jobId/12md.mdcrd 1 1000000
trajin $jobId/13md.mdcrd 1 1000000
trajin $jobId/14md.mdcrd 1 1000000
trajin $jobId/15md.mdcrd 1 1000000
trajin $jobId/16md.mdcrd 1 1000000
trajin $jobId/17md.mdcrd 1 1000000
trajin $jobId/18md.mdcrd 1 1000000
reference $jobId/com1.watbox.leap.rst7 [startframe]
strip :WAT
#autoimage :1-170
autoimage :1288
rms backbone :1-1554@CA,N,C,O ref [startframe] out bb_fit.dat
trajout com.1.nowat.mdcrd nobox novelocity notemperature notime noreplicadim
EOF

# 1288 is part of RAF incerted into the luminal regon. 
# 1-1516 is everythin exept ATP
# ATP is 1555 and 1556 


# now write out the receptor as dimer
#parm ../003md_tleap/com.leap.prm7
#parm ../003md_tleap/com.nowat.leap.prm7
#parm ../003md_tleap/com.leap.prm7
cat << EOF >! make.raf.2.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :1-1282,1470-1556
trajout raf.2.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

# now write out the receptor as dimer
#parm ../003md_tleap/com.leap.prm7
#parm ../003md_tleap/com.nowat.leap.prm7
cat << EOF >! make.com.3.mmc.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :1283-1469
trajout com.3.mmc.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

cat << EOF >! make.com.4.mm.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :1283-1554
trajout com.4.mm.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

cat << EOF >! make.mon1.5.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :642-1554,1556
trajout m1.5.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF


cat << EOF >! make.mon2.6.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :1-641,1283-1555
trajout m2.6.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

# RAF and CDC37
cat << EOF >! make.rc.7.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.nowat.mdcrd 1 1000000
strip :1-1282,1555-1556
trajout com.7.rc.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF



cat << EOF > qsub.csh 
#!/bin/csh

cd $workdir
$AMBERHOME/bin/cpptraj -i make.com.1.mmrc.nowat.in >! make.com.1.mmrc.nowat.log
$AMBERHOME/bin/cpptraj -i make.raf.2.in >! make.raf.2.log 
$AMBERHOME/bin/cpptraj -i make.com.3.mmc.in >! make.com.3.mmc.log 
$AMBERHOME/bin/cpptraj -i make.com.4.mm.in >! make.com.4.mm.log 
$AMBERHOME/bin/cpptraj -i make.mon1.5.in >! make.mon1.5.log 
$AMBERHOME/bin/cpptraj -i make.mon2.6.in >! make.mon2.6.log 
$AMBERHOME/bin/cpptraj -i make.rc.7.in >! make.rc.7.log 

EOF

sbatch qsub.csh
#csh qsub.csh

#end # lig <- this is actually the mutant
end # seed 
#end # poses
