#!/bin/csh


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 
set amberexe = "$AMBERHOME/bin/sander"

#set com = "mmrc" 
#set s1  = "mmc"
#set s2  = "raf"
#
#set com = "mmrc" 
#set s1  = "mm"
#set s2  = "rc"
#
# set com = "com" 
# set s1  = "rec"
# set s2  = "lig"

set com = "mm"
set s1  = "m1"
set s2  = "m2"

set name = "${s1}_${s2}_${com}"
#set name = "${com}"

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

#cd  analysis/008_mmgbsa_momomer/
#cd  analysis/008_mmgbsa/
#cd  ${pwd}/008_mmgbsa/full_${seed}/
cd ${mountdir}/0008_mmgbsa_chunk/full_${seed}/${chunk}

foreach species ($s1 $s2 $com) 
#foreach species ($com) 

# awk 'BEGIN{lammda = 0.00542; beta=0.92; print "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" }/VDWAALS/{vdw=$3; es=$6; gb = $9}/ESURF/{esurf = $3;sasa = ($3-beta)/lammda; printf"%f, %f, %f, %f, %f, %f \n",vdw,es,gb,esurf,sasa,vdw+es+gb+esurf}' mmgbsa_cal_${species}.out > mmgbsa_cal_${species}_processed.csv 

  awk 'BEGIN{lammda = 0.00542; beta=0.92; print "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" }/VDWAALS/{vdw=$3; es=$6; gb = $9}/ESURF/{esurf = lammda*$3+beta;sasa = $3; printf"%f, %f, %f, %f, %f, %f \n",vdw,es,gb,esurf,sasa,vdw+es+gb+esurf}' mmgbsa_cal_${species}.out > mmgbsa_cal_${species}_processed.csv

end

paste -d, mmgbsa_cal_${com}_processed.csv mmgbsa_cal_${s1}_processed.csv mmgbsa_cal_${s2}_processed.csv  > mmgbsa_cal_processed_${name}.csv

#awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}' mmgbsa_cal_processed.csv > mmgbsa_cal_processed_delta.csv
awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(NF==18){if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}}' mmgbsa_cal_processed_${name}.csv > mmgbsa_cal_processed_${name}_delta.csv

end # chunk

set workdir2 = ${mountdir}/0008_mmgbsa_chunk/full_${seed}/all_chunks/
mkdir -p $workdir2
cd $workdir2

 echo  "Dvdw,Des,Dgb,Dapol,DGbind" > mmgbsa_cal_all_processed_${name}_delta.csv
 #echo  "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" > mmgbsa_cal_all_${name}_processed.csv
 #cat ${mountdir}/0008_mmgbsa_chunk/full_${seed}/??md/mmgbsa_cal_${name}_processed.csv | grep -v "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" >> mmgbsa_cal_all_${name}_processed.csv
 #paste -d, mmgbsa_cal_all_${com}_processed.csv ${mountdir}/0008_mmgbsa_chunk/full_${seed}/??md/mmgbsa_cal_${s1}_processed.csv ${mountdir}/0008_mmgbsa_chunk/full_${seed}/??md/mmgbsa_cal_${s2}_processed.csv  > mmgbsa_cal_processed_${name2}.csv
 #awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(NF==18){if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}}' mmgbsa_cal_processed_${name2}.csv | grep -v "Dvdw,Des,Dgb,Dapol,DGbind"  >> mmgbsa_cal_processed_${name2}_delta.csv
 cat ${mountdir}/0008_mmgbsa_chunk/full_${seed}/??md/mmgbsa_cal_processed_${name}_delta.csv | grep -v "Dvdw,Des,Dgb,Dapol,DGbind" >> mmgbsa_cal_all_processed_${name}_delta.csv

 python ${mountdir}/for008mmgbsa_plot.py  mmgbsa_cal_all_processed_${name}_delta.csv plots_${name} > plot_${name}.log
end # seed
