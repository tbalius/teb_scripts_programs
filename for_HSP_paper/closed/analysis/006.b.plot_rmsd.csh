## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

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

python ${scriptdir}/006.plot_rmsd.py hsp83_dimer_bb_fit.dat    "HSP83 Dimer backbone RMSD"       hsp83_dimer_bb_fit_rmsd
python ${scriptdir}/006.plot_rmsd.py hsp83_dimer_nofit.dat "HSP83 Dimer RMSD"    hsp83_dimer_rmsd
python ${scriptdir}/006.plot_rmsd.py hsp83_dimer_ions_nofit.dat "HSP83 Dimer RMSD (w/ions)"    hsp83_dimer_ions_rmsd
python ${scriptdir}/006.plot_rmsd.py cdc37_nofit.dat "CDC37 RMSD"    cdc37_rmsd
python ${scriptdir}/006.plot_rmsd.py raf_nofit.dat "RAF RMSD"    raf_rmsd
python ${scriptdir}/006.plot_rmsd.py atp1.dat      "ATP1 RMSD"   atp1_rmsd
python ${scriptdir}/006.plot_rmsd.py atp2.dat     "ATP2 RMSD"   atp2_rmsd
python ${scriptdir}/006.plot_rmsd.py SRC_loop_rmsd.dat      "SRC loop RMSD"   SRC_loop_rmsd
#python ${mountdir}/006.plot_rmsf_renumbered.py SRC_loop_rmsf_fluct_combined.dat  "SRC loop RMSF"      SRC_loop_rmsf
#python ${mountdir}/006.plot_rmsf_renumbered.py RAF_luminal_rmsf_fluct_combined.dat  "RAF luminal RMSF"      RAF_luminal_rmsf
#python ${mountdir}/006.plot_rmsf_renumbered.py HSP_mon1_rmsf_fluct_combined.dat "HSP Monomer 1 RMSF"  HSP_mon1_rmsf
#python ${mountdir}/006.plot_rmsf_renumbered.py HSP_mon2_rmsf_fluct_combined.dat "HSP Monomer 2 RMSF" HSP_mon2_rmsf
#python ${mountdir}/006.plot_rmsf_renumbered.py RAF_rmsf_fluct_combined.dat "RAF RMSF" RAF_rmsf
#python ${mountdir}/006.plot_rmsf_renumbered.py cdc37_rmsf_fluct_combined.dat "CDC37 RMSF" cdc37_rmsf

end # seed
