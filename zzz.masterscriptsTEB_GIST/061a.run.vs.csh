#!/bin/csh

# This script runs the VS of a specified database 

 # sets dock 3.7 path
 setenv DOCKBASE /nfs/home/tbalius/zzz.github/DOCK
 

 # <CHANGE THIS> choosing the database to screen and path to db
 # prefixName is db2 directory name that contains all db2 files AND
 # the prefix for dir for docking chunks of the database.
 #set prefixName = "frags-now-marvin"
 #set prefixName = "leads-now-marvin"
 #set pathToDb2 = "/nfs/db/tbalius/$prefixName" 

 # for natural products (run in SF and copies over to UofT) the path is:
 #set docktype =  "_nogist"
 set docktype =  "_gist"
 #set docktype =  "_min"
 set prefixName = "frag"
 set indexfile = ../020.get_database_index_files/2017.03.07.ZINC-downloader-3D-db2.gz.database_index

 set desiredDirectoryCount = "2428"	# especially for leads, for other ones <2000 suffices

 set mountdir = `pwd`
 echo "mountdir = $mountdir"
 set filedir = $mountdir/flex/2prep/  # CHANGE THIS

 #set pdbname =  "3AZ2"
 set workdir = "$mountdir/vs_flex_${docktype}" 

# rm -r $workdir
 mkdir -p $workdir
 cd $workdir

 # dockfiles contains spheres, grids, and other needed files for docking
 # INDOCK assumes to find a dockfiles directory 2 directories up relative to vs_$prefixName/$prefixName-001 where the dock calcs are run 
 ln -s $filedir/dockfiles .
 ln -s $filedir/gistfiles .
 ln -s $filedir/INDOCK${docktype} INDOCK

 # make database for docking: sets up directories and assigns chunks to be docked in that directory
 echo $DOCKBASE/docking/setup/setup_db2_zinc15_file_number.py . $prefixName  $indexfile $desiredDirectoryCount count
 $DOCKBASE/docking/setup/setup_db2_zinc15_file_number.py . $prefixName  $indexfile $desiredDirectoryCount count
 
 # submit dock3.7 (run on sgehead)
 echo $DOCKBASE/docking/submit/submit.csh
 $DOCKBASE/docking/submit/submit.csh
  
