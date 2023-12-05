## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

set username = `whoami`

#setenv AMBERHOME /home/${username}/zzz.programs/amber/amber18
setenv AMBERHOME /home/${username}/zzz.programs/amber/amber22_ambertools23/amber22

set mountdir  = `pwd`
#set mountdir_ori = "/path/to/files/Semi_fix_2023_01_19"
set mountdir_ori = "/path/to/files/Closed_fix_2023_01_19_fix_cap"
set scriptdir = "${mountdir}"

#set mut = E37C 
#set lig = DL2040 
#set lig = DL2078 
#set lig = DL1314_Protomer1 
#set lig = 228354851 
#set lig = mol017
#set lig = mol016

#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
#cd $pwd


   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "mod_0"
   #set seed = "mod_5"
   #set seed = "mod_50"
   #set seed = "no_restaint_0"

foreach seed ( \
  "0"  \
  "5"  \
  "50" \
 "500" \
)

 set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"

#echo "ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7"

#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
#set temp = `ls ${mountdir_ori}/${pdb}/0004.MDrun_mod_${seed}/*/01mi.rst7 | head -1`
set temp = `ls ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
#exit
set jid = $jobId


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
#rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .
#ln -s ${mountdir_ori}/0004.MDrun_mod_${seed}/${jid} .
ln -s ${mountdir_ori}/0004.MDrun_corrected_${seed}/${jid} .

# Mg is 310.

# rms hsp83_backbone :1-640,642-1281@CA,N,C,O ref [startframe] out hsp83_dimer_bb_fit.dat
# #rms receptor :1-168,171-172 ref [startframe] out rec_nofit.dat nofit
# rms hsp83_dimer :1-640,642-1281 ref [startframe] out hsp83_dimer_nofit.dat nofit
# rms hsp83_dimer_ions :1-1282 ref [startframe] out hsp83_dimer_ions_nofit.dat nofit
# rms raf :1284-1469 ref [startframe] out raf_nofit.dat nofit
# rms cdc37 :1470-1554 ref [startframe] out cdc37_nofit.dat nofit
#

#parm rec.wat.leap.prm7 
#parm $jobId/com4.watbox.leap.prm7 
#reference $jobId/com4.watbox.leap.rst7 [startframe] 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm $jobId/com1.watbox.leap.prm7 
trajin $jobId/01md.mdcrd 1 last
trajin $jobId/02md.mdcrd 1 last
trajin $jobId/03md.mdcrd 1 last
trajin $jobId/04md.mdcrd 1 last
trajin $jobId/05md.mdcrd 1 last
trajin $jobId/06md.mdcrd 1 last
#trajin $jobId/07md.mdcrd 1 last
trajin $jobId/07.0md.mdcrd 1 last
trajin $jobId/07.1md.mdcrd 1 last
trajin $jobId/07.2md.mdcrd 1 last
trajin $jobId/08md.mdcrd 1 last
trajin $jobId/09md.mdcrd 1 last
trajin $jobId/10md.mdcrd 1 last
trajin $jobId/11md.mdcrd 1 last
trajin $jobId/12md.mdcrd 1 last
trajin $jobId/13md.mdcrd 1 last
trajin $jobId/14md.mdcrd 1 last
trajin $jobId/15md.mdcrd 1 last
trajin $jobId/16md.mdcrd 1 last
trajin $jobId/17md.mdcrd 1 last
trajin $jobId/18md.mdcrd 1 last
reference $jobId/com1.watbox.leap.rst7 [startframe] 
reference $jobId/18md.mdcrd lastframe [last]
autoimage :1-467,469-964 # residue chosen at the center of the dimer interface
rms backbone_start :1-640,642-1281,1284-1554@CA,N,C,O ref [startframe] out bb_fit_start.dat 
rms backbone_last :1-640,642-1281,1284-1554@CA,N,C,O ref [last] out bb_fit_last.dat 
go
EOF

cat << EOF > qsub.csh 
#!/bin/csh

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd.log #&
EOF

sbatch qsub.csh

#end
end # seed 
