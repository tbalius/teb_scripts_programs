set mountdir = `pwd`

#set workdir = $mountdir/chimera_rmsd_full_alignment/
set workdir = $mountdir/workingdir/chimera_rmsd_5/ # Sets the workdir as /home/kleinam/klein_research_summer2019/chimera_rmsd_5

rm -rf $workdir # Removes current workdir directory and all files
mkdir -p $workdir # Create a directory that takes in the value of the workdir variable at that time
cd $workdir # Change the directory to the variable currently set to workdir

set chimerapath = "/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera" #"/mnt/nfs/soft/chimera/current/bin/chimera"

#ls -l ${mountdir}/workingdir/align_loop?/rec?.pdb
#ls -l ${mountdir}/workingdir/????/????_?.pdb
#ls -l ${mountdir}/workingdir/????/????.pdb

#set list = ` ls ${mountdir}/1*/rec.pdb `

 ls ${mountdir}/ori_and_states_files_with_residue_count.txt
 
set list = ` cat ${mountdir}/ori_and_states_files_with_residue_count.txt`
# line above: list rec.pdb files found in align_loop? in workingdir, those with ????_?.pdb, and those that do not have "_A" in their filename and then printing/extracting the ninth column

#echo $list | tr ' ' '\n'
#exit
#set list = ` ls ${mountdir}/181L/rec.pdb ${mountdir}/3GU*/rec.pdb ${mountdir}/4I7J/rec.pdb`
#set list = ` ls ${mountdir}/*/rec.pdb | head `

#set template = ` ls $mountdir/*/*A.pdb $mountdir/*/*B.pdb $mountdir/*/*C.pdb | sort | head -1`
## step1 aline pdbs
#set template = $list[1] # sets template variable to be equal to the lists' first element (rec?.pdb)
set template = "/home/kleinam/klein_kras_analysis/be_blasti_output/6GOD_model_0_A/6GOD_model_0_A_A.pdb" # sets template variable to be equal to the lists' first element (rec?.pdb)
#set template = $list[182] # sets template variable to be equal to the lists' first element (rec?.pdb)

foreach pdb ($list) # loop to go through each element in the list

  #set prefix = `echo $pdb | awk -F\/ '{print $NF}' | cut -c1-4`
  ## this gets the letter: eg. ethyl_refine_loop_009/ethyl_refine_loop_009_B.pdb -> B
  #set letter = `echo $pdb | awk -F\/ '{print $NF}' | awk -F\. '{print $1}' | awk -F\_ '{print $NF}'`
  #set name1  = "${prefix}_$letter"
  #set name1  = `echo $pdb | awk -F\/ '{print $9}'`
  set name1  = $pdb:t:r # set name1 variable to the pdb variable at each time the for loop runs; what does :t:r mean?
  echo "$name1...$pdb" # prints the $name1 variable at that time and the $pdb varible in order to make sure they match

  #exit

  echo $template $pdb # prints the $template variable value at that time and the $pdb variable as well
  echo $name1 # prints the $name1 variable during that iteration of the loop

  if (-e $name1.pdb) continue # if statement that says to continue to next pdb file if file does not exist

  if ($pdb == $template) then # if statement that says if both the pdb and template variables are equal to one another
      echo "template" # print template
      cp $template $name1.pdb # copy what is store in templateto a file with the name according to name1 with a .pdb extension
  endif # end when out of entries


# this is excluding the loop
# match #1:1-35,37-53,55-96,98-107,115-160@N,CA,C,O #0:1-35,37-53,55-96,98-107,115-160@N,CA,C,O
# this includes the loop for alignment
# match #1:1-35,37-53,55-96,98-160@N,CA,C,O #0:1-35,37-53,55-96,98-160@N,CA,C,O
# match #1:1-107,115-160@N,CA,C,O #0:1-107,115-160@N,CA,C,O
# match #1:#1-35,36-53,54-96,97-107,108-150,154-164,182-189 #0:1-35,36-53,54-96,97-107,108-150,154-164,182-189

cat <<EOF > chimera_script.align.$name1.com 
# open files
open $template $pdb
# do alignment
mmaker #0 #1
write format pdb 1 $name1.aligned.pdb
EOF
     $chimerapath --nogui chimera_script.align.$name1.com > chimera_script.align.$name1.output

end ## alignment
 
exit # script will end here to do only chimera alignments (separate script used for RMSD)
 
 set list = ` ls *.pdb ` # sets list as a list of everything that contains any characters/any number of characters with the .pdb extension
 #set list = ` ls *.pdb `

rm `ls chimera_script.*.output | grep -v "align"` # remove all lines that do not contain 'align'
rm `ls chimera_script.*.com | grep -v "align"` # remove all lines that do not contain 'align' 
rm rmsd.*.txt # remove rmsd.*.txt files

## caclulate rmsds
foreach sel_id ( \ # for loop to go though each sel_id; where should sel_id be and what does it need to be
        "loop" \
        #"Val111" \
 	#"Glu108" \
)
 
echo "sel_id = $sel_id"

if ($sel_id == "loop") then
   set seltion = "#0:185-194@N,CA,C,O #1:185-194@N,CA,C,O"
#else if ($sel_id == "Val111") then
#   set seltion = "#0:111@N,CA,C,O #1:111@N,CA,C,O"
#   #else if ($sel_id == "Glu108") then
#   #   set seltion = "#0:108@N,CA,C,O #1:108@N,CA,C,O"
else
    echo "sel_id = $sel_id not defined" # print the sel_id at that time and that that particular sel_id is not defined
    exit # exit
endif

ls *.aligned.pdb > aligned_list.txt

#/nfs/software/chimera/current/bin/chimera --nogui --script "../chimera_rmsd.py aligned_list.txt '$seltion' " | tee -a $sel_id.txt
#/home/baliuste/zzz.programs/Chimera --nogui --script 
$chimerapath --nogui --script "home/baliuste/zzz.scripts/chimera_rmsd.py aligned_list.txt '$seltion' " > ! $sel_id.txt

awk ' /file/{printf"%s %s ", $2, $3} /RMSD/{printf"%s\n",$7}' ${sel_id}.txt  | sed 's/.pdb//g' >! ${sel_id}_process.txt

end #selection num # end when all of the files have been sifted through
#
