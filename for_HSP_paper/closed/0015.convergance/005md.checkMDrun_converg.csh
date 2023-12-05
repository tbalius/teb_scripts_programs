# This script makes 3 lists: 
#       1) for the initial equilibration run (until RT is reached)
#       2) for the final equilibration run
#       3) for the production run
# It then runs a python script that generates plots for analysis of the quality of the MD run in a separate directory.


set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap"
set scriptdir = "$mountdir"
#set mut = E37C 
#set lig = DL2040 
#set lig = DL2078 
#set lig = DL1314_Protomer1 
#set lig = 228354851_poses_00010
#set lig = 228354851
#set lig = mol017 
#set lig = mol016 

#cd $pwd

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

foreach seed ( \
  "0"  \
  "5"  \
  "50" \
  "500" \
)

 #set pdb = "5VBE"
  set pdb = ""
 #set pdb = "_min"
 #set pdb = "5VBE_min"
 #set lig = ${lig}_${seed}


#set temp = `ls ${mountdir}/${pdb}/004.MDrun_${seed}/*/01mi.rst7 | head -1`
set temp = `ls ${mountdir_ori}/${pdb}/0004.MDrun_corrected_${seed}/*/01mi.rst7 | head -1`
echo ${temp}
set jobId = $temp:h:t
echo $jobId
set jid = $jobId


  #set jid = $1         #job id as specified by queue e.g. 5609039; this is also the directory name
  #set workdir   = $mountdir/${pdb}/004.MDrun_${seed}/${jid}_plots
  set workdir   = $mountdir/${pdb}/0004.MDrun_corrected_${seed}/${jid}_plots
  set filedir = $workdir:h:t
  #set workdir   = $mountdir/004.MDrun_lig/${jid}_plots

#  if ($jid == "") then
#     echo "Give JobID as argument. \n e.g.    csh 005md.checkMDrun.csh 5609039 \n"
#     exit
#  endif

  if (-e ${workdir}) then
     echo "$workdir exists"
     #exit
     continue
  endif

  mkdir -p ${workdir}  
  cd $workdir
  #if the job is running, log in the node where you run the job and use the two lines below
  set username = `whoami`
  #ln -s /scratch/${username}/${jid} 
  #if the job finishes, use the line below and no need to log in the node where you run the job\
  ln -s ${mountdir_ori}/${filedir}/${jid} .
 
  ls ${jid}/01mi.out ${jid}/02mi.out ${jid}/03mi.out ${jid}/04mi.out ${jid}/01md.out ${jid}/02md.out ${jid}/03md.out ${jid}/04md.out ${jid}/05md.out ${jid}/06md.out > equil1.txt
  ls ${jid}/07.0md.out ${jid}/07.1md.out ${jid}/07.2md.out ${jid}/08md.out > equil2.txt
  ls ${jid}/09md.out ${jid}/10md.out ${jid}/11md.out ${jid}/12md.out ${jid}/13md.out ${jid}/14md.out ${jid}/15md.out ${jid}/16md.out ${jid}/17md.out ${jid}/18md.out > production.txt

# runs python plotter <in> <out>
  python ${scriptdir}/for005md_conv.py equil1.txt equil1.png > equil1.log
  python ${scriptdir}/for005md_conv.py equil2.txt equil2.png > equil2.log
  python ${scriptdir}/for005md_conv.py production.txt production.png > production.log

#echo "\n   Now open png's: \n   gthumb MDrundir/MDrun/${jid}_plots/*png"
end # seed
