#!/bin/csh 

# This script runs Ryan's blastermaster python masterscript for generating everything that dock needs, i.e. grids, spheres
# Run on sgehead as jobs are submitted to the queue

# TEB/ MF -- March 2017

setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK" 
source /nfs/soft/python/envs/complete/latest/env.csh


set mountdir = `pwd`

set workdir = ${mountdir}/docking/1prep
set pramdir = ${mountdir}/for011.dockprep_parm_files


  if ( -s $workdir ) then
     echo "$workdir does exits"
     exit
  endif

mkdir -p $workdir
cd $workdir

ln -s $mountdir/gist/010a.full_gist_combine gistfiles 

cp $mountdir/gist/007align_to_md/rec_aligned.pdb .
cp $mountdir/gist/007align_to_md/lig_aligned.pdb .

cat rec_aligned.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | awk '{if($12 != "H"){print $0}}' | sed -e "s/HETATM/ATOM  /g" | sed -e 's/HEM/HM2/g' >!  rec.pdb

cat lig_aligned.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >  xtal-lig.pdb



# the following lines create a qsub script which submits blastermaster to the queue
cat <<EOF > qsub.csh
#!/bin/csh 
#\$ -cwd
#\$ -j yes
#\$ -o stderr
#\$ -q all.q

setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK" 
source /nfs/soft/python/envs/complete/latest/env.csh

cd $workdir
$DOCKBASE/proteins/blastermaster/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="$pramdir/reduce_wwPDB_het_dict_mod.txt" --chargeFile="$pramdir/amb_mod.crg.oxt" --vdwprottable="$pramdir/prot_mod.table.ambcrg.ambH" -v
EOF

qsub qsub.csh 


# this will produce two directories:
# 1) working - contains all input and output files that are generated; not needed afterwards but as a reference
# 2) dockfiles - contains everything that is needed to run dock (copied from working)
#    grids 
#    	trim.electrostatics.phi 
#    	vdw.vdw 
#    	vdw.bmp 
# 	ligand.desolv.heavy
# 	ligand.desolv.hydrogen
#    spheres
#    	matching_spheres.sph
