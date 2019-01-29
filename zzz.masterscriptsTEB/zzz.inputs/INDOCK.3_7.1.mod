DOCK 3.7 parameter
##################################################### 
# NOTE: split_database_index is reserved to specify a list of files
ligand_atom_file               split_database_index #standard for docking large databases
#####################################################
#                             OUTPUT
#####################################################

output_file_prefix            test. #default, but can be changed

#####################################################
#                             MATCHING
#####################################################

match_method                  2 #1 matches up to the distance_tolerance below, ignoring match_goal, step, maximum, etc. 
                                #2 uses the adaptive sampling that attempts to get a number of match_goal orientational samples 
distance_tolerance            0.05 #starting distance tolerance
match_goal                    10000 #desired number of orientational samples to get before quitting under match_method = 2
distance_step                 0.05 #increment from distance_tolerance until max or match_goal is reached
distance_maximum              0.5 #biggest tolerance that will be used to attempt to get match_goal orientational samples
timeout                       1000.0 #number of seconds before quitting on any given ligand
nodes_maximum                 4 #max number of points for which all distances must be within the tolerance. 3 possible, 4 suggested.
nodes_minimum                 4 #min number of points for which all distances must be within the tolerance. 4 suggested, 3 possible.
bump_maximum                  500.0 #van der Waals score in kcal/mol for any part of the molecule to get before further examination stopped
bump_rigid                    500.0 #van der Waals score in kcal/mol for the rigid component of the ligand molecule, if above, discarded

#####################################################
#                             COLORING
#####################################################

chemical_matching             no #default to off, can use chemical matching from DOCK3.6 if desired
case_sensitive                no #case sensitivity for chemical matching groups

#####################################################
#                             SEARCH MODE
#####################################################

atom_minimum                  4   #minimum number of atoms in ligand for it to be scored
atom_maximum                  100 #maximum number of atoms in ligand for it to be scored
number_save                   1  #how many poses to save. Any number of poses can be saved, but disk space is a factor!
save_limit                    1000000 #only scores below (better than) this will have their poses saved. useful for speeding up prospective
                                      #runs, not recommended for retrospective tests as it can influence/hamper result processing.
#####################################################
#                             SCORING
#####################################################

ligand_desolvation            volume #use GB desolvation scoring, other options are full or none
vdw_maximum                   1.0e10 #maximum vdw score possible, prevents overflow
electrostatic_scale           1.0 #scaling factors to be applied to scores, likely not to be trifled with
vdw_scale                     1.0 #again, scales the entire vdw score.
internal_scale                0.0 #scales an internal focusing term. set this to 0 as this doesn't work at all/isn't implemented
per_atom_scores               no #change to yes if per-atom scoring breakdowns desired. note that this doubles output size.

#####################################################
# INPUT FILES / THINGS THAT CHANGE
#####################################################

receptor_sphere_file          dockblaster_run/sph/match2.sph #receptor matching spheres file following age old SPH format
vdw_parameter_file            dockblaster_run/grids/vdw.parms.amb.mindock #vdw parameter file.
flexible_receptor             no #describing only single receptor file for now
total_receptors               1 

############## grids/data for one receptor

rec_number                    1
rec_group                     1
rec_group_option              1
solvmap_file                  dockblaster_run/grids/solvmap_sev         #GB-based desolvation maps 
delphi_file                   dockblaster_run/grids/rec+sph.qnifft.phi #electrostatics map, size must be declared with delphi_nsize below
chemgrid_file                 dockblaster_run/grids/chem.vdw            #vdw grid file, contains vdw scores
bumpmap_file                  dockblaster_run/grids/chem.bmp            #vdw bump file, only used for header data for chemgrid_file 
delphi_nsize                  193                             #size of electrostatics grid (cubic). blastermaster.py trims to the minimum size necessary to save memory.

############## end of INDOCK
