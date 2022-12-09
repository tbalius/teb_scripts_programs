#!/usr/bin/python
# Written by Trent Balius (shoichet lab, 2016) 


import os, shutil 


#def make_dir(workdir,ligmol2,recmol2,recdms):
def make_dir(workdir,ligmol2,recmol2):
    # make sure the workdir does not exist.
    if(os.path.isdir(workdir)):
       print( workdir+ " exists!")
       exit()
    # make sure all files exist.
    if not(os.path.exists(ligmol2)):
       print(ligmol2 + "does not exist. ")
       exit()
    if not(os.path.exists(recmol2)):
       print (recmol2 + "does not exist. ")
       exit()
    #if not(os.path.exists(recdms)):
    #   print recdms + "does not exist. "
    #   exit()
    # make workdir. change dir to workdir
    os.mkdir(workdir)
    os.chdir(workdir)
    # copy file into workdir 
    shutil.copyfile(ligmol2, "xtal-lig.mol2")
    shutil.copyfile(recmol2,"rec.mol2")
    #shutil.copyfile(recdms, "rec.dms")

def dms_run():
    recmol2="rec.mol2"
    recpdb="rec.pdb"
    recdms="rec.dms"
    obabel = "/usr/bin/obabel"
    obabel_cmd = obabel+" -d -imol2 "+recmol2+' -opdb -O '+recpdb
    print(obabel_cmd)
    os.system(obabel_cmd)
    dms = "/home/baliuste_nih_gov/zzz.programs/DOCK-master/ucsfdock/proteins/dms/bin/dms"
    #dms = "/home/baliuste_nih_gov_nih_gov/test/dms/src/dms"
    dms_cmd = dms +" "+ recpdb + " -a -d 0.2 -g dms.log -p -n -o " + recdms
    print(dms_cmd)
    os.system(dms_cmd)
    
    


def dockprep():
    DOCKPATH = "/home/baliuste_nih_gov/zzz.programs/dock6/"
    ligfile = "xtal-lig.mol2"
    recdms = "rec.dms"
    #recpdb = "rec.pdb"
    name = "rec"
    # step one generate spheres.
    SPH = DOCKPATH+"/bin/sphgen"

    dms_run()

    file1 = open('INSPH','w')
    file1.write("rec.dms\nR\nX\n0.0\n4.0\n1.0\nrec.sph\n")
    file1.close()
    print ("Run Sphgen")
    os.system(SPH)


    SPHSEL = DOCKPATH+"/bin/sphere_selector"
    os.system(SPHSEL + " rec.sph " +ligfile+" 5.0")
    shutil.copyfile("selected_spheres.sph", "rec.5.0.sph")

    # step two generate grids
    file2 = open('showbox.in','w')
    file2.write("Y\n8.0\nrec.5.0.sph\n1\nrec.box.pdb\n")
    file2.close()
    showbox = DOCKPATH+"/bin/showbox"
    os.system(showbox +' < showbox.in')

    GRID = DOCKPATH+"/bin/grid"
    shutil.copyfile(DOCKPATH + "/parameters/vdw_AMBER_parm99.defn", "vdw_AMBER_parm99.defn") 

    file3 = open('grid.rec.6_12.in','w')
    file3.write("compute_grids                  yes\n")
    file3.write("grid_spacing                   0.3\n")
    file3.write("output_molecule                no\n")
    file3.write("contact_score                  no\n")
    file3.write("energy_score                   yes\n")
    file3.write("energy_cutoff_distance         9999\n")
    file3.write("atom_model                     a\n")
    file3.write("attractive_exponent            6\n")
    file3.write("repulsive_exponent             12\n")
    file3.write("distance_dielectric            yes\n")
    file3.write("dielectric_factor              4\n")
    file3.write("bump_filter                    yes\n")
    file3.write("bump_overlap                   0.75\n")
    file3.write("receptor_file                  %s.mol2\n"%name)
    file3.write("box_file                       %s.box.pdb\n"%name)
    file3.write("vdw_definition_file            vdw_AMBER_parm99.defn\n")
    file3.write("score_grid_prefix              rec.6_12.grid\n")
    file3.close()
    os.system(GRID + " -i grid.rec.6_12.in -o grid..out")

def dock():
    DOCKPATH = "/home/baliuste_nih_gov/zzz.programs/dock6/"
    DOCK = DOCKPATH+"/bin/dock6"
    file = open('dock.in','w')
    
    shutil.copyfile("xtal-lig.mol2","ligand.mol2")
    #shutil.copyfile(DOCKPATH + "/parameters/vdw_AMBER_parm99.defn", "vdw_AMBER_parm99.defn") 
    shutil.copyfile(DOCKPATH + "/parameters/flex_drive.tbl", "flex_drive.tbl") 
    shutil.copyfile(DOCKPATH + "/parameters/flex.defn", "flex.defn") 

     
    file.write("ligand_atom_file                                             ligand.mol2\n")
    file.write("limit_max_ligands                                            no\n")
    file.write("skip_molecule                                                no\n")
    file.write("read_mol_solvation                                           no\n")
    file.write("calculate_rmsd                                               yes\n")
    file.write("use_rmsd_reference_mol                                       no\n")
    file.write("use_database_filter                                          no\n")
    file.write("orient_ligand                                                yes\n")
    file.write("automated_matching                                           yes\n")
    file.write("receptor_site_file                                           rec.5.0.sph\n")
    file.write("max_orientations                                             1000\n")
    file.write("critical_points                                              no\n")
    file.write("chemical_matching                                            no\n") 
    file.write("use_ligand_spheres                                           no\n")
    file.write("use_internal_energy                                          yes\n")
    file.write("internal_energy_rep_exp                                      12\n")
    file.write("flexible_ligand                                              yes\n")
    file.write("user_specified_anchor                                        no\n")
    file.write("limit_max_anchors                                            no\n")
    file.write("min_anchor_size                                              5\n")
    file.write("pruning_use_clustering                                       yes\n")
    file.write("pruning_max_orients                                          1000\n")
    file.write("pruning_clustering_cutoff                                    100\n")
    file.write("pruning_conformer_score_cutoff                               100.0\n")
    file.write("use_clash_overlap                                            no\n")
    file.write("write_growth_tree                                            no\n")
    file.write("bump_filter                                                  no\n")
    file.write("score_molecules                                              yes\n")
    file.write("contact_score_primary                                        no\n")
    file.write("contact_score_secondary                                      no\n")
    file.write("grid_score_primary                                           yes\n")
    file.write("grid_score_secondary                                         no\n")
    file.write("grid_score_rep_rad_scale                                     1\n")
    file.write("grid_score_vdw_scale                                         1\n")
    file.write("grid_score_es_scale                                          1\n")
    file.write("grid_score_grid_prefix                                       rec.6_12.grid\n")
    file.write("multigrid_score_secondary                                    no\n")
    file.write("dock3.5_score_secondary                                      no\n")
    file.write("continuous_score_secondary                                   no\n")
    file.write("descriptor_score_secondary                                   no\n")
    file.write("gbsa_zou_score_secondary                                     no\n")
    file.write("gbsa_hawkins_score_secondary                                 no\n")
    file.write("SASA_descriptor_score_secondary                              no\n")
    file.write("amber_score_secondary                                        no\n")
    file.write("minimize_ligand                                              yes\n")
    file.write("minimize_anchor                                              yes\n")
    file.write("minimize_flexible_growth                                     yes\n")
    file.write("use_advanced_simplex_parameters                              no\n")
    file.write("simplex_max_cycles                                           1\n")
    file.write("simplex_score_converge                                       0.1\n")
    file.write("simplex_cycle_converge                                       1.0\n")
    file.write("simplex_trans_step                                           1.0\n")
    file.write("simplex_rot_step                                             0.1\n")
    file.write("simplex_tors_step                                            10.0\n")
    file.write("simplex_anchor_max_iterations                                500\n")
    file.write("simplex_grow_max_iterations                                  500\n")
    file.write("simplex_grow_tors_premin_iterations                          0\n")
    file.write("simplex_random_seed                                          0\n")
    file.write("simplex_restraint_min                                        no\n")
    file.write("atom_model                                                   all\n")
    file.write("vdw_defn_file                                                vdw_AMBER_parm99.defn\n")
    file.write("flex_defn_file                                               flex.defn\n")
    file.write("flex_drive_file                                              flex_drive.tbl\n")
    file.write("ligand_outfile_prefix                                        flex.dock2grid\n")
    file.write("write_orientations                                           no\n")
    file.write("num_scored_conformers                                        5000\n")
    file.write("write_conformations                                          no\n")
    file.write("cluster_conformations                                        yes\n")
    file.write("cluster_rmsd_threshold                                       2.0\n")
    file.write("rank_ligands                                                 no\n")
    file.close()
    os.system(DOCK + " -i dock.in -o dock.out -v")

def redock():
    DOCKPATH = "/home/baliuste_nih_gov/zzz.programs/dock6/"
    DOCK = DOCKPATH+"/bin/dock6"
    if not (os.path.exists("dock_mod.in")):
        print ("dock_mod.in does not exist. make a dock_mod.in files before running")
        return
    os.system(DOCK + " -i dock_mod.in -o dock_mod.out -v")


#dockprep()
#dock()
#redock()
