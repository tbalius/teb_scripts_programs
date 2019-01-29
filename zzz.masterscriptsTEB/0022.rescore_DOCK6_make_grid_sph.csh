## written by Trent E Balius; edited by TEB and Marcus Fischer
## Shoichet lab 2013-2014
# should just run, i.e. no changes should be required
# runs all steps of DOCK6 input generation, i.e. we run: dms, sphgen, sphereselect, showbox and grid
# takes <5min

  set name_noh_prefix = rec				
  set name_prefix = rec_processed			#generated in previous step	
  set lig_name_prefix = xtal-lig_processed 		#generated in previous step

  set mountdir = `pwd`
  set procdir  = "${mountdir}/DOCK6_pre-processing"	#generated in previous step
  set workdir  = "${mountdir}/DOCK6_prep"		#working dir

  rm -rf ${workdir}
  mkdir $workdir
  cd $workdir  

  sed 's/HETATM/ATOM  /g' ${procdir}/${name_noh_prefix}.pdb > ${name_noh_prefix}.pdb	#copies adhering to file input expectations
  ln -s ${procdir}/${name_prefix}.pdb .			
  ln -s ${procdir}/${name_prefix}.mol2 .
  ln -s ${procdir}/${lig_name_prefix}.mol2 .

  echo ${name_prefix}
  set DMS = "/mnt/nfs/home/tbalius/zzz.svn/dockenv/trunk/private/dms"		# locations
  set SPH = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/sphgen"		# note: DOCK6 version of sphgen
  if ! ( -e ${name_prefix}.dms) then 		# not to overwrite
    echo "Run DMS"
    ${DMS} ${name_noh_prefix}.pdb -a -g dms.${name_prefix}.log -p -n -o ${name_prefix}.dms
  endif


  if ! ( -e ${name_prefix}.sph) then 		#not to overwrite

#generates input file for sphgen, see http://ringo.ams.sunysb.edu/index.php/2013_DOCK_tutorial_with_Orotodine_Monophosphate_Decarboxylase - Placing Spheres for explanation
cat << EOF > INSPH
${name_prefix}.dms
R
X
0.0
4.0
1.4
${name_prefix}.sph
EOF
    echo "Run Sphgen"
    ${SPH} 
  endif

 set SPHSEL = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/sphere_selector"	#grabs spheres close (5.0A) to ligand
 ${SPHSEL} ${name_prefix}.sph ${lig_name_prefix}.mol2 5.0
 mv selected_spheres.sph ${name_prefix}.5.0.sph


# draws a box with marginsize 8 around ligand spheres
cat << EOF > showbox.in 		
Y                        
8.0                      
${name_prefix}.5.0.sph   
1                        
${name_prefix}.box.pdb   
EOF

  showbox < showbox.in

# generates GRID 
 set GRID = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/grid"
ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/vdw_AMBER_parm99.defn .

#check if it hasnt been run, create input and run
if ! ( -e ${name_prefix}.grid.nrg ) then

echo "make grid"

# input file with 6-9 parameters
cat << EOF > ! grid.${name_prefix}.in
compute_grids                  yes
grid_spacing                   0.3
output_molecule                no
contact_score                  no
energy_score                   yes
energy_cutoff_distance         9999
atom_model                     a
attractive_exponent            6
repulsive_exponent             9
distance_dielectric            yes
dielectric_factor              4
bump_filter                    yes
bump_overlap                   0.75
receptor_file                  ${name_prefix}.mol2
box_file                       ${name_prefix}.box.pdb
vdw_definition_file            vdw_AMBER_parm99.defn
score_grid_prefix              ${name_prefix}.grid
EOF

# runs GRID with 6-9
${GRID} -i grid.${name_prefix}.in -o grid.${name_prefix}.out

# same input file but with 6-12 parameters
cat << EOF > ! grid.${name_prefix}.6_12.in
compute_grids                  yes
grid_spacing                   0.3
output_molecule                no
contact_score                  no
energy_score                   yes
energy_cutoff_distance         9999
atom_model                     a
attractive_exponent            6
repulsive_exponent             12
distance_dielectric            yes
dielectric_factor              4
bump_filter                    yes
bump_overlap                   0.75
receptor_file                  ${name_prefix}.mol2
box_file                       ${name_prefix}.box.pdb
vdw_definition_file            vdw_AMBER_parm99.defn
score_grid_prefix              ${name_prefix}.6_12.grid
EOF

# runs GRID with 6-12
${GRID} -i grid.${name_prefix}.6_12.in -o grid.${name_prefix}.6_12.out

endif

