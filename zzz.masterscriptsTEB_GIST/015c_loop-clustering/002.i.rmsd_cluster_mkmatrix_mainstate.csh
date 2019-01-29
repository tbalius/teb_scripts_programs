
source /nfs/soft/python/envs/complete/latest/env.csh

set mountdir = `pwd`

set filedir = $mountdir/mainstate/rmsd
set workdir = $mountdir/mainstate/clustering

if (-e $workdir) then
   echo "$workdir exists"
   exit
endif

 mkdir -p $workdir
 cd $workdir

 # syntex: for002.rmsd_cluster_complete.py   rmsd.file output_prefix   clusterThreshold   white_val_heatmap_midpoint
 python ${mountdir}/for002.rmsd_cluster_complete.py ${filedir}/loop_process.txt matrix_loop_complete_hist 1.0 1.0 > ! matrix_loop_complete_hist.1.0.log.txt
 python ${mountdir}/for002.rmsd_cluster_single.py ${filedir}/loop_process.txt   matrix_loop_single_hist   0.6 0.6 > ! matrix_loop_single_hist.0.6.log.txt

echo "gthumb mainstate/clustering*/*png"

