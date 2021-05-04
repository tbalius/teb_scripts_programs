
set pwd = `pwd`

# set seed = "0"
# set seed = "5"
  set seed = "50"
# set seed = "500"
# set seed = "no_restaint_0"


#cd  analysis/008_mmgbsa_momomer/
#cd  analysis/008_mmgbsa/
cd  ${pwd}/008_mmgbsa/full_${seed}/

foreach species (lig rec com) 

  awk 'BEGIN{lammda = 0.00542; beta=0.92; print "vdw, es, gb, esurf, sasa, vdw+es+gb+esurf_lin" }/VDWAALS/{vdw=$3; es=$6; gb = $9}/ESURF/{esurf = $3;sasa = ($3-beta)/lammda; printf"%f, %f, %f, %f, %f, %f \n",vdw,es,gb,esurf,sasa,vdw+es+gb+esurf}' mmgbsa_cal_${species}.out > mmgbsa_cal_${species}_processed.csv 

end

paste -d, mmgbsa_cal_*_processed.csv > mmgbsa_cal_processed.csv

#awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}' mmgbsa_cal_processed.csv > mmgbsa_cal_processed_delta.csv
awk -F, 'BEGIN{fristline=1;print "Dvdw,Des,Dgb,Dapol,DGbind"}{if(NF==18){if(fristline==1){fristline=0}else{Dvdw = $1-($7+$13);Des =$2-($8+$14);Dgb=$3-($9+$15);Dapol=$4-($10+$16);Dbind=$6-($12+$18);print Dvdw "," Des "," Dgb "," Dapol "," Dbind }}}' mmgbsa_cal_processed.csv > mmgbsa_cal_processed_delta.csv

 python ${pwd}/for008mmgpsa_plot.py  mmgbsa_cal_processed_delta.csv plots > plot.log

