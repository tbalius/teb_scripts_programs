## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017

setenv AMBERHOME /home/baliuste/zzz.programs/amber/amber18
setenv DOCKBASE "/home/baliuste/zzz.github/DOCK"


#  set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
set lig = DL2078
#set lig = DL1314_Protomer1 

foreach pose (   \
               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $mountdir
#set pwd = $mountdir



set clustertype = "4.0_mod"
#set clustertype = "single_1.0_sieve10"

# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

#set workdir  = $mountdir/${pdb}/006.rmsd_${seed}/
#set workdir  = $mountdir/010.rmsd/
set workdir  = $mountdir/010.rmsd_${clustertype}/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


set clusterdir = ${mountdir}/009.clustering_${clustertype}

#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm ${mountdir}/003md_tleap/lig.leap.prm7 
trajin ${mountdir}/007.com.rec.lig_0/lig.mdcrd 1 100000
trajin ${mountdir}/007.com.rec.lig_5/lig.mdcrd 1 100000
trajin ${mountdir}/007.com.rec.lig_50/lig.mdcrd 1 100000
reference ${clusterdir}/rep.c0.pdb [ref] 
rms lig1     :1 ref [ref] out lig1.dat nofit
go
EOF

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd.log &

#end # seed
end # pose
