## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


# set mountdir  = `pwd`
set mountdir_ori = `pwd`
set mut = E37C 
set lig = DL2040 

foreach pose (   \
               1 \
#              2 \
#              3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
#cd $pwd


    set seed = "0"
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

set workdir  = $mountdir/${pdb}/006.rmsd_endref_${seed}/
rm -rf $workdir
mkdir -p $workdir
cd $workdir


ln -s ${mountdir}/${pdb}/004.MDrun_${seed}/${jobId} .

# Mg is 310.

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! rmsd.equil.prod.in 
parm $mountdir/003md_tleap/com.leap.prm7 
trajin $mountdir/007.com.rec.lig_0/com.nowat.mdcrd 1 10000
reference  $mountdir/007.com.rec.lig_0/com.nowat.mdcrd 10000 10000 [lastframe] 
rms backbone :1-169@CA,N,C,O ref [lastframe] out bb_fit.dat 
rms receptor :1-169,172 ref [lastframe] out rec_nofit.dat nofit 
rms gtp1     :171 ref [lastframe] out gtp1.dat nofit
rms lig1     :170 ref [lastframe] out lig1.dat nofit
rms lig1f    :170 ref [lastframe] out lig1_fit.dat
#trajout ref.pdb pdb
go
EOF

$AMBERHOME/bin/cpptraj -i rmsd.equil.prod.in > ! rmsd.log &

#end
end # poses
