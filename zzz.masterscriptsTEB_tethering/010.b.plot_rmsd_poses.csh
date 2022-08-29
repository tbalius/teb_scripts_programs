## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

setenv AMBERHOME /home/baliuste/zzz.programs/amber/amber18
setenv DOCKBASE "/home/baliuste/zzz.github/DOCK"


#  set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
#set lig = DL2078
set lig = DL1314_Protomer1

set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/
cd $mountdir

set clustertype = "4.0_mod"
#set clustertype = "single_1.0_sieve10"

# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

#set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
#set workdir  = $mountdir/010.rmsd/
set workdir  = $mountdir/010.rmsd_${clustertype}/
cd $workdir


python ${mountdir_ori}/006.plot_rmsd.py lig1.dat      lig1_bb_fit   lig1_rmsd

#end # seed
#end # pose
