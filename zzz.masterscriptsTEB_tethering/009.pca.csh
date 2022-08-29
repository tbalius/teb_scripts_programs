## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


# set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C 
#set lig = DL2040 
set lig = DL2078 
#set lig = DL1314_Protomer1 

#foreach pose (   \
#               1 \
#               2 \
#               3 \
#)
#set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/
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

set workdir  = $mountdir/${pdb}/009.PCA_combined/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! pca_complex.in 
parm ../../pose1/003md_tleap/com.leap.prm7
trajin ../../pose1/007.com.rec.lig_0/com.nowat.mdcrd 1 1000000
trajin ../../pose1/007.com.rec.lig_5/com.nowat.mdcrd 1 1000000
trajin ../../pose1/007.com.rec.lig_50/com.nowat.mdcrd 1 1000000

trajin ../../pose2/007.com.rec.lig_0/com.nowat.mdcrd 1 1000000
trajin ../../pose2/007.com.rec.lig_5/com.nowat.mdcrd 1 1000000
trajin ../../pose2/007.com.rec.lig_50/com.nowat.mdcrd 1 1000000

trajin ../../pose3/007.com.rec.lig_0/com.nowat.mdcrd 1 1000000
trajin ../../pose3/007.com.rec.lig_5/com.nowat.mdcrd 1 1000000
trajin ../../pose3/007.com.rec.lig_50/com.nowat.mdcrd 1 1000000

createcrd trajectories
run

#####################################################
# Calculate coordinate covariance matrix            #
#####################################################
crdaction trajectories matrix covar name covar_mat :1-172&!@H=

#####################################################
# Diagonalize coordinate covariance matrix          #
# Get first 3 eigenvectors                          #
#####################################################
runanalysis diagmatrix covar_mat out evecs.dat vecs 3 name myEvecs 
#runanalysis diagmatrix covar_mat out evecs.dat \
#vecs 3 name myEvecs \
#nmwiz nmwizvecs 3 nmwizfile dna.nmd nmwizmask :1-36&!@H=
crdaction trajectories projection evecs myEvecs :1-172&!@H= out project.dat beg 1 end 3
go
EOF

cat << EOF > qsub.csh
#!/bin/csh

$AMBERHOME/bin/cpptraj -i pca_complex.in > ! pca_complex.log #&

python ${mountdir_ori}/plot_pca.py project.dat > plot.log 
EOF

sbatch qsub.csh

#end
