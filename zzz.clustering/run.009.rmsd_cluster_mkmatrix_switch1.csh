

set mountdir = `pwd`

#set workdir = $mountdir/chimera_rmsd_switch1_alignment/
set workdir = $mountdir/workingdir/chimera_rmsd_5/
cd $workdir


 python /home/baliuste/zzz.scripts/matt_rmsd_cluster_complete_linkage_upper_triangle_with_histogram.py switch1_process.txt  matrix_switch1_complete_hist 1.0 1.0 > ! matrix_switch1_complete_hist.1.0.log.txt

 python /home/baliuste/zzz.scripts/matt_rmsd_cluster_single_linkage_upper_triangle_with_histogram.py switch1_process.txt matrix_switch1_single_hist 0.6 1.0 > ! matrix_switch1_single_hist.0.6.log.txt



