## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
#set scriptdir = "${mountdir}" #change me 


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

set workdir  = $mountdir/${pdb}/misc_distance_seed${seed}/
#mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .
#ln -s ${mountdir_ori}/0004.MDrun_corrected_${seed}/${jid} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! calc_dist.prod.in 
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
autoimage :296 # residue chosen at the center of the dimer interface
strip :WAT
#distance 340B_519A :932 :470 out 340B_519A_dist.txt geom
#distance RAF423_343A :1289 :294 out RAF423_343A_dist.txt geom
distance RAF423_RAF477 :1289 :1343 out RAF423_RAF477_dist.txt geom
#distance 343B_519A :935 :470 out 343B_519A_dist.txt geom
#distance 340A_519B :291 :1111 out 340A_519B_dist.txt geom 
#distance 343A_519B :294 :1111 out 343A_519B_dist.txt geom
#trajout ref.pdb pdb
go
EOF

cat << EOF > qsub.csh 
#!/bin/csh

$AMBERHOME/bin/cpptraj -i calc_dist.prod.in > ! calc_dist.log #&
EOF

sbatch qsub.csh

#end
end # seed 
