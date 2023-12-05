## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
 "500"    \
)

foreach chunk ( \
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

 set pdb = ""
 #set pdb = "_min"

#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
#set temp = `ls ${mountdir}/${pdb}/0004.MDrun_mod_${seed}/*/01mi.rst7 | head -1`
set temp = `ls ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId

set workdir  = $mountdir/${pdb}/0007.com.rec.lig_${seed}_chunk/${chunk}

rm -rf $workdir
mkdir -p $workdir
cd $workdir

#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .
#ln -s ${mountdir}/${pdb}/0004.MDrun_mod_${seed}/${jobId} .
ln -s ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/${jobId} .

# strip away water and save the full dimer complex
cat << EOF > make.com.1.mmrc.nowat.in
parm $jobId/com1.watbox.leap.prm7
trajin $jobId/$chunk.mdcrd 1 last
reference $jobId/com1.watbox.leap.rst7 [startframe]
strip :WAT
#autoimage :1-170
autoimage :1288
rms backbone :1-1554@CA,N,C,O ref [startframe] out bb_fit.dat
trajout com.1.${chunk}.nowat.mdcrd nobox novelocity notemperature notime noreplicadim
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
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :1-1282,1470-1556
trajout raf.2.${chunk}.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

# now write out the receptor as dimer
#parm ../003md_tleap/com.leap.prm7
#parm ../003md_tleap/com.nowat.leap.prm7
cat << EOF >! make.com.3.mmc.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :1283-1469
trajout com.3.${chunk}.mmc.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

cat << EOF >! make.com.4.mm.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :1283-1554
trajout com.4.${chunk}.mm.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

cat << EOF >! make.mon1.5.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :642-1554,1556
trajout m1.5.${chunk}.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF


cat << EOF >! make.mon2.6.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :1-641,1283-1555
trajout m2.6.${chunk}.mdcrd nobox novelocity notemperature notime noreplicadim
go
EOF

# RAF and CDC37
cat << EOF >! make.rc.7.in
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ./com.1.${chunk}.nowat.mdcrd 1 1000000
strip :1-1282,1555-1556
trajout com.7.${chunk}.rc.mdcrd nobox novelocity notemperature notime noreplicadim
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
end # chunks 
end # seed 
#end # poses
