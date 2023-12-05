## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.


set mountdir  = `pwd`
set mountdir_ori = "/path/to/files/Semi_fix_2023_01_19"
set scriptdir = "${mountdir}"

## TEB / MF comments -- March 2017
#set mountdir = `pwd`
#set mut = E37C 
#set lig = DL2040 
#set lig = DL2078 
#set lig = DL1314_Protomer1 

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
 "500" \
)

set pdb = ''
#set pdb = '_min'
#set pdb = '5VBE_min'

set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
#set workdir  = $mountdir/${pdb}/006.rmsf_combined/
#set workdir  = $mountdir/analysis/006.rmsd.old/${lig}
#set workdir  = $mountdir/analysis/006.rmsd_lig_sim
cd $workdir

#set jobId = "563115"
#set jobId = "595584"

#ln -s ${mountdir}/004.MDrun/${jobId} .

python ${scriptdir}/006.plot_rmsd.py bb_fit_start.dat    "backbone RMSD to start"       bb_fit_rmsd_start
python ${scriptdir}/006.plot_rmsd.py bb_fit_last.dat    "backbone RMSD to last"       bb_fit_rmsd_last
#python ${scriptdir}/006.plot_rmsd.py hsp83_dimer_nofit.dat "HSP83 Dimer RMSD"    hsp83_dimer_rmsd
#python ${scriptdir}/006.plot_rmsd.py hsp83_dimer_ions_nofit.dat "HSP83 Dimer RMSD (w/ions)"    hsp83_dimer_ions_rmsd
#python ${scriptdir}/006.plot_rmsd.py atp1.dat      "ATP1 RMSD"   atp1_rmsd
#python ${scriptdir}/006.plot_rmsd.py atp2.dat      "ATP2 RMSD"   atp2_rmsd
#python ${scriptdir}/006.plot_rmsd.py SRC_loop_rmsd.dat      "SRC loop RMSD"   SRC_loop_rmsd

end # seed
