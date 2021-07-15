## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


  set mountdir  = `pwd`

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"

set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set jobId = $temp:h:t
echo $jobId
set jid = $jobId


# set workdir   = $mountdir/004.MDrun/${lig}/${jid}_plots

set workdir  = $mountdir/${pdb}/009.clustering_${seed}/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

ls ../003md_tleap/com.leap.prm7 ../007.com.rec.lig_${seed}/com.nowat.mdcrd

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm ../003md_tleap/com.leap.prm7
trajin ../007.com.rec.lig_${seed}/com.nowat.mdcrd 1 1000000
cluster C0 \
        dbscan minpoints 25 epsilon 0.9 sievetoframe \
        rms :169 nofit \
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

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd.log &

#end
