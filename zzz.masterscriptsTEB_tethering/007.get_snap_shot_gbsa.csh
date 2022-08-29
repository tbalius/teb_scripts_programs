

set mountdir_ori = `pwd`
set mut = E37C 
set lig = DL2040 
#set lig = DL2078 
set lig = DL1314_Protomer1 

foreach pose (   \
               1 \
               2 \
               3 \
)


# grep "3\." analysis/006.rmsd/K5A_0/lig2.dat | sort -k2
# tail analysis/006.rmsd/K5A_0/lig2.dat
# echo "61140 - 50000" | bc
#  11140
# echo "37975 - 11140" | bc
#  26835
#  cat analysis/006.rmsd/K5A_0/lig2.dat | sort -n -k2 | tail | awk '{print $1}'
#  cat analysis/006.rmsd/K5A_0/lig2.dat | sort -n -k2 | tail | awk '{printf"%d \\\n", $1 - 11140}'
 #awk 'BEGIN{frist=1}{if(frist==1){frist=0}else if($2>3.0){print $0}}' 5VBE/006.rmsd_0/lig1.dat | sort -n -k2 | tail -5  

 #set name = 5VBE_old
 #set name = 5VBE_min_old
 set name = "."
 #set name = "_min"
 #set seed = "0"
 #set seed = "5"
 #set seed = "50"
 #set seed = "no_restaint_0"

set mountdir = `pwd`

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
#"mod_0"  \
#"mod_5"  \
#"mod_50" \
)

 set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
 cd $mountdir

 echo ${mut}.${lig}.pose${pose}.seed_${seed}

 set threshold = -30.0

# awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | tail -10
# set list = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | awk '{print $1}' | tail -10 | xargs `
# awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | tail -10
# set list2 = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>-20.0){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | awk '{print $1}' | tail -10 | xargs `
 awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<'${threshold}'){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | tail -10
 set list = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5<'$threshold'){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -rn -k6 | awk '{print $1}' | tail -10 | xargs `
 awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>'${threshold}'){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | tail -10
 set list2 = `  awk -F, 'BEGIN{frist=1;count=0}{if(frist!=1){count=count+1};if(frist==1){frist=0}else if($5>'${threshold}'){print count,$0}}' ${name}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv | sed -e "s/,/ /g" | sort -n -k6 | awk '{print $1}' | tail -10 | xargs `
 echo $list 
 echo $list2



 set pdb = "${name}" 

set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId

set workdir  = $mountdir/${pdb}/007.snapshot_mmgbsa_${seed}/
set filedir  = $mountdir/${pdb}/007.com.rec.lig_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

#ln -s ${mountdir}/004.MDrun/${lig}/${jobId} .
ln -s $filedir/com.nowat.mdcrd .

foreach num  ( $list $list2)

# call ccptraj
# read in complex traj
# write out specific snapshot
cat << EOF >! make.snapshot.in
parm ../003md_tleap/com.leap.prm7
trajin ./com.nowat.mdcrd $num $num 
trajout snapshot.${num}.rst rst nobox novelocity notemperature notime noreplicadim
go
EOF
$AMBERHOME/bin/cpptraj -i make.snapshot.in > ! make.snapshot.log 


# cal ambbdb
# convert mdcrd to pdbfile for visulazation

$AMBERHOME/bin/ambpdb -p ../003md_tleap/com.leap.prm7 < snapshot.${num}.rst > snapshot.${num}.pdb 

end #num
cd $mountdir
end # seed
end # poses
