#!/bin/csh

## right now the processing scripts requier that the FORTRAN STOP be in the stderr file
## if docking is not run on a queue then we need to create the stderr file and put "FORTRAN STOP" in the file.
## 

set filedir = `pwd`
#set mountdir = "/mnt/nfs/work/tbalius/Water_Project/run_DOCK3.7/workingdir"
set mountdir = `pwd`
set d37 =  $DOCK_BASE/src/dock37tools
#set dir_name = standard


cd $mountdir

#foreach indock_type ( "standard" )

foreach pdbname ( \
 "3O1D_tart3" \
 )
  

foreach lig_type ( \
 "ligands" \
# "decoys" \
# "known-non-binders" \
 )


   ls -ld ${mountdir}/${pdbname}/ligands-decoys/${lig_type}/chunk*/ | awk '{print $9}'

   foreach stderrfile (` ls -ld ${mountdir}/${pdbname}/ligands-decoys/${lig_type}/chunk*/ | awk '{print $9}' `)
     echo $stderrfile/stderr

     if !(-e $stderrfile/stderr) touch $stderrfile/stderr

     cat $stderrfile/stderr

     grep "FORTRAN STOP" $stderrfile/stderr 

     echo "FORTRAN STOP" >> $stderrfile/stderr
   end

end # lig_type

end # pdbname
#end # indock_type


