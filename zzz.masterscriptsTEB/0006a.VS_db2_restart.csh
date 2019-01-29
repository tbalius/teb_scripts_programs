#!/bin/csh

#This script restarts a prematurely terminated VS run (without rerunning finished stuff)

  set d37 = "$DOCK_BASE/src/dock37tools"

 #set prefixName = "frags-now-marvin"
 set prefixName = "leads-now-marvin"

 set mountdir = `pwd`
 echo "mountdir = $mountdir"

 set workdir = "$mountdir/vs_$prefixName" 

 cd $workdir

 # resubmit dock3.7; with -f, --force-it        force restart for all unfinished jobs
 echo $d37/restart.py -f
 $d37/restart.py -f
 
  
