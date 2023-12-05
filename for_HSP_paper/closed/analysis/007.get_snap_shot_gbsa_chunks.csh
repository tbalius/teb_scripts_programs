#!/bin/csh


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
#set mountdir_ori = "${mountdir}/Semi_fix_2023_01_19" #change me
set scriptdir = "${mountdir}" #change me 


#set name = "."
 set com = "com"
 set s1  = "rec"
 set s2  = "lig"

#set com = "mm" 
#set s1  = "m1"
#set s2  = "m2"

set name = "${s1}_${s2}_${com}"

foreach seed ( \
 "0"     \
 "5"      \
 "50"     \
 "500"    \
)

#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/

 echo ${name} ${seed}

 #set threshold = -30.0
 #set threshold = -370.0
 #set threshold = -500.0
 set threshold = -200.0

#  0008_mmgbsa_chunk/full_500/all_chunks/

# awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | tail -10
# set list = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | awk '{print $1}' | tail -10 | xargs `
# awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | tail -10
# set list2 = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | awk '{print $1}' | tail -10 | xargs `
 awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<'${threshold}'){print count,$0}}' $mountdir/0008_mmgbsa_chunk/full_${seed}/all_chunks/mmgbsa_cal_all_processed_${name}_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | tail -10
 set list = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<'$threshold'){print count,$0}}' $mountdir/0008_mmgbsa_chunk/full_${seed}/all_chunks/mmgbsa_cal_all_processed_${name}_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | awk '{print $1}' | tail -10 | xargs `
 awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>'${threshold}'){print count,$0}}' $mountdir/0008_mmgbsa_chunk/full_${seed}/all_chunks/mmgbsa_cal_all_processed_${name}_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | tail -10
 set list2 = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>'${threshold}'){print count,$0}}' $mountdir/0008_mmgbsa_chunk/full_${seed}/all_chunks/mmgbsa_cal_all_processed_${name}_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | awk '{print $1}' | tail -10 | xargs `
 echo $list 
 echo $list2



 set pdb = "." 

set workdir  = $mountdir/${pdb}/007.snapshot_mmgbsa_${name}_${seed}/
set filedir  = $mountdir/${pdb}/007.com.dimer_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

ln -s $filedir/com.nowat.mdcrd .

foreach num  ( $list $list2)

# call ccptraj
# read in complex traj
# write out specific snapshot
cat << EOF >! make.snapshot.in
parm ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
trajin ./com.nowat.mdcrd $num $num
trajout snapshot.${num}.rst rst nobox novelocity notemperature notime noreplicadim
go
EOF

$AMBERHOME/bin/cpptraj -i make.snapshot.in > ! make.snapshot.log

# cal ambpdb
# convert mdcrd to pdbfile for visualization

 $AMBERHOME/bin/ambpdb -p ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7 < snapshot.${num}.rst > snapshot.${num}.pdb

end #num
cd $mountdir
end # seed
