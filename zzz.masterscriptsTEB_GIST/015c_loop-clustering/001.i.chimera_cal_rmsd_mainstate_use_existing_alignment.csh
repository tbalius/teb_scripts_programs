

set mountdir = `pwd`

set filedir = $mountdir/../015b_RMSD/workingdir
set workdir = $mountdir/mainstate/rmsd_prealign

#rm -rf $workdir
if (-e $workdir) then
   echo "$workdir exists"
   exit
endif

mkdir -p $workdir
cd $workdir

set chimerapath = "/mnt/nfs/soft/chimera/current/bin/chimera" 

#ls -l ${mountdir}/workingdir/align_loop?/rec?.pdb
#ls -l ${mountdir}/workingdir/????/????_?.pdb
#ls -l ${mountdir}/workingdir/????/????.pdb

#set list = ` ls -l ${mountdir}/workingdir_mod/align_loop?/rec?.pdb ${mountdir}/workingdir_mod/????/????.pdb |  awk '{print $9}'`
#set list = ` ls -l ${filedir}/align_????/????.pdb |  awk '{print $9}'`
#echo "${filedir}/align_????/aligned.rec.pdb"
set list = ` ls ${filedir}/align_????/aligned.rec.pdb `
#echo $list | tr ' ' '\n' 
#exit
#set list = ` ls ${mountdir}/181L/rec.pdb ${mountdir}/3GU*/rec.pdb ${mountdir}/4I7J/rec.pdb`
#set list = ` ls ${mountdir}/*/rec.pdb | head `

#set template = ` ls $mountdir/*/*A.pdb $mountdir/*/*B.pdb $mountdir/*/*C.pdb | sort | head -1`
## step1 aline pdbs
set template = $list[1]

foreach file ($list)
#
#  echo $file | awk -F\/ '{print NF - 1}'
  set field = `echo $file | awk -F\/ '{print NF - 1}'` # number slash sparated fields in path, the name of the inner most director is our opjective
#  #echo $file | awk -F\/ '{print $14}' 
#  echo $file | awk -F\/ '{print $'$field'}'
  set name = `echo $file | awk -F\/ '{print $'$field'}' | sed -e 's/align_//g'`

  cp $file $name.aligned.pdb 

end 
#exit

set list = ` ls *.pdb `
#set list = ` ls *.pdb `

#rm `ls chimera_script.*.output | grep -v "align"`
#rm `ls chimera_script.*.com | grep -v "align"`
#rm rmsd.*.txt


## caclulate rmsds

foreach sel_id ( \
  "loop" \
  #"Val111" \
  #"Glu108" \
)

echo "sel_id = $sel_id"

if ($sel_id == "loop") then
   set seltion = "#0:185-194@N,CA,C,O #1:185-194@N,CA,C,O"
#else if ($sel_id == "Val111") then
#   set seltion = "#0:111@N,CA,C,O #1:111@N,CA,C,O"
#else if ($sel_id == "Glu108") then
#   set seltion = "#0:108@N,CA,C,O #1:108@N,CA,C,O"
else
   echo "sel_id = $sel_id not defined"
   exit
endif

ls *.aligned.pdb > aligned_list.txt 

#/nfs/software/chimera/current/bin/chimera --nogui --script "../chimera_rmsd.py aligned_list.txt '$seltion' " | tee -a $sel_id.txt
/nfs/soft/chimera/current/bin/chimera --nogui --script "${mountdir}/for001.chimera_rmsd.py aligned_list.txt '$seltion' " > ! $sel_id.txt

awk ' /file/{printf"%s %s ", $2, $3} /RMSD/{printf"%s\n",$7}' ${sel_id}.txt  | sed 's/.pdb//g' >! ${sel_id}_process.txt

end #selection num
