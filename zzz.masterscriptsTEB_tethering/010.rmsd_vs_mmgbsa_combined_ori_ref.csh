


#set pwd = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
#set lig = DL2078
set lig = DL1314_Protomer1 

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
# set seed = "no_restaint_5"
# set seed = "no_restaint_50"


  #cd  analysis/008_mmgbsa_momomer/
  #cd  analysis/008_mmgbsa/
  set workdir =   ${pwd}/010_rmsd_vs_mmgbsa/full_combined/
  mkdir -p ${workdir}
  cd ${workdir}
  
  awk -F, '{print $5}' ${pwd}/008_mmgbsa/full_0/mmgbsa_cal_processed_delta.csv > mmgbsa.txt
  set num = `wc -l mmgbsa.txt | awk '{print $1}' `
  @ num = $num - 1
  echo $num
  awk -F, '{print $5}' ${pwd}/008_mmgbsa/full_5/mmgbsa_cal_processed_delta.csv | tail -$num >> mmgbsa.txt
  awk -F, '{print $5}' ${pwd}/008_mmgbsa/full_50/mmgbsa_cal_processed_delta.csv | tail -$num >> mmgbsa.txt

  head -1 ${pwd}/006.rmsd_0/lig1.dat > rmsd_lig.txt
  tail -$num ${pwd}/006.rmsd_0/lig1.dat >> rmsd_lig.txt
  tail -$num ${pwd}/006.rmsd_5/lig1.dat >> rmsd_lig.txt
  tail -$num ${pwd}/006.rmsd_50/lig1.dat >> rmsd_lig.txt

  paste rmsd_lig.txt mmgbsa.txt |awk '{print $2, $3}' > rmsd_vs_mmgbsa.txt

  python ${mountdir_ori}/plot_rmsd_mmgbsa.py rmsd_vs_mmgbsa.txt

end # pose
