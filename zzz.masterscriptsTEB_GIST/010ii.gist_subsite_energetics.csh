#!/bin/csh 

# This script does the following:
# 1) From the MD water freq densities (gist-gO.dx) it generates pdb files containing cluster centers at varying levels of bulk density, here 5, 10, 20, 50 as thresholds.
# 2) Using gist-EswPlus2Eww_ref.dx we then calculate the energies associated with each cluster center (aka MD water), where energy assigned is normalized by the voxel.
# 3) All pdbs can be visualized within PyMOL -- look at the _mdl.pdb files frames using the play button 


## TEB/ MF -- March 2017


setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK
source /nfs/soft/python/envs/complete/latest/env.csh


#set mountdir = "/mnt/nfs/work/users/tbalius/Water_Project/run_DOCK3.7"
set mountdir = `pwd`

set workdir  = $mountdir/gist/010ii.gist_subsite_energetics
set filedir  = $mountdir/gist/010a.full_gist_combine/
set scriptdir = $mountdir/GIST_DX_tools-master/src

  rm -rf  ${workdir}
  mkdir ${workdir}
  cd ${workdir}

  cp $filedir/gist-EswPlus2Eww_ref.dx .
  cp $filedir/gist-gO.dx .

# input for py script is e.g.  'gist-gO.dx 1 5 2 05xbulkdens'
# gist-gO.dx 	contains the MD densities for waters
# 1     	(or -1) is multiplier for water vs anti-water
# 5     	waters above 5x bulk density
# 2     	times 0.5A grid points are considered connected (aka 1A)
# 05xbulkdens 	sensible identifier for pdb file that is generated

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-gO.dx 1 5 2 05xbulkdens > log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph 05xbulkdens_clusters.pdb 05xbulkdens_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' 05xbulkdens_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx 05xbulkdens_clusters.sph > ! 05xbulkdens_clusters_energies.log

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-gO.dx 1 10 2 10xbulkdens >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph 10xbulkdens_clusters.pdb 10xbulkdens_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' 10xbulkdens_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx 10xbulkdens_clusters.sph > ! 10xbulkdens_clusters_energies.log

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-gO.dx 1 20 2 20xbulkdens > log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph 20xbulkdens_clusters.pdb 20xbulkdens_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' 20xbulkdens_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx 20xbulkdens_clusters.sph > ! 20xbulkdens_clusters_energies.log

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-gO.dx 1 50 2 50xbulkdens >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph 50xbulkdens_clusters.pdb 50xbulkdens_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' 50xbulkdens_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx 50xbulkdens_clusters.sph > ! 50xbulkdens_clusters_energies.log


# Waters below -1 kcal/mol/A^3   and    Anti-waters above 1kcal/mol/A^3 -- using gist-EswPlus2Eww_ref.dx
  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-EswPlus2Eww_ref.dx  1 1.0 2 energy_1p0antiwaters >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph energy_1p0antiwaters_clusters.pdb energy_1p0antiwaters_clusters.sph
  sed -i 's/ 0\.700   / 1.400   /g' energy_1p0antiwaters_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx energy_1p0antiwaters_clusters.sph > ! energy_1p0antiwaters.log

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-EswPlus2Eww_ref.dx -1 1.0 2 energy_-1p0waters >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph energy_-1p0waters_clusters.pdb energy_-1p0waters_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' energy_-1p0waters_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx energy_-1p0waters_clusters.sph > ! energy_-1p0waters.log
  #cp out0new_gist.dx out0new_gist-EswPlus2Eww_ref_energy_waters.dx

# Waters below -0.5 kcal/mol/A^3   and    Anti-waters above 0.5 kcal/mol/A^3 -- using gist-EswPlus2Eww_ref.dx
  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-EswPlus2Eww_ref.dx  1 0.5 2 energy_0p5antiwaters >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph energy_0p5antiwaters_clusters.pdb energy_0p5antiwaters_clusters.sph
  sed -i 's/ 0\.700   / 1.400   /g' energy_0p5antiwaters_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx energy_0p5antiwaters_clusters.sph > ! energy_0p5antiwaters.log

  python $scriptdir/dx-gist_make_centers_of_intensity.py gist-EswPlus2Eww_ref.dx -1 0.5 2 energy_-0p5waters >> log
  $DOCKBASE/proteins/pdbtosph/bin/pdbtosph energy_-0p5waters_clusters.pdb energy_-0p5waters_clusters.sph >> log
  sed -i 's/ 0\.700   / 1.400   /g' energy_-0p5waters_clusters.sph
  python $scriptdir/clusterEnergies_from_dx-sph.py gist-EswPlus2Eww_ref.dx energy_-0p5waters_clusters.sph > ! energy_-0p5waters.log
  #cp out0new_gist.dx out0new_gist-EswPlus2Eww_ref_energy_waters.dx


# merging individual pdbs into one:
# makes single pdb file with "MODEL" entries for PyMOl to thumb through out of the 4 pdbs that contain cluster centers at varying levels of X-times bulk density.
  echo "MODEL 1" > bulkdens_frames_mdl.pdb
  cat 05xbulkdens_clusters.pdb >> bulkdens_frames_mdl.pdb
  echo "ENDMDL \nMODEL 2" >> bulkdens_frames_mdl.pdb
  cat 10xbulkdens_clusters.pdb >> bulkdens_frames_mdl.pdb
  echo "ENDMDL \nMODEL 3" >> bulkdens_frames_mdl.pdb
  cat 20xbulkdens_clusters.pdb >> bulkdens_frames_mdl.pdb
  echo "ENDMDL \nMODEL 4" >> bulkdens_frames_mdl.pdb
  cat 50xbulkdens_clusters.pdb >> bulkdens_frames_mdl.pdb

# makes single pdb file with "MODEL" entries for PyMOl to thumb through out of the 4 pdbs that contain all points composing the clusters at varying levels of X-times bulk density.
  echo "MODEL 1" > bulkdens_points_mdl.pdb
  cat 05xbulkdens_points.pdb >> bulkdens_points_mdl.pdb
  echo "ENDMDL \nMODEL 2" >> bulkdens_points_mdl.pdb
  cat 10xbulkdens_points.pdb >> bulkdens_points_mdl.pdb
  echo "ENDMDL \nMODEL 3" >> bulkdens_points_mdl.pdb
  cat 20xbulkdens_points.pdb >> bulkdens_points_mdl.pdb
  echo "ENDMDL \nMODEL 4" >> bulkdens_points_mdl.pdb
  cat 50xbulkdens_points.pdb >> bulkdens_points_mdl.pdb

# makes single pdb file with "MODEL" entries for PyMOl to thumb through out of the 4 pdbs that contain Energies for each cluster center at varying levels of X-times bulk density.  
echo "MODEL 1" > clustEnergy_frames_mdl.pdb
  cat clustEnergy05xbulkdens_clusters.pdb >> clustEnergy_frames_mdl.pdb
  echo "ENDMDL \nMODEL 2" >> clustEnergy_frames_mdl.pdb
  cat clustEnergy10xbulkdens_clusters.pdb >> clustEnergy_frames_mdl.pdb
  echo "ENDMDL \nMODEL 3" >> clustEnergy_frames_mdl.pdb
  cat clustEnergy20xbulkdens_clusters.pdb >> clustEnergy_frames_mdl.pdb
  echo "ENDMDL \nMODEL 4" >> clustEnergy_frames_mdl.pdb
  cat clustEnergy50xbulkdens_clusters.pdb >> clustEnergy_frames_mdl.pdb

# consider making energy pdbs with MODEL entries for PyMOL. 

echo "Open pdbs in PyMOL \n pymol gist/010ii.gist_subsite_energetics/*pdb gist/007align_to_md/*pdb"

#   $DOCKBASE/proteins/pdbtosph/bin/pdbtosph one_center_of_energies.pdb one_center_of_energies.sph
#  sed -i 's/0.700    7/1.400    7/g' one_center_of_energies.sph
#  python ~/zzz.scripts/dx-gist_score_gist_sph.py loopC.EswPusEww.dx  one_center_of_energies.sph > ! one_center_of_energies.log
#  #cp out0new_gist.dx out0new_gist_loopC_one_center_of_energies.dx




