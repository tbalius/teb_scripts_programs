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


foreach TS_low_die ( "0.0" "0.3" "0.5" "0.7" "1.0" )
foreach TS_desolv  ( "0.0" "0.3" "0.5" "0.7" "1.0" )

#echo "${pdbname}"

#set workdir = ${mountdir}/${pdbname}/

# checks that 001 ran successfully and produced the directory structure as expected
# if not stops with current pdb code and continues with next one in list
# if ! ( -s $workdir ) then
#    echo "$workdir does not exit"
#    continue
# endif

set workdir = ${mountdir}/blastermaster_cof_${TS_low_die}_${TS_desolv}
mkdir $workdir 
cd $workdir

#mkdir blastermaster_cof_${TS_low_die}_${TS_desolv} 
#cd blastermaster_cof_${TS_low_die}_${TS_desolv} 

# receptor and MG ions
# grep -m1 MG G13D-*/*.?.pdb

ls ../rec_no_cof/working/rec.crg.pdb
#cat ../rec_no_cof/working/rec.crg.pdb ../chimera/cof/cof.pdb | \
cat ../rec_no_cof/working/rec.crg.pdb ../chimera/cof/cof.pdb > rec.crg.pdb  

ls ../rec_no_cof/rec.pdb ../chimera/cof/cof.pdb 

#exit

#cat ../rec_no_cof/rec.pdb ../chimera/cof/cof.pdb | \
cat ../rec_no_cof/rec.pdb ../chimera/cof/cof.pdb | grep -v ' H$' > rec.pdb  

cat ../rec_no_cof/xtal-lig.pdb > xtal-lig.pdb  

 set TEB_SCRIPTS_PATH = ~baliuste/zzz.github/teb_scripts_programs

 cp $DOCKBASE/proteins/defaults/prot.table.ambcrg.ambH  $DOCKBASE/proteins/defaults/amb.crg.oxt . 
 chmod u+w prot.table.ambcrg.ambH amb.crg.oxt  
 
 python ${TEB_SCRIPTS_PATH}/zzz.scripts/mol2toDOCK37type.py ../chimera/cof/cof.ante.charge.mol2 temp

 cat temp.prot.table.ambcrg.ambH >> prot.table.ambcrg.ambH
 cat temp.amb.crg.oxt >>  amb.crg.oxt

#cat xtal-lig_ori.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >  xtal-lig.pdb

rm -f  qsub.csh
# the following lines create a qsub script which submits blastermaster to the queue
cat <<EOF > qsub.csh
#!/bin/csh 
#SBATCH -t 4:00:00
#SBATCH --output=stderr

cd $workdir
mkdir working
cp rec.crg.pdb working/rec.crg.pdb
# this is the modifed blastermaster script in which the user can spesify a manuly protonated file
# and it also can be used for tarting (making residues more polar). 
EOF
#$DOCKBASE/proteins/blastermaster/blastermaster.py --addNOhydrogensflag --chargeFile=`pwd`/amb.crg.oxt --vdwprottable=`pwd`/prot.table.ambcrg.ambH -v
# the following lines create a qsub script which submits blastermaster to the queue
if (${TS_desolv} == "0.0" && ${TS_low_die} == "0.0") then # this is standard. 
cat <<EOF >> qsub.csh
   $DOCKBASE/proteins/blastermaster/blastermaster.py  --addNOhydrogensflag --chargeFile=`pwd`/amb.crg.oxt --vdwprottable=`pwd`/prot.table.ambcrg.ambH -v
EOF

else if (${TS_desolv} == "0.0") then
cat <<EOF >> qsub.csh
   $DOCKBASE/proteins/blastermaster/blastermaster.py  --addNOhydrogensflag --chargeFile=`pwd`/amb.crg.oxt --vdwprottable=`pwd`/prot.table.ambcrg.ambH --useThinSphEleflag --ts_dist_ele ${TS_low_die} --ts_radius_ele ${TS_low_die} --ts_dist_to_lig 4.0 --mstsDensity 1.2 -v
EOF
else if (${TS_low_die} == "0.0") then
cat <<EOF >> qsub.csh
   $DOCKBASE/proteins/blastermaster/blastermaster.py --addNOhydrogensflag --chargeFile=`pwd`/amb.crg.oxt --vdwprottable=`pwd`/prot.table.ambcrg.ambH  --useThinSphLdsflag --ts_dist_lds ${TS_desolv} --ts_radius_lds ${TS_desolv}  --ts_dist_to_lig 4.0 --mstsDensity 1.2 -v
EOF
else
cat <<EOF >> qsub.csh
   $DOCKBASE/proteins/blastermaster/blastermaster.py  --addNOhydrogensflag --chargeFile=`pwd`/amb.crg.oxt --vdwprottable=`pwd`/prot.table.ambcrg.ambH --useThinSphEleflag --useThinSphLdsflag --ts_dist_ele ${TS_low_die} --ts_radius_ele ${TS_low_die} --ts_dist_lds ${TS_desolv} --ts_radius_lds ${TS_desolv}  --ts_dist_to_lig 4.0 --mstsDensity 1.2 -v
EOF
endif

#qsub qsub.csh 
sbatch qsub.csh 

end #TS_desolv
end #TS_low_die
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