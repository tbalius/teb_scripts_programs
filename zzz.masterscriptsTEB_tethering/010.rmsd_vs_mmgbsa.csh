


set pwd = `pwd`

# set seed = "0"
# set seed = "5"
  set seed = "50"
# set seed = "500"
# set seed = "no_restaint_0"
# set seed = "no_restaint_5"
# set seed = "no_restaint_50"


  #cd  analysis/008_mmgbsa_momomer/
  #cd  analysis/008_mmgbsa/
  set workdir =   ${pwd}/010_rmsd_vs_mmgbsa/full_${seed}/
  mkdir -p ${workdir}
  cd ${workdir}
  
  awk -F, '{print $5}' ${pwd}/008_mmgbsa/full_${seed}/mmgbsa_cal_processed_delta.csv > mmgbsa.txt
  set num = `wc -l mmgbsa.txt | awk '{print $1}' `
  @ num = $num - 1
  echo $num

  head -1 ${pwd}/006.rmsd_${seed}/lig1.dat > rmsd_lig.txt
  tail -$num ${pwd}/006.rmsd_${seed}/lig1.dat >> rmsd_lig.txt

  paste rmsd_lig.txt mmgbsa.txt |awk '{print $2, $3}' > rmsd_vs_mmgbsa.txt

  python ${pwd}/plot_rmsd_mmgbsa.py rmsd_vs_mmgbsa.txt
