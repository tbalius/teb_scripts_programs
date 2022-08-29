## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


# set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C 
#set lig = DL2040 
set lig = DL2078 

#foreach pose (   \
#               1 \
#               2 \
#               3 \
#)
#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/
#cd $mountdir


   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"

#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
#set jobId = $temp:h:t
#echo $jobId
#set jid = $jobId


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/009.PCA_combined/
cd $workdir

python ${mountdir_ori}/plot_pca.py project.dat > plot.log 

#end
