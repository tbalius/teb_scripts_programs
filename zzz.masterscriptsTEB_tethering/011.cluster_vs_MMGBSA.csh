

 #cat ../pose1/008_mmgbsa/full_0/mmgbsa_cal_processed_delta.csv ../pose1/008_mmgbsa/full_5/mmgbsa_cal_processed_delta.csv ../pose1/008_mmgbsa/full_50/mmgbsa_cal_processed_delta.csv \
 cat 008_mmgbsa/full_0/mmgbsa_cal_processed_delta.csv 008_mmgbsa/full_5/mmgbsa_cal_processed_delta.csv 008_mmgbsa/full_50/mmgbsa_cal_processed_delta.csv \
    #../pose4/008_mmgbsa/full_0/mmgbsa_cal_processed_delta.csv ../pose4/008_mmgbsa/full_5/mmgbsa_cal_processed_delta.csv ../pose4/008_mmgbsa/full_50/mmgbsa_cal_processed_delta.csv \
     #../pose2/008_mmgbsa/full_0/mmgbsa_cal_processed_delta.csv ../pose2/008_mmgbsa/full_5/mmgbsa_cal_processed_delta.csv ../pose2/008_mmgbsa/full_50/mmgbsa_cal_processed_delta.csv \
     | grep -v DGbind \
     | awk -F, 'BEGIN{count=1}{if(count==1){printf"Num  DGbind\n"}printf"%d  %s\n",count,$5;count=count+1}' > mmgbsa.dat

 paste  009.clustering_4.0_mod/cnumvtime.dat mmgbsa.dat | awk '{print $2,$4}' > cnumvmmgbsa_complete_4.dat

 python 011.plot_cluster_rmsd.py cnumvmmgbsa_complete_4.dat cnumvmmgbsa_complete_4 cnumvmmgbsa_complete_4

