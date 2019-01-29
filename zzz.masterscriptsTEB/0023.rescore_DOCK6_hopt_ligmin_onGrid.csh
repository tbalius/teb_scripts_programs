## written by Trent E Balius; edited by TEB and Marcus Fischer
## Shoichet lab 2013-2014
# should just run, i.e. no changes should be required
# this is the script to prepare the xtal-lig footprint reference (minimizes hydrogens and ligand (both in presence of receptor)
# takes <10min)

  set name_noh_prefix = rec		#as before
  set name_prefix = rec_processed
  set lig_name_prefix = xtal-lig_processed

  set mountdir = `pwd`
  set filedir = "/mnt/nfs/work/fischer/VDR/masterscriptsTEB"  		# CHANGE THIS to point to input files (before in /nfs/work/tbalius/VDR/rescoring_with_dock6/zzz.inputs/)
  set procdir  = "${mountdir}/DOCK6_pre-processing"	#created in step 1
  set prepdir  = "${mountdir}/DOCK6_prep"		#created in step 2
  set workdir  = "${mountdir}/DOCK6_hopt"		#now created

  rm -rf ${workdir}
  mkdir $workdir
  cd $workdir

  set DOCK = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/dock6"				#make sure all these are right
  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/vdw_AMBER_parm99.defn .		#defines lig vdw radii
  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex.defn .			#defines lig torsions based on atomtypes
  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex_drive.tbl .		#defines dihedral angles to be sampled

  ln -s ${procdir}/$lig_name_prefix.mol2 ligand.mol2 		# ligand file
  ln -s ${procdir}/rec_processed.mol2 receptor.mol2 		# receptor file
  ln -s ${prepdir}/$name_prefix.grid.nrg grid.nrg 		# receptor grid file (vdw and elstat)
  ln -s ${prepdir}/$name_prefix.grid.bmp grid.bmp 		# receptor grid file (bump)

  ln -s ${filedir}/zzz.inputs/H_opt.flex.defn . 		# modified flex-def file to only sample polar Hs (i.e. hydroxyls)
  ln -s ${filedir}/zzz.inputs/hopt.fad.grid.in .		# dock input file for sampling only polar Hs in presence of receptor
  ln -s ${filedir}/zzz.inputs/xtalmin.1000iter-tether10.in .	# dock input file for 1000 step ligand minimization in presence of receptor

echo "run dock to optimize polar hydrogens"

# this only move the polar hydrogens on the ligand

${DOCK} -i hopt.fad.grid.in -o hopt.fad.grid.out
  ln -s hopt.fad.grid_scored.mol2 ligand_2.mol2

echo "run dock to aliviate clashes."
# will let the ligand molecule move, to aleviate clashs.  
${DOCK} -i xtalmin.1000iter-tether10.in -o xtalmin.1000iter-tether10.out


