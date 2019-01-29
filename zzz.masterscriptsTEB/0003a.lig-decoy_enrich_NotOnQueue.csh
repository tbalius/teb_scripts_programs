#!/bin/csh

#This script docks a DUD-e like ligand-decoy-database to evaluate the enrichment performance of actives over decoys
#It assumes that ligands and decoys have been pre-prepation (see script blablabla_ToDo) which needs to be run in SF.

# filedir is where your rec.pdb and xtal-lig.pdb and dockfiles directory live 
set filedir = "/mnt/nfs/work/fischer/VDR/gemini_tart3_gem_rs_sph"	#CHANGE THIS
# this is where the work is done:
set mountdir = $filedir				# Might CHANGE THIS
set dude_dir = "/mnt/nfs/work/fischer/VDR/lig-decoy-db"  # should contain decoy.smi and ligand.smi for ROC script 00005...csh
  ## TO DO - rename this outside in the dir structure and call in blbalbalbabla script
if (-s $dude_dir) then 
  echo " $dude_dir exist"
else
  # this is something to modified in future. 
  # probably better to exit if it is not there.
  echo "making a symbolic link:"
  echo "ln -s /mnt/nfs/work/fischer/VDR/27Jan2014_learningDOCKrgc/databases_all_xtal-ligand_decoy $dude_dir"
  ln -s /mnt/nfs/work/fischer/VDR/27Jan2014_learningDOCKrgc/databases_all_xtal-ligand_decoy $dude_dir
endif

# change if you want to use a different or consistent dock version
set dock = ${DOCK_BASE}/bin/Linux/dock3.7_flex/dock.csh

set list = "3O1D_tart3" 
#set list = `cat $1`
#set list = `cat file`
				# CHANGE THIS (pdbname)
foreach pdbname ( $list )

# creates "ligands" and "decoys" and has the aim to dock all of the subsets for those two
#foreach db_type ( "ligands" "decoys" )
foreach db_type ( "ligands" )

set workdir1 = "${mountdir}/${pdbname}/ligands-decoys/${db_type}"

mkdir -p  ${workdir1}
cd  ${workdir1} 
# puts dockfiles in the right relative-path that INDOCK file expects
ln -s $filedir/dockfiles .

set count = '1'

# loop over database files to put each into a seperate chunk
foreach dbfile (`ls $dude_dir/${db_type}/${db_type}*.db2.gz`)

echo $dbfile

set chunk = "chunk$count"

set workdir2 = ${workdir1}/$chunk

## so you don't blow away stuff
if ( -s $workdir2 ) then
   echo "$workdir2 exits"
   continue
endif

#rm -rf ${workdir}
mkdir -p ${workdir2}
cd ${workdir2}

# copy INDOCK file of choice in right location
#cp $filedir/zzz.dock3_input/INDOCK . 
#cp $filedir/INDOCK_match20K INDOCK
#cp $filedir/INDOCK_5k_TolerantClash INDOCK	# CHANGE THIS
cp $filedir/INDOCK .
 # modified the dock file using sed. here we change some key sampling parameters; sed -i changes input file internally (overwrites), -e changes file externally (pipes it to screen or into file if redirected)
 sed -i "s/bump_maximum                  50.0/bump_maximum                  500.0/g" INDOCK 
 sed -i "s/bump_rigid                    50.0/bump_rigid                    500.0/g" INDOCK 
 sed -i "s/check_clashes                 yes/check_clashes                 no/g" INDOCK 

ln -s $dbfile . 

set dbf = `ls *.gz`

echo "./$dbf"

# says what to dock and where it sits
echo "./$dbf" > split_database_index

# writes submission script that runs dock on the sgehead queue
cat <<EOF > DOCKING_${db_type}.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q all.q
#\$ -o stdout
#\$ -e stderr

cd ${workdir2}
echo "starting . . ."
date
echo $dock 
$dock
date
echo "finished . . ."

EOF

#qsub DOCKING_${db_type}.csh
csh DOCKING_${db_type}.csh
# alternatively if you don't want to run it on the queue but locally comment in this instead:
#csh DOCKING_${lig_type}.csh &

@ count = ${count} + 1 
# counter is chuch dir

end # dbfile
end # db_type
end # pdbname

