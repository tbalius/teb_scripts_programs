#!/bin/csh 
## this script was written by Trent Balius in the Shoichet Group, 2014

# This shell script will do the following:
#
# calculate rmsd with DOCK6 from DOCK3.7 run
#

#set mountdir = `pwd`
set mountdir = `pwd`
set filedir  = "$mountdir/../" 
#set DOCK = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/dock6"
set DOCK6 = "/mnt/nfs/home/tbalius/zzz.programs/dock6.6_mod3/dock6/bin/dock6"

set PDBid = "4NVA"
set typelist = "_gist _gist_elstat0p9 _min _nogist"
#set dockingtype = "gist_Esw_plus_Eww_ref2_coarse2"


foreach dockingtype ($typelist)
#foreach dockingtype (\
#  gist-EswPlusEww_ref2_all_spheres \
 #gist-EswPlusEww_ref2_scale2.0 \
#  standard_all_spheres \
 #standard \
 #standard_sph_1 \
#)

cd $mountdir/workingdir/smiles/

#set list = `cat pdblist `
set list = `awk '{print $1}' pdblig_to_zincname.txt `
#set list = " 25T " 

#foreach pdbcode ($list)
#set ligcode = `awk '/ATOM/{print $4}' $mountdir/workingdir/$pdbname/xtal-lig.pdb | sort -u`
foreach ligcode ($list)

set zincid  = `awk '{if($1=="'$ligcode'"){if (count == 0) {printf "%.12s ", $2; count=count+1}}}' $mountdir//workingdir/smiles/pdblig_to_zincname.txt`
set pdbcodes = `awk '{if($2=="'$ligcode'"){printf "%.4s ",$1}}' $mountdir/workingdir/smiles/ligcode_to_pdb.txt`

#there may be more than one pdb code per ligand name
foreach pdbcode ($pdbcodes)

#foreach conf ( "A" "B" "C" "D" ) 

#set workdir = $mountdir/workingdir_mod/DOCKING_${dockingtype}/rmsd_${pdbcode}_CcP_$conf
set workdir = $mountdir/workingdir/$PDBid$dockingtype/rmsd_${pdbcode}
rm -rf $workdir
mkdir -p $workdir
cd $workdir

 ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/vdw_AMBER_parm99.defn .
 ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex.defn .
 ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex_drive.tbl .
 #ln -s $mountdir/workingdir_mod/align_${pdbcode}/aligned.lig.pdb lig.pdb
 ln -s $mountdir/workingdir/align_${pdbcode}/aligned.lig.pdb lig.pdb

 /nfs/soft/openbabel/current/bin/obabel -ipdb lig.pdb -omol2 -O referencebefore_dockprep.mol2 -d

 echo $zincid
# ls -l  $filedir/workingdir/align_CcP_$conf/DOCKING_${dockingtype}/ligands/postDOCKING/poses.mol2
# ln -s ${filedir}/workingdir/align_CcP_$conf/DOCKING_${dockingtype}/ligands/postDOCKING/poses.mol2 vs_poses.mol2
 ls -l $filedir/docking/2runEnrich/PDBid$dockingtype/ligands/allChunksCombined/poses.mol2
 ln -s $filedir/docking/2runEnrich/PDBid$dockingtype/ligands/allChunksCombined/poses.mol2 vs_poses.mol2

 ln -s $mountdir/get_mol2_zinc_id.py .
 ln -s $mountdir/replace_sybel_with_ele.py .
 python get_mol2_zinc_id.py vs_poses.mol2 "$zincid" pose.mol2
 sed -i 's/ 1      / 1  LIG1 /g' pose.mol2

 /nfs/soft/openbabel/current/bin/obabel -imol2 pose.mol2 -omol2 -O pose_noh.mol2 -d

 mv pose_noh.mol2 pose_noh_type.mol2
 mv referencebefore_dockprep.mol2 referencebefore_dockprep_type.mol2
 python replace_sybel_with_ele.py pose_noh_type.mol2 pose_noh.mol2
 python replace_sybel_with_ele.py referencebefore_dockprep_type.mol2 referencebefore_dockprep.mol2 

# this is spesific for dock6.6 with break with dock6.8
#touch rmsd.in
cat << EOF > rmsd.in
ligand_atom_file                                             pose_noh.mol2
limit_max_ligands                                            no
skip_molecule                                                no
read_mol_solvation                                           no
calculate_rmsd                                               yes
use_rmsd_reference_mol                                       yes
rmsd_reference_filename                                      referencebefore_dockprep.mol2
use_database_filter                                          no
orient_ligand                                                no
use_internal_energy                                          no
flexible_ligand                                              no
bump_filter                                                  no
score_molecules                                              no
atom_model                                                   all
vdw_defn_file                                                vdw_AMBER_parm99.defn
flex_defn_file                                               flex.defn
flex_drive_file                                              flex_drive.tbl
ligand_outfile_prefix                                        rmsdcalc
write_orientations                                           no
num_scored_conformers                                        1
rank_ligands                                                 no
EOF

$DOCK6 -i rmsd.in -o rmsd.out


end # pdbcode
#end # conf
end # pdbcode or ligcode
end # dockingtype
