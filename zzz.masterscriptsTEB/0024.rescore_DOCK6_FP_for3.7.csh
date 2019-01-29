#!/bin/csh
## Writen by Trent Balius; edited by TEB and Marcus Fischer 
## in the Shoichet Group, 2013
# runs actual footprint rescoring using DOCK6 (for dock3.7)
# takes about 1 hour (step where all grid-minimized ligands are minimized on receptor coords takes long)
# to check progress: 		grep "Name:" -c DOCK6_fp_rescore_3.7_frags/rec_min_out_scored.mol2
# this will give number of ligands processed out of 5000

  set name_noh_prefix = rec
  set name_prefix = rec_processed
  set lig_name_prefix = xtal-lig_processed

  set mountdir  = `pwd`
  set scriptdir = `pwd`
  set filedir = "/mnt/nfs/work/fischer/VDR/masterscriptsTEB"
  set procdir = "${mountdir}/DOCK6_pre-processing"		#from step 1
  set prepdir = "${mountdir}/DOCK6_prep"			#from step 2
  set hoptdir = "${mountdir}/DOCK6_hopt"			#from step 3
  #made in this step:
  set workdir = "${mountdir}/DOCK6_fp_rescore_3.7_frags"	# ***** CHANGE ME here and below (mol2) 
  #set workdir = "${mountdir}/DOCK6_fp_rescore_3.7_leads"
  #set workdir = "${mountdir}/DOCK6_fp_rescore_3.7_NP"

  rm -rf ${workdir}
  mkdir -p $workdir
  cd $workdir

# where "to-be-rescored" mol2 file is located
  #set mol2file = /nfs/home/fischer/work/VDR/tartedHis/vs_frags-now-marvin/top.1000.mol2
  set mol2file = ${mountdir}/vs_frags-now-marvin/top.5000.mol2		 # ***** CHANGE ME here and above (workdir)
  #set mol2file = ${mountdir}/vs_leads-now-marvin/top.5000.mol2 
  #set mol2file = ${mountdir}/vs_natural-products/top.5000.mol2 

# DOCK6 command to run on 10 (-np) processors with parallel DOCK6 (mpi version)...
  set DOCK = "/nfs/home/tbalius/zzz.programs/mpich/mpich-3.0.4_install/bin/mpirun -np 10 /nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/dock6.mpi"
# ... instead of standard serial DOCK
  #set DOCK = "/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/dock6"

  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/vdw_AMBER_parm99.defn .		# as before
  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex.defn .
  ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex_drive.tbl .

  ln -s ${procdir}/rec_processed.mol2 receptor.mol2 		# receptor file from step 1

  ln -s ${hoptdir}/hopt.fad.grid_scored.mol2 xtalmin.mol2	# FP reference from step 3 
								# ***** CHANGE THIS for alternative FP reference

  ln -s ${filedir}/zzz.inputs/grid.min.in .			# 3 standard input files needed to run DOCK
  ln -s ${filedir}/zzz.inputs/rec.min.in .
  ln -s ${filedir}/zzz.inputs/descriptor.sum1fp_euc.in .	# DOCK input file; Keep and eyeball on this -  may change in the future of dock development
  
# could use alternative references, e.g. frag of xtal-lig 
  #ln -s ${filedir}/zzz.inputs/frag1_descriptor.sum1fp_euc.in .	# alternative DOCK input file; would replace previous line
  #ln -s ${filedir}/zzz.inputs/frag2_descriptor.sum1fp_euc.in .
  #ln -s ${filedir}/zzz.inputs/frag3_descriptor.sum1fp_euc.in .
  #ln -s ${mountdir}/zzz.fp_references/${fp_refname}_frag1.mol2 frag1.mol2	# would then link new FP references accordingly
  #ln -s ${mountdir}/zzz.fp_references/${fp_refname}_frag2.mol2 frag2.mol2
  #ln -s ${mountdir}/zzz.fp_references/${fp_refname}_frag3.mol2 frag3.mol2

  ln -s ${prepdir}/$name_prefix.6_12.grid.nrg grid.nrg 			# 6-12 receptor grid files
  ln -s ${prepdir}/$name_prefix.6_12.grid.bmp grid.bmp 			
  cp  $mol2file ligands_for_grid_min.mol2
  sed -i "s/ 1     / 1 LIG /g" ligands_for_grid_min.mol2		# to write residue name missing from DOCK3.7 but required for DOCK6.6 


echo "run dock single point energy calculation"

cat <<EOF > script.csh
cd $workdir

echo "All ligands from previous screen are currently minimized on grid."
${DOCK} -i grid.min.in -o grid.min.out -v
ln -s  grid_min_out_scored.mol2 ligands_for_rec_min.mol2
echo "All grid-minimized ligands are currently minimized on receptor coords."
${DOCK} -i rec.min.in -o rec.min.out -v

ln -s rec_min_out_scored.mol2 ligands.mol2
echo "FP scores are calculated for all minimized ligands and the top1000 are being written out."
${DOCK} -i descriptor.sum1fp_euc.in -o descriptor.sum1fp_euc.out -v
EOF
#${DOCK} -i frag1_descriptor.sum1fp_euc.in -o frag1_descriptor.sum1fp_euc.out -v
#${DOCK} -i frag2_descriptor.sum1fp_euc.in -o frag2_descriptor.sum1fp_euc.out -v
#${DOCK} -i frag3_descriptor.sum1fp_euc.in -o frag3_descriptor.sum1fp_euc.out -v

csh script.csh &		# could do 'qsub script.csh' and define using 10 proc in script to run on queue


