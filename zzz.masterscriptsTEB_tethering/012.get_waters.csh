## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set mountdir = `pwd`

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"

foreach seed ("0" "5" "50") 


set list = `ls ${mountdir}/${pdb}/007.snapshot_mmgbsa_${seed}/snapshot.*.rst`
foreach rst ($list)

 
 set frame_num = $rst:r:e
 #set frame_num = 0022
 #set frame_num  = 0564
 #set frame_num  = 9424

 set traj_num      = ` echo "${frame_num}/1000" | bc `
 set frame_num_mod = ` echo "${frame_num}%1000" | bc `
 set name = `echo $traj_num | awk '{printf"%02d",$1+9}'`

 echo "frame_num = ${frame_num} traj_num = ${traj_num} mod = ${frame_num_mod} name = $name"

# exit
set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId

#set workdir  = $mountdir/${pdb}/012.water_${frame_num}_${seed}/
set workdir  = $mountdir/${pdb}/012.water/snapshot_${frame_num}_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

#trajout com_wat.pdb nobox novelocity notemperature notime noreplicadim
# strip away water and save the full dimer complex
#trajin $jobId/18md.mdcrd 1 10000
cat << EOF > get.wat.in
parm $jobId/com.watbox.leap.prm7
trajin $jobId/${name}md.mdcrd ${frame_num_mod} ${frame_num_mod} 1
reference $jobId/com.watbox.leap.rst7 [startframe]
#autoimage :1-172
autoimage :1-171
#rms backbone :1-169@CA,N,C,O ref [startframe] out bb_fit.dat
rms backbone :1-168@CA,N,C,O ref [startframe] out bb_fit.dat
#closest 10 :170
closest 10 :169
#strip :1-172
strip :1-171
trajout wat.pdb nobox novelocity notemperature notime noreplicadim
EOF

$AMBERHOME/bin/cpptraj -i get.wat.in > ! get.wat.log 

cat << EOF > get.wat_com.in
parm $jobId/com.watbox.leap.prm7
trajin $jobId/${name}md.mdcrd ${frame_num_mod} ${frame_num_mod} 1
reference $jobId/com.watbox.leap.rst7 [startframe]
#autoimage :1-172
#rms backbone :1-169@CA,N,C,O ref [startframe] out bb_fit.dat
#closest 10 :170
autoimage :1-171
rms backbone :1-168@CA,N,C,O ref [startframe] out bb_fit.dat
closest 10 :169
trajout com_wat.pdb nobox novelocity notemperature notime noreplicadim
EOF
$AMBERHOME/bin/cpptraj -i get.wat_com.in > ! get.wat_com.log 

#end # lig <- this is actually the mutant
end # rst
end # seed
