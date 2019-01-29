
# script that modifies INDOCK file to include GIST parameters 
# will update INDOCK file, so first we back it up to _nogist
# then apply patch and call it _gist

# TEB/ MF -- March 2017

cd flex/2prep


cat << EOF > gist.patch
--- INDOCK	2017-03-07 10:32:01.564704546 -0800
+++ INDOCK_gist	2017-03-07 10:31:06.673064360 -0800
@@ -36,6 +36,7 @@
 ligand_desolvation            volume
 vdw_maximum                   1.0e10
 electrostatic_scale           1.0
+gist_scale                   -1.0
 vdw_scale                     1.0
 internal_scale                0.0
 per_atom_scores               no
@@ -82,6 +83,7 @@
 solvmap_file                  ../dockfiles/1/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/1/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/1/trim.electrostatics.phi
+gist_file                     ../gistfiles/gist-EswPlus2Eww_ref.dx
 chemgrid_file                 ../dockfiles/1/vdw.vdw
 bumpmap_file                  ../dockfiles/1/vdw.bmp
 ############## grids/data for one receptor
@@ -97,6 +99,7 @@
 solvmap_file                  ../dockfiles/2/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/2/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/2/trim.electrostatics.phi
+gist_file                     0 
 chemgrid_file                 ../dockfiles/2/vdw.vdw
 bumpmap_file                  ../dockfiles/2/vdw.bmp
 ############## grids/data for one receptor
@@ -112,6 +115,7 @@
 solvmap_file                  ../dockfiles/3/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/3/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/3/trim.electrostatics.phi
+gist_file                     0 
 chemgrid_file                 ../dockfiles/3/vdw.vdw
 bumpmap_file                  ../dockfiles/3/vdw.bmp
 ############## grids/data for one receptor
@@ -127,6 +131,7 @@
 solvmap_file                  ../dockfiles/4/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/4/ligand.desolv.hydrogen
 delphi_file                   0
+gist_file                     0 
 chemgrid_file                 ../dockfiles/4/vdw.vdw
 bumpmap_file                  ../dockfiles/4/vdw.bmp
 ############## grids/data for one receptor
@@ -142,6 +147,7 @@
 solvmap_file                  ../dockfiles/5/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/5/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/5/trim.electrostatics.phi
+gist_file                     0 
 chemgrid_file                 ../dockfiles/5/vdw.vdw
 bumpmap_file                  ../dockfiles/5/vdw.bmp
 ############## grids/data for one receptor
@@ -157,6 +163,7 @@
 solvmap_file                  ../dockfiles/6/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/6/ligand.desolv.hydrogen
 delphi_file                   0
+gist_file                     0 
 chemgrid_file                 ../dockfiles/6/vdw.vdw
 bumpmap_file                  ../dockfiles/6/vdw.bmp
 ############## grids/data for one receptor
@@ -172,6 +179,7 @@
 solvmap_file                  ../dockfiles/7/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/7/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/7/trim.electrostatics.phi
+gist_file                     0 
 chemgrid_file                 ../dockfiles/7/vdw.vdw
 bumpmap_file                  ../dockfiles/7/vdw.bmp
 ############## grids/data for one receptor
@@ -187,6 +195,7 @@
 solvmap_file                  ../dockfiles/8/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/8/ligand.desolv.hydrogen
 delphi_file                   0
+gist_file                     0 
 chemgrid_file                 ../dockfiles/8/vdw.vdw
 bumpmap_file                  ../dockfiles/8/vdw.bmp
 ############## grids/data for one receptor
@@ -202,6 +211,7 @@
 solvmap_file                  ../dockfiles/9/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/9/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/9/trim.electrostatics.phi
+gist_file                     0 
 chemgrid_file                 ../dockfiles/9/vdw.vdw
 bumpmap_file                  ../dockfiles/9/vdw.bmp
 ############## end of INDOCK
EOF

cp INDOCK INDOCK_nogist
patch < gist.patch 
mv INDOCK INDOCK_gist
#cp INDOCK_nogist INDOCK


