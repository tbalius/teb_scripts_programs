# This script makes 3 lists: 
#       1) for the initial equilibration run (until RT is reached)
#       2) for the final equilibration run
#       3) for the production run
# It then runs a python script that generates plots for analysis of the quality of the MD run in a separate directory.


set mountdir  = `pwd`
set mountdir_ori = "/path/to/files/Closed_fix_2023_01_19_fix_cap"
set scriptdir = "$mountdir"

foreach seed ( \
  "0"  \
  "5"  \
  "50" \
  "500" \
)

  set pdb = ""


  set workdir   = $mountdir/${pdb}/0008.MMGBSA_${seed}/


  if (-e ${workdir}) then
     echo "$workdir exists"
     continue
  endif

  mkdir -p ${workdir}  
  cd $workdir

  ln -s ${mountdir}/Closed_fix_2023_01_19_fix_cap/0008_mmgbsa_chunk/full_$seed/all_chunks/mmgbsa_cal_all_processed_m1_m2_mm_delta.csv .
  ln -s ${mountdir}/Closed_fix_2023_01_19_fix_cap/0008_mmgbsa_chunk/full_$seed/all_chunks/mmgbsa_cal_all_processed_mm_rc_mmrc_delta.csv .
  ln -s ${mountdir}/Closed_fix_2023_01_19_fix_cap/0008_mmgbsa_chunk/full_$seed/all_chunks/mmgbsa_cal_all_processed_mmc_raf_mmrc_delta.csv .

  python ${scriptdir}/for008mmgbsa_plot_conv.py  mmgbsa_cal_all_processed_m1_m2_mm_delta.csv plot_m1_m2_mm > m1_m2_mm.log
  python ${scriptdir}/for008mmgbsa_plot_conv.py  mmgbsa_cal_all_processed_mm_rc_mmrc_delta.csv plot_mm_rc_mmrc > mm_rc_mmrc.log
  python ${scriptdir}/for008mmgbsa_plot_conv.py  mmgbsa_cal_all_processed_mmc_raf_mmrc_delta.csv plot_mmc_raf_mmrc > mmc_raf_mmrc.log

end # seed
