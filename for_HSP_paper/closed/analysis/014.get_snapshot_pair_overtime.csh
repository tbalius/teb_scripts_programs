## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

#set com = "mmrc"
#set s1  = "mmc"
#set s2  = "raf"

 set com = "com"
 set s1  = "rec"
 set s2  = "lig"

set name = "${s1}_${s2}_${com}"

 set pdb = ""
 #set pdb = "_min"

foreach seed ( \
 "0"   \
 "5"   \
 "50"  \
 "500" \
) 

#set workdir  = $mountdir/${pdb}/014.seed_${seed}.footprint/
#set workdir  = $mountdir/${pdb}/old2/014.footprint_overtime/name_${name}_seed_${seed}/
set workdir  = $mountdir/${pdb}/014.footprint_overtime_frame_by_frame/${name}_seed_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

set list = `ls ${mountdir}/${pdb}/007.snapshot_mmgbsa_${name}_${seed}/snapshot.*.rst`
set prm  =  ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"

#set mask1 = "1-168,170-171"
#set mask2 = "169"
set mask1 = "299"
set mask2 = "959"
    
   set traj = ${mountdir}/${pdb}/007.com.dimer_${seed}/com.nowat.mdcrd
   #set traj = ${mountdir}/${pdb}/old2/0007.com.rec.lig_${seed}_chunk/09md/com.1.09md.nowat.mdcrd

cat <<EOF > qsub.csh 
#!/bin/csh

   cd $workdir
   python ${script}/amber_reader_frame_by_frame.py $prm $traj $mask1 $mask2  ${mask1}_${mask2}_seed${seed} > ${mask1}_${mask2}_seed${seed}.log 
   #python ${script}/amber_reader_mod.py $prm $traj $mask1 $mask2  ${mask1}_${mask2}_seed${seed} > ${mask1}_${mask2}_seed${seed}.log

EOF

sbatch qsub.csh 
   #exit
end # rst

