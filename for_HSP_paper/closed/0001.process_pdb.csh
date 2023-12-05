
  set username = `whoami`
  set pwd = `pwd`
  #echo ${pwd}
  #exit
  set filedir = $pwd/0001.files

  set scriptdir = `pwd` 
  #set name = "CYS"
  #set num  = " 37"
  #set num  = "165"
  #set num  = " 59"
  set workdir = 0001.chimera/

  if -e $workdir then
      echo "$workdir exists "
      exit
  endif
  
  mkdir $workdir
  cd $workdir

# /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/mon1_no_ATP.pdb  mon1_no_ATP_complete"
# /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/mon2_no_ATP.pdb  mon2_no_ATP_complete"
  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/mon1_noATP.pdb  mon1_no_ATP_complete" > log
  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/mon2_noATP.pdb  mon2_no_ATP_complete" >> log
  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/RAF.pdb  RAF_complete" >> log
  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_dockprep.py $filedir/CDC37.pdb  CDC37_complete" >> log

  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_addh.py $filedir/ATP_mon1.pdb ATP_mon1 keepH" >> log
  /home/${username}/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/${username}/zzz.scripts/chimera_addh.py $filedir/ATP_mon2.pdb ATP_mon2 keepH" >> log
 

