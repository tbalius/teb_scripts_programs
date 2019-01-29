#!/bin/csh 

# This script runs Ryan's blastermaster python masterscript for generating everything that dock needs, i.e. grids, spheres
# Run on sgehead as jobs are submitted to the queue

# list is same as in 001... script 
set list = "1DB1"
#set list = `cat $1`
#set list = `cat /nfs/work/users/tbalius/VDR/Enrichment/pdblist_all `

set mountdir = `pwd`
#set mountdir = "/nfs/work/users/tbalius/VDR/"

# loop over all pdb(s)
foreach pdbname ( $list )

echo "${pdbname}"

set workdir = ${mountdir}/${pdbname}

# checks that 001 ran successfully and produced the directory structure as expected
# if not stops with current pdb code and continues with next one in list
  if ! ( -s $workdir ) then
     echo "$workdir does not exit"
     continue
  endif

cd $workdir

#cat xtal-lig_ori.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >  xtal-lig.pdb

# the following lines create a qsub script which submits blastermaster to the queue
cat <<EOF > qsub.csh
#!/bin/csh 
#\$ -cwd
#\$ -j yes
#\$ -o stderr
#\$ -q all.q
cd $workdir
$DOCK_BASE/src/blastermaster_1.0/blastermaster.py --addhOptions=" -HIS -FLIPs "  -v
EOF

qsub qsub.csh 

end # pdbname
# going to the next pdb

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
