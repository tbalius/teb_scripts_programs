#!/bin/csh 


set mountdir = `pwd`
#set mountdir = "/mnt/nfs/work//tbalius/Water_Project/run_DOCK3.7"
#set filedir  = "/mnt/nfs/work//tbalius/Water_Project"

#foreach conf (  "C"  )
foreach conf ( "A.B.C" )
#foreach conf ( "A.B.C.justloops" )
#foreach conf ( "A.B.C" "A.B.C.justloops" )

set workdir = $mountdir/workingdir/align_CcP_$conf/

  rm -rf  ${workdir}
  mkdir ${workdir}
  cd ${workdir}
  

cat $mountdir/workingdir/align/aligned.$conf.rec.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | awk '{if($12 != "H"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >!  rec.pdb
cat $mountdir/workingdir/align_4NVE/aligned.lig.pdb | awk '{if ($1 == "ATOM" || $1 == "HETATM"){print $0}}' | sed -e "s/HETATM/ATOM  /g"  >!  xtal-lig.pdb

# to use the new charge model
  sed -i 's/HEM/HM2/g'   rec.pdb
  #sed -i 's/ FE /  FE/g' rec.pdb
  mv rec.pdb rec.pdb.old
  grep -v "HOH" rec.pdb.old > rec.pdb 
  #grep -v "HOH" rec.pdb.old | grep -v "^................F" > rec.pdb 
  # remove the waters and state F
  #
#grep "ATOM" /mnt/nfs/work/tbalius/Water_Project/structures_from_marcus/APO_rt_consensusloop_new2.pdb | grep -v "^................ " | cut -c18-26 | uniq | awk '{printf "%s,", $3} END{printf "\n"}'
grep "ATOM" rec.pdb | grep -v "^................ " | cut -c17-26 | uniq 
#set reslist = `grep "ATOM" rec.pdb | grep -v "^................ " | cut -c18-26 | uniq | awk '{printf "%s,", $3} END{printf "\n"}'`
if ( $conf == "A.B.C") then
   set reslist = 186+187+188+189+190+191+192+193+194,199,228
else if ( $conf == "A.B.C.justloops") then
   set reslist = 186+187+188+189+190+191+192+193+194
else 
   echo "reslist is not defined"
   exit
endif

echo $reslist
#echo 186+187+188+189+190+191+192+193+194,199,228
#echo 186+187+188+189+190+191+194,192+193,199,228
  # we could sparate 192+193 if state F is used

#cp /usr/local2/lib/dms/radii .

## startdockblaster6 calls a modified Makefile
## that uses Ryan G Coleman's reduce procegers:
## blasterAddHydrogens_standalone.py
#startdockblaster6 >& log.txt

#$DOCK_BASE/src/blastermaster_1.0/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="${mountdir}/zzz.for_reduce/reduce_wwPDB_het_dict_mod.txt" --chargeFile="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/amb_mod.crg.oxt" --vdwprottable="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/prot_mod.table.ambcrg.ambH" -v
###$DOCKBASE/proteins/blastermaster/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="${mountdir}/zzz.for_reduce/reduce_wwPDB_het_dict_mod.txt" --chargeFile="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/amb_mod.crg.oxt" --vdwprottable="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/prot_mod.table.ambcrg.ambH" -v -f  --flexibleResidues=${reslist} -s
cat <<EOF >! qsub.csh
#!/bin/csh 
#\$ -cwd
#\$ -j yes
#\$ -o stderr
#\$ -q all.q
cd $workdir
$DOCKBASE/proteins/blastermaster_mod/blastermaster.py --addhOptions=" -HIS -FLIPs " --addhDict="${mountdir}/zzz.for_reduce/reduce_wwPDB_het_dict_mod.txt" --chargeFile="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/amb_mod.crg.oxt" --vdwprottable="/nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/prot_mod.table.ambcrg.ambH" -v -f --flexiblePenaltyM=2.0 --flexibleResidues=${reslist} -s
EOF

#qsub qsub.csh 
csh qsub.csh 

end # conf


