## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

#set workdir  = $mountdir/009.clustering_4.0_mod/cdc37/
#set workdir  = $mountdir/009.clustering_4.0_mod/complex/
#set workdir  = $mountdir/009.clustering_4.0_mod/HSP_dimer/
#set workdir  = $mountdir/009.clustering_4.0_mod/raf/
#set workdir  = $mountdir/009.clustering_4.0_mod/HSP_mon1/
#set workdir  = $mountdir/009.clustering_4.0_mod/HSP_mon2/
set workdir  = $mountdir/009.clustering_4.0_mod/SRC_loops/
#rm -rf $workdir
mkdir -p $workdir
cd $workdir


#ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#ls ../003md_tleap_new/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! cluster.in 
parm ${mountdir_ori}/0003md_tleap/com1.mmrc.leap.prm7
trajin ${mountdir}/007.com.dimer_0/com.nowat.mdcrd 1 last
trajin ${mountdir}/007.com.dimer_5/com.nowat.mdcrd 1 last
trajin ${mountdir}/007.com.dimer_50/com.nowat.mdcrd 1 last
trajin ${mountdir}/007.com.dimer_500/com.nowat.mdcrd 1 last
cluster C0 \
        hieragglo epsilon 4.0 clusters 20 complete \
        rms :291-301,932-942 nofit \
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
