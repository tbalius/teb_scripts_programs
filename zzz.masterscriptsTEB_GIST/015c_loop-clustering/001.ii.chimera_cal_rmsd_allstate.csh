

set mountdir = `pwd`

set filedir = $mountdir/../015b_RMSD/workingdir/
set workdir = $mountdir/allstates/rmsd

if (-e $workdir) then
   echo "$workdir exists"
   continue
endif

mkdir -p $workdir
cd $workdir

set chimerapath = "/mnt/nfs/soft/chimera/current/bin/chimera" 

#ls -l ${mountdir}/workingdir/align_loop?/rec?.pdb
#ls -l ${mountdir}/workingdir/????/????_?.pdb
#ls -l ${mountdir}/workingdir/????/????.pdb

#set list = ` ls ${mountdir}/1*/rec.pdb `
#set list = ` ls -l ${mountdir}/workingdir/align_loop?/rec?.pdb ${mountdir}/workingdir/????/????_?.pdb ${mountdir}/workingdir/????/????.pdb | grep -v "_A" |  awk '{print $9}'`
#set list = ` ls -l ${filedir}/????/????_?.pdb ${filedir}/????/????.pdb | grep -v "_A" |  awk '{print $9}'`

echo ${filedir}/????/????_?.pdb ${filedir}/????/????.pdb
ls ${filedir}/????/????_?.pdb ${filedir}/????/????.pdb 

set list = `ls ${filedir}/????/????_?.pdb ${filedir}/????/????.pdb | grep -v "_A"`
#echo $list | tr ' ' '\n' 
#exit
#set list = ` ls ${mountdir}/181L/rec.pdb ${mountdir}/3GU*/rec.pdb ${mountdir}/4I7J/rec.pdb`
#set list = ` ls ${mountdir}/*/rec.pdb | head `

#set template = ` ls $mountdir/*/*A.pdb $mountdir/*/*B.pdb $mountdir/*/*C.pdb | sort | head -1`
## step1 aline pdbs
set template = $list[1]

foreach pdb ($list)

  #set prefix = `echo $pdb | awk -F\/ '{print $NF}' | cut -c1-4`
  ## this gets the letter: eg. ethyl_refine_loop_009/ethyl_refine_loop_009_B.pdb -> B
  #set letter = `echo $pdb | awk -F\/ '{print $NF}' | awk -F\. '{print $1}' | awk -F\_ '{print $NF}'`
  #set name1  = "${prefix}_$letter"
  #set name1  = `echo $pdb | awk -F\/ '{print $9}'`
  set name1  = $pdb:t:r
  echo "$name1...$pdb"

  #exit

  echo $template $pdb
  echo $name1 

  if (-e $name1.pdb) continue

  if ($pdb == $template) then
      echo "template"
      cp $template $name1.pdb
  endif   

  
 cp $pdb  $name1.pdb.old
 grep "^.....................A\|X\|B" $name1.pdb.old > $name1.pdb # to only have one chain. 
 #cp $name1.pdb.old $name1.pdb
cat <<EOF > chimera_script.align.$name1.com
 # open files
 open $template $name1.pdb
 # calculate rmsd
 mmaker #0 #1
 # this is excluding the loop
 #match #1:1-35,37-53,55-96,98-107,115-160@N,CA,C,O #0:1-35,37-53,55-96,98-107,115-160@N,CA,C,O
 # this includes the loop for alignment
 #match #1:1-35,37-53,55-96,98-160@N,CA,C,O #0:1-35,37-53,55-96,98-160@N,CA,C,O
 #match #1:1-107,115-160@N,CA,C,O #0:1-107,115-160@N,CA,C,O
 write format pdb 1 $name1.aligned.pdb
EOF

 $chimerapath --nogui chimera_script.align.$name1.com > chimera_script.align.$name1.output

end ## alignment

#exit

set list = ` ls *.pdb `
#set list = ` ls *.pdb `

rm `ls chimera_script.*.output | grep -v "align"`
rm `ls chimera_script.*.com | grep -v "align"`
rm rmsd.*.txt


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
/nfs/soft/chimera/current/bin/chimera --nogui --script "~/zzz.scripts/chimera_rmsd.py aligned_list.txt '$seltion' " > ! $sel_id.txt

awk ' /file/{printf"%s %s ", $2, $3} /RMSD/{printf"%s\n",$7}' ${sel_id}.txt  | sed 's/.pdb//g' >! ${sel_id}_process.txt

end #selection num
