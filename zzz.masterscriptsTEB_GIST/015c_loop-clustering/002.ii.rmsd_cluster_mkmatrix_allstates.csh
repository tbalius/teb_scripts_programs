

set mountdir = `pwd`

set filedir = $mountdir/allstates/rmsd
set workdir = $mountdir/allstates/clustering

if (-e $workdir) then
   echo "$workdir exists"
   continue
endif

 mkdir -p $workdir
 cd $workdir

 python ${mountdir}/for002.rmsd_cluster_complete.py ${filedir}/loop_process.txt  ${filedir}/matrix_loop_complete_hist 1.0 1.0 > ! matrix_loop_complete_hist.1.0.log.txt
 python ${mountdir}/for002.rmsd_cluster_single.py loop_process.txt matrix_loop_single_hist 0.6 1.0 > ! matrix_loop_single_hist.0.6.log.txt

 echo "gthumb mainstate/clustering*/*png"
