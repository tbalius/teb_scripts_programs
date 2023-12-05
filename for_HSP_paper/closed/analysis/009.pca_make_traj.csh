## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

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

#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/cdc37
#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/complex
#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/HSP_dimer
#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/HSP_mon1
#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/HSP_mon2
#set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/raf
set workdir  = $mountdir/${pdb}/009.PCA_combined_mode_traj/SRC_loops
#rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd
pwd
ls ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
#ls ../../pose1/003md_tleap/

#exit

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! pca_complex.in 


#####################################################
# Visualize the fluctuations of the eigenmodes      #
# Read the file with the eigenvectores              #
#####################################################
#readdata ${mountdir}/009.PCA_combined/complex/evecs.dat name Evecs
#readdata ${mountdir}/009.PCA_combined/cdc37/evecs.dat name Evecs
#readdata ${mountdir}/009.PCA_combined/HSP_dimer/evecs.dat name Evecs
#readdata ${mountdir}/009.PCA_combined/HSP_mon1/evecs.dat name Evecs
#readdata ${mountdir}/009.PCA_combined/HSP_mon2/evecs.dat name Evecs
#readdata ${mountdir}/009.PCA_combined/raf/evecs.dat name Evecs
readdata ${mountdir}/009.PCA_combined/SRC_loops/evecs.dat name Evecs


#####################################################
# Load a topology                                   #
# This is necesary to create a new topology         #
# that will match the read in eigenmodes            #
#####################################################
#parm cpu/cpu.prmtop
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
#parmstrip !(:1-640,642-1281,1284-1554&!@H=)
#parmstrip !(:1-640,642-1281&!@H=)
#parmstrip !(:642-1281&!@H=)
parmstrip !(:291-301,932-942&!@H=)
#parmstrip !(:1-640&!@H=)
#parmstrip !(:1284-1469&!@H=)
#parmstrip !(:1470-1554&!@H=)
parmwrite out com.leap.noh.prmtop

#####################################################
# Create a NetCDF trajectory file with the          #
# modes of motion of the first PCA                  #
#####################################################
runanalysis modes name Evecs trajout eigan_mode1_traj.mdcrd \
pcmin -100 pcmax 100 tmode 1 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-640&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-1280&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-85&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-1551&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-1554&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-85&!@H= trajoutfmt mdcrd 
#pcmin -10 pcmax 10 tmode 1 trajoutmask :1-467,469-964&!@H= trajoutfmt mdcrd 
#runanalysis modes name Evecs trajout eigan_mode1_traj.nc \
#pcmin -100 pcmax 100 tmode 1 trajoutmask :1-172&!@H= trajoutfmt netcdf

runanalysis modes name Evecs trajout eigan_mode2_traj.mdcrd \
pcmin -100 pcmax 100 tmode 2 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-640&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-1280&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-85&!@H= trajoutfmt mdcrd
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-1551&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-85&!@H= trajoutfmt mdcrd 
#pcmin -10 pcmax 10 tmode 2 trajoutmask :1-467,469-964&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-1554&!@H= trajoutfmt mdcrd 
#runanalysis modes name Evecs trajout eigan_mode2_traj.nc \
#pcmin -100 pcmax 100 tmode 2 trajoutmask :1-172&!@H= trajoutfmt netcdf

runanalysis modes name Evecs trajout eigan_mode3_traj.mdcrd \
pcmin -100 pcmax 100 tmode 3 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-640&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-1280&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-85&!@H= trajoutfmt mdcrd
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-22&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-85&!@H= trajoutfmt mdcrd
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-1551&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-186&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-85&!@H= trajoutfmt mdcrd 
#pcmin -10 pcmax 10 tmode 3 trajoutmask :1-467,469-964&!@H= trajoutfmt mdcrd 
#pcmin -100 pcmax 100 tmode 3 trajoutmask :1-1554&!@H= trajoutfmt mdcrd 
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
#SBATCH --partition=norm

$AMBERHOME/bin/cpptraj -i pca_complex.in > ! pca_complex.log #&

#python ${mountdir_ori}/plot_pca.py 
EOF

sbatch qsub.csh
#end
