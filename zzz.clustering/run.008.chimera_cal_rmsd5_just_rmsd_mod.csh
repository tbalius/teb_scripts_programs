
set mountdir = `pwd`

#set workdir = $mountdir/chimera_rmsd_full_alignment/
set workdir = $mountdir/workingdir/chimera_rmsd_5/ # Sets the workdir as /home/kleinam/klein_research_summer2019/chimera_rmsd_5
cd $workdir # Change the directory to the variable currently set to workdir

 
set chimerapath = "/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera" #"/mnt/nfs/soft/chimera/current/bin/chimera"
 set list = ` ls *.pdb ` # sets list as a list of everything that contains any characters/any number of characters with the .pdb extension
 #set list = ` ls *.pdb `

rm `ls chimera_script.*.output | grep -v "align"` # remove all lines that do not contain 'align'
rm `ls chimera_script.*.com | grep -v "align"` # remove all lines that do not contain 'align' 
rm rmsd.*.txt # remove rmsd.*.txt files

## caclulate rmsds
# for loop to go though each sel_id; where should sel_id be and what does it need to be
foreach sel_id ( \
        "full" \
	"switch1"
        #"loop" \
        #"Val111" \
 	#"Glu108" \
)
 
echo "sel_id = $sel_id"

if ($sel_id == "full") then
   set seltion = "#0:2-9,18-25,39-50,77-121,127-164@N,CA,C,O #1:2-25,39-50,72-121,127-164@N,CA,C,O"
else if ($sel_id == "switch1") then
   #set seltion = "#0:185-194@N,CA,C,O #1:185-194@N,CA,C,O"
   set seltion = "0:30-38@N,CA,C,O #1:30-38@N,CA,C,O"
#else if ($sel_id == "Val111") then
#   set seltion = "#0:111@N,CA,C,O #1:111@N,CA,C,O"
#   #else if ($sel_id == "Glu108") then
#   #   set seltion = "#0:108@N,CA,C,O #1:108@N,CA,C,O"
else
    echo "sel_id = $sel_id not defined" # print the sel_id at that time and that that particular sel_id is not defined
    exit # exit
endif

#ls *.aligned.pdb > aligned_list.txt

#/nfs/software/chimera/current/bin/chimera --nogui --script "../chimera_rmsd.py aligned_list.txt '$seltion' " | tee -a $sel_id.txt
#/home/baliuste/zzz.programs/Chimera --nogui --script 
$chimerapath --nogui --script "/home/baliuste/zzz.scripts/chimera_rmsd.py aligned_list_switchI.txt '$seltion' " > ! $sel_id.txt

awk ' /file/{printf"%s %s ", $2, $3} /RMSD/{printf"%s\n",$7}' ${sel_id}.txt  | sed 's/.pdb//g' >! ${sel_id}_process.txt

end #selection num # end when all of the files have been sifted through
#
