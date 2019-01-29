# This script makes 3 lists: 
#	 1) for the initial equilibration run (until RT is reached)
# 	 2) for the final equilibration run
#	 3) for the production run
# It then runs a python script that generates plots for analysis of the quality of the MD run in a separate directory.
#
# by TEB/ MF March 2017


  set jid = $1		#job id as specified by queue e.g. 5609039; this is also the directory name
  set mountdir  = `pwd`
  set workdir   = $mountdir/MDrundir/MDrun/${jid}_plots

  if ($jid == "") then
     echo "Give JobID as argument. \n e.g.    csh 005md.checkMDrun.csh 5609039 \n"
     exit
  endif

  if (-e ${workdir}) then
     echo "$workdir exists"
     exit
  endif

  mkdir -p ${workdir}  
  cd $workdir

  ln -s ../${jid} 
 
  ls ${jid}/01mi.out ${jid}/02mi.out ${jid}/01md.out ${jid}/02md.out ${jid}/03md.out ${jid}/04md.out ${jid}/05md.out ${jid}/06md.out > equil1.txt
  ls ${jid}/07.1md.out ${jid}/07.2md.out ${jid}/08md.out > equil2.txt
  ls ${jid}/09md.out ${jid}/10md.out ${jid}/11md.out ${jid}/12md.out ${jid}/13md.out ${jid}/14md.out ${jid}/15md.out ${jid}/16md.out ${jid}/17md.out ${jid}/18md.out > production.txt

# runs python plotter <in> <out>
  python ${mountdir}/for005md.py equil1.txt equil1.png
  python ${mountdir}/for005md.py equil2.txt equil2.png
  python ${mountdir}/for005md.py production.txt production.png

echo "\n   Now open png's: \n   gthumb MDrundir/MDrun/${jid}_plots/*png"
