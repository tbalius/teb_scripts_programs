## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


# set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C 
#set lig = DL2040 
set lig = DL2078 
set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"

#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
#set jobId = $temp:h:t
#echo $jobId
#set jid = $jobId


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd
pwd
ls ../../pose1/003md_tleap/com.leap.prm7
#ls ../../pose1/003md_tleap/

#exit

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! pca_complex.in 


#####################################################
# Visualize the fluctuations of the eigenmodes      #
# Read the file with the eigenvectores              #
#####################################################
readdata ../009.PCA_combined/evecs.dat name Evecs


#####################################################
# Load a topology                                   #
# This is necesary to create a new topology         #
# that will match the read in eigenmodes
#####################################################
#parm cpu/cpu.prmtop
parm ../../pose1/003md_tleap/com.leap.prm7
parmstrip !(:1-172&!@H=)
parmwrite out com.leap.noh.prmtop

#####################################################
# Create a NetCDF trajectory file with the          #
# modes of motion of the first PCA                  #
#####################################################
runanalysis modes name Evecs trajout eigan_mode1_traj.mdcrd \
pcmin -10 pcmax 10 tmode 1 trajoutmask :1-172&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-171&!@H= trajoutfmt mdcrd 
#runanalysis modes name Evecs trajout eigan_mode1_traj.nc \
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-172&!@H= trajoutfmt netcdf

runanalysis modes name Evecs trajout eigan_mode2_traj.mdcrd \
pcmin -10 pcmax 10 tmode 2 trajoutmask :1-172&!@H= trajoutfmt mdcrd 
#runanalysis modes name Evecs trajout eigan_mode2_traj.nc \
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-172&!@H= trajoutfmt netcdf

runanalysis modes name Evecs trajout eigan_mode3_traj.mdcrd \
pcmin -10 pcmax 10 tmode 3 trajoutmask :1-172&!@H= trajoutfmt mdcrd 
#runanalysis modes name Evecs trajout eigan_mode3_traj.nc \
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-172&!@H= trajoutfmt netcdf


#####################################################
# Now you can open the files:                       #
# cpu-gpu-modes.prmtop                              #
# cpu-gpu-modes.nc                                  #
# in Chimera / VMD and watch the movie              #
# which shows the first mode of motion              #
#####################################################
EOF

cat << EOF > qsub.csh
#!/bin/csh

$AMBERHOME/bin/cpptraj -i pca_complex.in > ! pca_complex.log #&

#python ${mountdir_ori}/plot_pca.py 
EOF

sbatch qsub.csh
#end
