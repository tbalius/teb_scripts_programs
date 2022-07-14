#!/bin/csh 

# This script runs Ryan's blastermaster python masterscript for generating everything that dock needs, i.e. grids, spheres
# Run on sgehead as jobs are submitted to the queue

# list is same as in 001... script 
#set list = "3AZ2"
#set list = `ls snapshot_*.pdb | sed -e 's/.pdb//g'` # or use `cat filename` to list your pdb codes here from a text file like pdblist_rat, to loop over each variable (pdb code) later
#set list = `cat $1`
#set list = `cat /nfs/work/users/tbalius/VDR/Enrichment/pdblist_all `

set mountdir = `pwd`
#set mountdir = "/nfs/work/users/tbalius/VDR/"

## move the dir 3AZ2 after runing  0002 to 3AZ2_auto
#  mv 3AZ2/ 3AZ2_auto
#  mkdir 3AZ2/
## make sym-links 
# cd 3AZ2/
#/mnt/nfs/work/users/fischer/VDR/waterchannel_3AZ2/3AZ2_auto/*.pdb .
# mkdir working/
# cd working
# cp /mnt/nfs/work/users/fischer/VDR/waterchannel_3AZ2/3AZ2_auto/working/rec.crg.pdb rec.crg.ori.pdb
# # open structure in chimera and manully change protiniation of residue 305 from epsion to delta.
# chimera rec.crg.ori.pdb
# we removed the eps hydrogen from Histidine 305
# we then used the add hydrogen tool (tools/structure editing/AddH and then choise the option "Individually chosen"
# and selected to protonate the delta nitrogen for residue 305.
# remove non-polar hydrogens with the following command:
#   del HC
# # change the name of residue 305 with the following sed statement.
# sed -e "s/HIE A 305/HID A 305/g" rec.crg.mod.pdb > rec.crg.pdb

# loop over all pdb(s)
#foreach pdbname ( $list )

#echo "${pdbname}"

#set workdir = ${mountdir}/${pdbname}/
set workdir = ${mountdir}/

# checks that 001 ran successfully and produced the directory structure as expected
# if not stops with current pdb code and continues with next one in list
  if ! ( -s $workdir ) then
     echo "$workdir does not exit"
     continue
  endif

cd $workdir

mkdir rec_no_cof 
cd rec_no_cof 

# receptor and MG ions
# grep -m1 MG G13D-*/*.?.pdb
#cat ../rec.pdb ../pep.2.pdb > rec.pdb  
#cat ../rec.pdb > rec.pdb  
#cat ../rec_mod_no_cof.pdb > rec.pdb  
cat ../chimera/rec_complete_noH.pdb > rec.pdb  

#grep -m 1 "^.................LIG" $workdir/*.?.pdb | awk -F: '{print $1}'
#set ligfile = `grep -m 1 "^.................LIG" $workdir/*.?.pdb | awk -F: '{print $1}'`
#cat $ligfile | grep "HETATM" | sed -e 's/HETATM/ATOM  /g'> xtal-lig.pdb
cat ../clu.2.16.26.pdb_1.pdb > xtal-lig.pdb

#cat xtal-lig_ori.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >  xtal-lig.pdb

rm -f  qsub.csh
# the following lines create a qsub script which submits blastermaster to the queue
cat <<EOF > qsub.csh
#!/bin/csh 
#SBATCH -t 4:00:00
#SBATCH --output=stderr

cd $workdir/rec_no_cof
# this is the modifed blastermaster script in which the user can spesify a manuly protonated file
# and it also can be used for tarting (making residues more polar). 
$DOCKBASE/proteins/blastermaster/blastermaster.py --addhOptions=" -HIS -FLIPs "  -v 
EOF

#qsub qsub.csh 
sbatch qsub.csh 

#end # pdbname
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
