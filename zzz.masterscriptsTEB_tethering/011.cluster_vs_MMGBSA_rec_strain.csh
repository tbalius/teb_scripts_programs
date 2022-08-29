

 #cat ../pose1/008_mmgbsa/full_0/mmgbsa_cal_rec_processed.csv ../pose1/008_mmgbsa/full_5/mmgbsa_cal_rec_processed.csv ../pose1/008_mmgbsa/full_50/mmgbsa_cal_rec_processed.csv \
 cat 008_mmgbsa/full_0/mmgbsa_cal_rec_processed.csv 008_mmgbsa/full_5/mmgbsa_cal_rec_processed.csv 008_mmgbsa/full_50/mmgbsa_cal_rec_processed.csv \
    #../pose4/008_mmgbsa/full_0/mmgbsa_cal_rec_processed.csv ../pose4/008_mmgbsa/full_5/mmgbsa_cal_rec_processed.csv ../pose4/008_mmgbsa/full_50/mmgbsa_cal_rec_processed.csv \
    #../pose2/008_mmgbsa/full_0/mmgbsa_cal_rec_processed.csv ../pose2/008_mmgbsa/full_5/mmgbsa_cal_rec_processed.csv ../pose2/008_mmgbsa/full_50/mmgbsa_cal_rec_processed.csv \
     | grep -v  "vdw+es+gb+esurf_lin" \
     | awk -F, 'BEGIN{count=1}{if(count==1){printf"Num  Grec\n"}printf"%d  %s\n",count,$5;count=count+1}' > mmgbsa_rec.dat


 set min = `awk 'BEGIN{min=10000000.0;count=0}{if(count!=0){if($2<min){min=$2}};count=count+1}END{print min}' mmgbsa_rec.dat `
 set max = `awk 'BEGIN{max=-10000000.0;count=0}{if(count!=0){if($2>max){max=$2}};count=count+1}END{print max}' mmgbsa_rec.dat `

 echo "min = $min; max = $max"
 
 awk 'BEGIN{min='$min';count=0}{if(count==0){print $0}else{printf"%s %f\n",$1,($2-min)};count=count+1}' mmgbsa_rec.dat > mmgbsa_rec_strain.dat

 paste  009.clustering_4.0_mod/cnumvtime.dat mmgbsa_rec_strain.dat | awk '{print $2,$4}' > cnumvrecstrain_complete_4.dat

 python 011.plot_cluster_rmsd.py cnumvrecstrain_complete_4.dat cnumvrecstrain_complete_4 cnumvrecstrain_complete_4 

