## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

# set mountdir  = `pwd`
#set mut = E37C 
#set lig = DL2040 
#set lig = DL2078 
#set lig = 228354851 
#set lig = mol016 
#set lig = FNL-1615 


#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
#set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/
#cd $mountdir

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

#set workdir  = $mountdir/${pdb}/009.PCA_combined/cdc37/
set workdir  = $mountdir/${pdb}/009.PCA_combined/complex/
#set workdir  = $mountdir/${pdb}/009.PCA_combined/HSP_dimer/
#set workdir  = $mountdir/${pdb}/009.PCA_combined/HSP_mon1/
#set workdir  = $mountdir/${pdb}/009.PCA_combined/HSP_mon2/
#set workdir  = $mountdir/${pdb}/009.PCA_combined/SRC_loops/
#set workdir  = $mountdir/${pdb}/009.PCA_combined/raf/
#rm -rf $workdir
#mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! pca_complex.in 
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ${mountdir}/0007.com.rec.lig_0/com.1.nowat.mdcrd 1 last
trajin ${mountdir}/0007.com.rec.lig_5/com.1.nowat.mdcrd 1 last
trajin ${mountdir}/0007.com.rec.lig_50/com.1.nowat.mdcrd 1 last
trajin ${mountdir}/0007.com.rec.lig_500/com.1.nowat.mdcrd 1 last


createcrd trajectories
run

#####################################################
# Calculate coordinate covariance matrix            #
#####################################################
#crdaction trajectories matrix covar name covar_mat :291-301,932-942&!@H=
crdaction trajectories matrix covar name covar_mat :1-640,642-1281,1284-1554&!@H=
#crdaction trajectories matrix covar name covar_mat :1470-1554&!@H=
#crdaction trajectories matrix covar name covar_mat :1-640,642-1281&!@H=
#crdaction trajectories matrix covar name covar_mat :1-640&!@H=
#crdaction trajectories matrix covar name covar_mat :642-1281&!@H=
#crdaction trajectories matrix covar name covar_mat :1284-1469&!@H=

#####################################################
# Diagonalize coordinate covariance matrix          #
# Get first 20 eigenvectors                         #
#####################################################
runanalysis diagmatrix covar_mat out evecs.dat vecs 20 name myEvecs 
#runanalysis diagmatrix covar_mat vecs 3 name myEvecs \
#nmwiz nmwizvecs 3 nmwizfile complex.nmd nmwizmask :1-640,642-1281,1284-1554&!@H=
crdaction trajectories projection evecs myEvecs :1-640,642-1281,1284-1554&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :1284-1469&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :642-1281&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :1-640&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :1-640,642-1281&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :1470-1554&!@H= out project.dat beg 1 end 20
#crdaction trajectories projection evecs myEvecs :291-301,932-942&!@H= out project.dat beg 1 end 20
go
EOF

cat << EOF > qsub.csh
#!/bin/csh

#$AMBERHOME/bin/cpptraj -i pca_complex.in > ! pca_complex_NMD.log #&
$AMBERHOME/bin/cpptraj -i pca_complex.in > ! pca_complex.log #&

python ${scriptdir}/plot_pca.py project.dat > plot.log 
EOF

sbatch qsub.csh

#end
