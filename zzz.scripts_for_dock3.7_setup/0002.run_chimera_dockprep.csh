
set mountdir = `pwd`
set scriptdir = /home/baliuste/zzz.github/teb_scripts_programs/zzz.scripts

#foreach pdb ( $pdblist ) 
# loop over pdbnames e.g. 1DB1 or list
#foreach pdbname ( $list )
#set pdb = $pdbname:r

#set protein = ${mountdir}/$pdb/rec.pdb
set protein = ${mountdir}/rec_mod_no_cof.pdb
#set ions = ${mountdir}/$pdb/pep.2.pdb
#set cof1 =  ${mountdir}/$pdb/pep.1.pdb
#set lig =  ${mountdir}/$pdb/lig.1.pdb
# head -2 snapshot_6496_mod_lys165/lig*.pdb
#set cof1 =  ${mountdir}/$pdb/lig.3.pdb
set cof1 =  ${mountdir}/cof.pdb
#set cof2 = ${mountdir}/$pdb/lig.2.pdb 

#set workdir = ${mountdir}/$pdb/chimera
set workdir = ${mountdir}/chimera
if -e $workdir then
   echo "$workdir exists. skiping ... "
   continue
endif
mkdir -p $workdir
cd $workdir

set chimerapath = /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/

#~/zzz.programs/Chimera/UCSF-Chimera64-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.github/teb_scripts_programs/zzz.scripts/chimera_dockprep.py 1L2S.pdb 1L2S_out"

#cat $protein $ions > rec.pdb
cat $protein > rec.pdb
cat $cof1 > cof.pdb
#python $mountdir/replace_atom_type.py cof.pdb cof_GTP.pdb 
python $mountdir/replace_atom_ele.py cof.pdb N3B N O cof_GTP 
#cat $cof2 > cof.pdb
#cat $cof1 $cof2 > cof.pdb
#cat $lig > lig.pdb

touch chimera.log

$chimerapath/chimera --nogui --script "${scriptdir}/chimera_dockprep.py rec.pdb rec_complete  "         >> chimera.log
$chimerapath/chimera --nogui --script "${scriptdir}/chimera_addh.py cof.pdb cof_addh ' ' "                 >> chimera.log
$chimerapath/chimera --nogui --script "${scriptdir}/chimera_dockprep.py cof_GTP.pdb cof_GTP_complete  " >> chimera.log
$chimerapath/chimera --nogui --script "${scriptdir}/chimera_addh.py     cof_GTP.pdb cof_GTP_addh ' '"      >> chimera.log

#end # pdb
