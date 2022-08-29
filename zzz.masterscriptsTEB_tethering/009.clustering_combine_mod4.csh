## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


  #set mountdir  = `pwd`
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


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/009.clustering_4.0_mod/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! cluster.in 
parm ${mountdir}/003md_tleap/lig.leap.prm7
trajin ${mountdir}/007.com.rec.lig_0/lig.mdcrd 1 1000000
trajin ${mountdir}/007.com.rec.lig_5/lig.mdcrd 1 1000000
trajin ${mountdir}/007.com.rec.lig_50/lig.mdcrd 1 1000000
cluster C0 \
        hieragglo epsilon 4.0 clusters 20 complete \
        rms :1 nofit \
        sieve 10 random \
        out cnumvtime.dat \
        sil Sil \
        summary summary.dat \
        info info.dat \
        cpopvtime cpopvtime.agr normframe \
        repout rep repfmt pdb \
        singlerepout singlerep.nc singlerepfmt netcdf \
        avgout Avg avgfmt restart
go
EOF


cat << EOF > qsub.csh
#!/bin/csh

$AMBERHOME/bin/cpptraj -i cluster.in > ! cluster.log #&
EOF

sbatch qsub.csh
#end
end # pose
