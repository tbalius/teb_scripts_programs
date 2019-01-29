#!/bin/csh 

# TEB / MF comments -- March2017

## specific to amber14
## go through multipliers ...
## scripts run within seconds on cluster


#set mountdir = "/mnt/nfs/work/users/tbalius/Water_Project/run_DOCK3.7"
set mountdir = `pwd`

foreach subtraj ( \
 09md \
 10md \
 11md \
 12md \
 13md \
 14md \
 15md \
 16md \
 17md \
 18md \
)

set workdir  = $mountdir/gist/010b.subtraj_gist_combine/$subtraj
set filedir  = $mountdir/gist/008b.subtraj_gist/$subtraj
set scriptdir = $mountdir/GIST_DX_tools-master/src

rm -rf $workdir
mkdir -p $workdir
cd $workdir

ln -s $filedir/gist-dTSorient-dens.dx .
ln -s $filedir/gist-dTStrans-dens.dx .
ln -s $filedir/gist-Esw-dens.dx .
ln -s $filedir/gist-Eww-dens.dx .

# this is the density of the water.
ln -s $filedir/gist-gO.dx .

cat <<EOF >! qsub_${subtraj}.csh
#!/bin/csh 
#\$ -cwd
#\$ -j yes
#\$ -o stderr
#\$ -q all.q

  cd ${workdir}
 # make a combination of the grids
 # We think that we should be substracting
 # Remove comment from top of line

 # tip3p and amber 14

  set bulkE = "-9.533" # kcal/mol/water
  set numberdensity = "0.0334" # waters/(angstroms^3)
  set A14const1 = \`echo "scale=4; -1.0 * \${bulkE} * \${numberdensity}" | bc\`
  # -0.3184 should be positive -*- = +

  python ${scriptdir}/dx-combine_grids.py gist-Eww-dens.dx       1.0 gist-gO.dx               \${A14const1} 0.0 gist-dEww-dens_ref
  python ${scriptdir}/dx-combine_grids.py gist-Esw-dens.dx       1.0 gist-dEww-dens_ref.dx    1.0           0.0 gist-EswPlusEww_ref
  python ${scriptdir}/dx-combine_grids.py gist-dTSorient-dens.dx 1.0 gist-dTStrans-dens.dx    1.0           0.0 gist-TSsw
  python ${scriptdir}/dx-combine_grids.py gist-EswPlusEww_ref.dx 1.0 gist-TSsw.dx            -1.0           0.0 gist-Gtot1_ref

  python ${scriptdir}/dx-combine_grids.py gist-Esw-dens.dx        1.0 gist-dEww-dens_ref.dx   2.0           0.0 gist-EswPlus2Eww_ref 	#<<THIS GUY
  python ${scriptdir}/dx-combine_grids.py gist-EswPlus2Eww_ref.dx 1.0 gist-TSsw.dx           -1.0           0.0 gist-Gtot2_ref

  # apply density cutoff.
  #python ${scriptdir}/dx-density-threshold.py gist-EswPlusEww_ref2.dx gist-gO.dx 5.0 gist-EswPlusEww_ref2_threshold5.0

  # norm grids.
  #python ${scriptdir}/dx-divide_grids.py gist-Eww-dens.dx gist-gO.dx 0.0329 gist-Eww-norm
  #python ${scriptdir}/dx-combine_grids.py gist-Eww-norm.dx 1.0 gist-gO.dx 0.0 "-9.533" gist-Eww-norm-ref

EOF

qsub qsub_${subtraj}.csh 
#csh qsub_${subtraj}.csh 



end # subtraj

echo " gist-EswPlus2Eww_ref is the best GIST grid retrospectively for CcP and used for prospective docking in (Balius et al.). "
echo " gist-Gtot1_ref is the second best on CcP. "

