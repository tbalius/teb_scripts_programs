## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 


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
ln -s ${mountdir_ori}/0004.MDrun_corrected_${seed}/${jid} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm $jobId/com1.watbox.leap.prm7
#trajin $jobId/01md.mdcrd 1 last
#trajin $jobId/02md.mdcrd 1 last
#trajin $jobId/03md.mdcrd 1 last
#trajin $jobId/04md.mdcrd 1 last
#trajin $jobId/05md.mdcrd 1 last
#trajin $jobId/06md.mdcrd 1 last
#trajin $jobId/07md.mdcrd 1 last
#trajin $jobId/07.0md.mdcrd 1 last
#trajin $jobId/07.1md.mdcrd 1 last
#trajin $jobId/07.2md.mdcrd 1 last
#trajin $jobId/08md.mdcrd 1 last
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
#autoimage :1-169
#autoimage :1-166
#autoimage :1-170 # no ions
autoimage :296 # residue chosen at the center of the dimer interface
#strip :WAT
rms hsp83_backbone :1-640,642-1281@CA,N,C,O ref [startframe] out hsp83_dimer_bb_fit.dat 
#rms receptor :1-168,171-172 ref [startframe] out rec_nofit.dat nofit 
rms hsp83_dimer :1-640,642-1281 ref [startframe] out hsp83_dimer_nofit.dat nofit 
rms hsp83_dimer_ions :1-1282 ref [startframe] out hsp83_dimer_ions_nofit.dat nofit
rms raf :1284-1469 ref [startframe] out raf_nofit.dat nofit
rms cdc37 :1470-1554 ref [startframe] out cdc37_nofit.dat nofit	
rms atp1     :1555 ref [startframe] out atp1.dat nofit
rms atp2     :1556 ref [startframe] out atp2.dat nofit
rms src_loop  :291-301,932-942 ref [startframe] out SRC_loop_rmsd.dat nofit
# compute RMSF of SRC loop regions
rms ref [startframe] # perform an RMS fit to the startframe structure prior to calculating RMSF
atomicfluct  :291-301,932-942 out SRC_loop_rmsf_bfactor.dat byres bfactor
atomicfluct  :1284-1294 out RAF_luminal_rmsf_bfactor.dat byres bfactor
atomicfluct  :1-640 out HSP_mon1_rmsf_bfactor.dat byres bfactor
atomicfluct  :642-1281 out HSP_mon2_rmsf_bfactor.dat byres bfactor
atomicfluct  :1284-1469 out RAF_rmsf_bfactor.dat byres bfactor
atomicfluct  :1470-1554 out cdc37_rmsf_bfactor.dat byres bfactor
#trajout ref.pdb pdb
go
EOF

cat << EOF > qsub.csh 
#!/bin/csh

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd_all_components_bfactor.log #&
EOF

sbatch qsub.csh

#end
end # seed 
