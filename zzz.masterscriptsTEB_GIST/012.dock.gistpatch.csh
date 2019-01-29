
# script that modifies INDOCK file to include GIST parameters 
# will update INDOCK file, so first we back it up to _nogist
# then apply patch and call it _gist

# TEB/ MF -- March 2017

cd docking/1prep

set nominparmflag = 'F'

if (nominparmflag == 'T') then
cat << EOF > minparm.patch
--- INDOCK	2017-03-03 16:24:11.228826066 -0800
+++ INDOCK_min	2017-03-06 11:25:58.425345398 -0800
@@ -51,6 +51,16 @@
 ang2_range                    10.0
 ang1_step                     2.5
 ang2_step                     2.5
+##################################################### 
+#                    MINIMIZATION
+minimize                      no
+sim_itmax                     500
+sim_trnstep                   0.2
+sim_rotstep                   5.0
+sim_need_to_restart           1.0
+sim_cnvrge                    0.1
+min_cut                       1.0e15
+iseed                         777
 #####################################################
 # INPUT FILES / THINGS THAT CHANGE
 receptor_sphere_file          ../dockfiles/matching_spheres.sph
EOF
cp INDOCK INDOCK_ori
patch < minparm.patch 
endif


cat << EOF > gist.patch
--- INDOCK	2017-03-06 11:27:24.376904919 -0800
+++ INDOCK_gist	2017-03-06 11:33:37.519015401 -0800
@@ -36,6 +36,7 @@
 ligand_desolvation            volume
 vdw_maximum                   1.0e10
 electrostatic_scale           1.0
+gist_scale                   -1.0
 vdw_scale                     1.0
 internal_scale                0.0
 per_atom_scores               no
@@ -75,6 +76,7 @@
 solvmap_file                  ../dockfiles/ligand.desolv.heavy
 hydrogen_solvmap_file         ../dockfiles/ligand.desolv.hydrogen
 delphi_file                   ../dockfiles/trim.electrostatics.phi
+gist_file                     ../gistfiles/gist-EswPlus2Eww_ref.dx
 chemgrid_file                 ../dockfiles/vdw.vdw
 bumpmap_file                  ../dockfiles/vdw.bmp
 ############## end of INDOCK
EOF

cp INDOCK INDOCK_nogist
patch < gist.patch 
mv INDOCK INDOCK_gist
#cp INDOCK_nogist INDOCK

echo "For minimization: \n cp docking/1prep/INDOCK_nogist docking/1prep/INDOCK_min \n vi docking/1prep/INDOCK_min \n change line from no to yes"

