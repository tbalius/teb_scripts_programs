#!/bin/csh

# This script runs the VS of a specified database 

 # sets dock 3.7 path
 set d37 = "$DOCK_BASE/src/dock37tools"

 # <CHANGE THIS> choosing the database to screen and path to db
 # prefixName is db2 directory name that contains all db2 files AND
 # the prefix for dir for docking chunks of the database.
 #set prefixName = "frags-now-marvin"
 #set prefixName = "leads-now-marvin"
 #set pathToDb2 = "/nfs/db/tbalius/$prefixName" 

 # for natural products (run in SF and copies over to UofT) the path is:
 set prefixName = "natural-products"
 set pathToDb2 = "/nfs/db/tbalius/set98"

 #set desiredDirectoryCount = "150"
 #set desiredDirectoryCount = "3000"
 set desiredDirectoryCount = "17000"	# especially for leads, for other ones <2000 suffices

 set mountdir = `pwd`
 echo "mountdir = $mountdir"

 #set pdbname =  "3AZ2"
 set workdir = "$mountdir/vs_$prefixName" 

# rm -r $workdir
 mkdir -p $workdir
 cd $workdir

 # dockfiles contains spheres, grids, and other needed files for docking
 # INDOCK assumes to find a dockfiles directory 2 directories up relative to vs_$prefixName/$prefixName-001 where the dock calcs are run 
 #ln -s $mountdir/$pdbname/dockfiles
 #ln -s $mountdir/$pdbname/INDOCK
 ln -s $mountdir/dockfiles
 ln -s $mountdir/INDOCK

 # make database for docking: sets up directories and assigns chunks to be docked in that directory
 echo $d37/setup_db2_lots.py $desiredDirectoryCount $prefixName  $pathToDb2/
 $d37/setup_db2_lots.py $desiredDirectoryCount $prefixName $pathToDb2/
 
 # submit dock3.7 (run on sgehead)
 echo $d37/submit.csh
 $d37/submit.csh
 
  
