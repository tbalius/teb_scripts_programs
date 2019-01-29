
source /nfs/soft/python/envs/complete/latest/env.csh

set mountdir = `pwd`
#-rw-r--r--.    1 tbalius bks   4385 Aug 25 13:14 process_extract_dock_occ_mod.py
#-rw-r--r--.    1 tbalius bks   1747 Aug 25 13:14 nogist_dock_occ_100.txt
#-rw-r--r--.    1 tbalius bks   2907 Aug 25 13:20 plot_stacked_barplot_propensities.py
#-rw-r--r--.    1 tbalius bks 345162 Aug 25 13:21 nogistdockocc_100fig.png
# /mnt/nfs/work/tbalius/Water_Project_all_in_the_same_frame_ph4_multigrid

set list = "4NVA"

foreach pdbname ($list)
#set m = 1.0
#set m = 2.0
#set m = 3.0

set workdir = "${mountdir}/flex_multpose/3runEnrich/${pdbname}_compare_gist_nogist/" 

if ( -e $workdir ) then
   echo "$workdir exists."
   exit
endif

mkdir $workdir
cd $workdir

foreach docktype ( \
  "nogist" \
  "gist" \
)

#set workdir = $mountdir/workingdir/align_CcP_A.B.C/DOCKING_${docktype}_save10_sph_${pdblig}/ligands/postDOCKING/
 set filedir = "${mountdir}/flex_multpose/3runEnrich/${pdbname}_${docktype}/ligands/allChunksCombined/"
#set workdir = $mountdir/workingdir/align_CcP_A.B.C_M_1.0_10poses/DOCKING_${docktype}/ligands/postDOCKING/
#set workdir = $mountdir/workingdir/align_CcP_A.B.C_M_2.0_10poses/DOCKING_${docktype}/ligands/postDOCKING/
#set workdir = $mountdir/workingdir/align_CcP_A.B.C_M_3.0_10poses/DOCKING_${docktype}/ligands/postDOCKING/

cd ${workdir}

# make a extract_all file that just contains the ZINC ids in the paper or those of interest. 
touch extract_all.xtalocc_$docktype.txt

foreach zincid ( \
  ZINC01583444 \
  ZINC00331902 \
  ZINC00331945 \
  ZINC00036634 \
  ZINC08652421 \
  ZINC06656163 \
  ZINC04962659 \
  ZINC00331160 \
  ZINC13739037 \
  ZINC01596053 \
  ZINC34979991 \
  ZINC00203341 \
  ZINC00519712 \
  ZINC00388812 \
)
    echo $zincid
    grep $zincid ${filedir}/extract_all.txt | uniq >> extract_all.xtalocc_$docktype.txt
end # zincid

 python $mountdir/for056.process_extract_dock_occ.py $filedir/extract_all.txt ${docktype}_save10.txt
 python $mountdir/for056.process_extract_dock_occ.py extract_all.xtalocc_$docktype.txt ${docktype}_save10.xtalocc.txt

 python $mountdir/for056.plot_stacked_barplot_propensities.py ${docktype}_save10.txt ${docktype}_save10
 python $mountdir/for056.plot_stacked_barplot_propensities.py ${docktype}_save10.xtalocc.txt ${docktype}_save10.xtalocc


end # docktype


 #python $mountdir/for056.plot_stacked_barplot_propensities_3sidebyside.py  $mountdir/for056.NatChemXtalOccs_mod2.csv ${docktype1}_M_${m}_save10.paper.txt ${docktype2}_M_${m}_save10.paper.txt
 python ${mountdir}/for056.plot_stacked_barplot_propensities_3sidebyside.py ${mountdir}/for056.NatChemXtalOccs.csv nogist_save10.xtalocc.txt gist_save10.xtalocc.txt xtal.nogist.gist
 python ${mountdir}/for056.plot_stacked_barplot_propensities_3sidebyside_euclidean.py ${mountdir}/for056.NatChemXtalOccs.csv nogist_save10.xtalocc.txt gist_save10.xtalocc.txt xtal.nogist.gist.euc
 #python $mountdir/for056.plot_stacked_barplot_propensities_3sidebyside.py standard_M_1.0_save10.paper.txt standard_M_2.0_save10.paper.txt standard_M_3.0_save10.paper.txt standard.m.eq.1.2.3
 #python $mountdir/for056.plot_stacked_barplot_propensities_3sidebyside.py gistC_M_1.0_save10.paper.txt gistC_M_2.0_save10.paper.txt gistC_M_3.0_save10.paper.txt gist.m.eq.1.2.3

end # pdbname
