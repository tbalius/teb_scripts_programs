
#set pwd = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
set lig = DL2078 
#set lig = DL1314_Protomer1 

foreach pose (   \
               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $mountdir
set pwd = $mountdir

# set seed = "0"
# set seed = "5"
# set seed = "50"
# set seed = "500"
# set seed = "no_restaint_0"

foreach seed ( \
 "0"      \
 "5"      \
 "50"     \
#"mod_0"  \
#"mod_5"  \
#"mod_50" \
)


#cd  analysis/008_mmgbsa_momomer/
#cd  analysis/008_mmgbsa/
cd  ${pwd}/008_mmgbsa/full_${seed}/

foreach species (lig rec com) 
  # 
  #awk 'BEGIN{lammda = 0.00542; beta=0.92;sascale=0.005; print "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" }/VDWAALS/{vdw=$3; es=$6; gb = $9}/ESURF/{sasa = $3/sascale; esurf = lammda*sasa+beta; printf"%f, %f, %f, %f, %f, %f \n",vdw,es,gb,esurf,sasa,vdw+es+gb+esurf}' mmgbsa_cal_${species}.out > mmgbsa_cal_${species}_processed.csv 
  awk 'BEGIN{lammda = 0.00542; beta=0.92; print "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" }/VDWAALS/{vdw=$3; es=$6; gb = $9}/ESURF/{sasa = $3; esurf = lammda*sasa+beta; printf"%f, %f, %f, %f, %f, %f \n",vdw,es,gb,esurf,sasa,vdw+es+gb+esurf}' mmgbsa_cal_${species}.out > mmgbsa_cal_${species}_processed.csv 

end

paste -d, mmgbsa_cal_*_processed.csv > mmgbsa_cal_processed.csv
# if surften = 0.005
#awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}' mmgbsa_cal_processed.csv > mmgbsa_cal_processed_delta.csv
# if surften = 1.0
awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(NF==18){if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}}' mmgbsa_cal_processed.csv > mmgbsa_cal_processed_delta.csv

 python ${mountdir_ori}/for008mmgpsa_plot.py  mmgbsa_cal_processed_delta.csv plots > plot.log

end # seed
end # pose
