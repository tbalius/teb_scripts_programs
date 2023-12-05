## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

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

set jidlist = ()

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
set jidlist = ( $jidlist $jobId )

end #seed

# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/006.rmsf_combined/
#rm -rf $workdir
#mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .
#ln -s ${mountdir_ori}/0004.MDrun_corrected_${seed}/${jid} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsf.equil.prod.in 
parm $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/com1.watbox.leap.prm7
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
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/09md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/10md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/11md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/12md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/13md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/14md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/15md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/16md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/17md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/18md.mdcrd 1 last
###
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/09md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/10md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/11md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/12md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/13md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/14md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/15md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/16md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/17md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_5/$jidlist[2]/18md.mdcrd 1 last
###
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/09md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/10md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/11md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/12md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/13md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/14md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/15md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/16md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/17md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_50/$jidlist[3]/18md.mdcrd 1 last
###
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/09md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/10md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/11md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/12md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/13md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/14md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/15md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/16md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/17md.mdcrd 1 last
trajin $mountdir/${pdb}/006.rmsd_500/$jidlist[4]/18md.mdcrd 1 last
reference $mountdir/${pdb}/006.rmsd_0/$jidlist[1]/com1.watbox.leap.rst7 [startframe] 
#autoimage :1-169
#autoimage :1-166
#autoimage :1-170 # no ions
autoimage :296 # residue chosen at the center of the dimer interface
#strip :WAT
#rms hsp83_backbone :1-640,642-1281@CA,N,C,O ref [startframe] out hsp83_dimer_bb_fit.dat 
#rms receptor :1-168,171-172 ref [startframe] out rec_nofit.dat nofit 
#rms hsp83_dimer :1-640,642-1281 ref [startframe] out hsp83_dimer_nofit.dat nofit 
#rms hsp83_dimer_ions :1-1282 ref [startframe] out hsp83_dimer_ions_nofit.dat nofit
#rms raf :1284-1469 ref [startframe] out raf_nofit.dat nofit
#rms cdc37 :1470-1554 ref [startframe] out cdc37_nofit.dat nofit	
#rms atp1     :1555 ref [startframe] out atp1.dat nofit
#rms atp2     :1556 ref [startframe] out atp2.dat nofit
#rms src_loop  :291-301,932-942 ref [startframe] out SRC_loop_rmsd.dat nofit
# compute RMSF of SRC loop regions
rms ref [startframe] # perform an RMS fit to the startframe structure prior to calculating RMSF
#atomicfluct  :291-301,932-942 out SRC_loop_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :291-301,932-942 out SRC_loop_rmsf_fluct_combined.dat byres
#atomicfluct  :1284-1294 out RAF_luminal_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :1284-1294 out RAF_luminal_rmsf_fluct_combined.dat byres
#atomicfluct  :1-640 out HSP_mon1_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :1-640 out HSP_mon1_rmsf_fluct_combined.dat byres
#atomicfluct  :642-1281 out HSP_mon2_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :642-1281 out HSP_mon2_rmsf_fluct_combined.dat byres
#atomicfluct  :1284-1469 out RAF_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :1284-1469 out RAF_rmsf_fluct_combined.dat byres
#atomicfluct  :1470-1554 out cdc37_rmsf_bfactor_combined.dat byres bfactor
atomicfluct  :1470-1554 out cdc37_rmsf_fluct_combined.dat byres
#trajout ref.pdb pdb
go
EOF

cat << EOF > qsub.csh 
#!/bin/csh

#$AMBERHOME/bin/cpptraj -i rmsf.equil.prod.in > ! rmsf_all_components_bfactor.log #&
$AMBERHOME/bin/cpptraj -i rmsf.equil.prod.in > ! rmsf_all_components.log #&
EOF

sbatch qsub.csh

#end
