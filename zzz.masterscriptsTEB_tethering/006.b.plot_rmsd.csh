## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017
#set mountdir = `pwd`
set mountdir_ori = `pwd`
set mut = E37C 
#set lig = DL2040 
set lig = DL2078 
#set lig = DL1314_Protomer1 

foreach pose (   \
#               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
#cd $pwd

#set seed = "0"
#set seed = "5"
#set seed = "50"
#set seed = "mod_0"
#set seed = "mod_5"
#set seed = "mod_50"
#set seed = "no_restaint_0"

foreach seed ( \
  "0"  \
  "5"  \
  "50" \
)

set pdb = ''
#set pdb = '_min'
#set pdb = '5VBE_min'

set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
#set workdir  = $mountdir/analysis/006.rmsd.old/${lig}
#set workdir  = $mountdir/analysis/006.rmsd_lig_sim
cd $workdir

#set jobId = "563115"
#set jobId = "595584"

#ln -s ${mountdir}/004.MDrun/${jobId} .

python ${mountdir_ori}/006.plot_rmsd.py bb_fit.dat    bb_fit        bb_fit_rmsd
python ${mountdir_ori}/006.plot_rmsd.py rec_nofit.dat rec_bb_fit    rec_rmsd
python ${mountdir_ori}/006.plot_rmsd.py gtp1.dat      gtp1_bb_fit   gtp1_rmsd
python ${mountdir_ori}/006.plot_rmsd.py lig1.dat      lig1_bb_fit   lig1_rmsd
python ${mountdir_ori}/006.plot_rmsd.py lig1_fit.dat  lig1_fit      lig1_fit_rmsd

#end
end # seed
end # poses
