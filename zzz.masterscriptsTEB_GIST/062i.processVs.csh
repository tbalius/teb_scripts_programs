
#!/bin/csh 

#This script combines VS results into a scores file (extract_all) and a poses file (getposes) to view in chimera

 setenv DOCKBASE "/nfs/home/tbalius/zzz.github/DOCK"
 source /nfs/soft/python/envs/complete/latest/env.csh

 set prefixName = "_flex__gist"
 #set prefixName = "_flex__nogist"
 #set prefixName = "_min"
 #set prefixName = "leads-now-marvin"
 #set prefixName = "natural-products"

 set mountdir = `pwd`
 echo "mountdir = $mountdir"

 set workdir = "$mountdir/vs$prefixName"

 cd $workdir

 if (-e dirlist_ori) then 
    echo "Ooh.  Maybe you want to use the original dirlist."
    echo "consider: cp dirlist_ori dirlist"
 endif

 # ignore bad poses with scores greater than -20.0 kcal/mol
 # when comparing two screens don't use cutoffs as they may result in omission of compounds from one screen and hence headaches.
 #$DOCKBASE/analysis/extract_all.py -s -20.0
 #$DOCKBASE/analysis/extract_all.py
 $DOCKBASE/analysis/extract_all.py --done

 # top poses for chimera viewdock
 # '-z' flag connects to ZINC for vendor information, [may cause issues] 
 # '-l 1000' flag only gets the first 1000 ligands in the file,
 # '-x 2' gets the top 2 poses,
 # '-f ligands.txt' file designates the ligand file to use (generated by extract_all)
 # '-o ligands.1000.mol2' designates the output filename
 # 
 $DOCKBASE/analysis/getposes.py -l 1000 -x 1 -f extract_all.sort.uniq.txt -o top.1000.mol2

# this will delete cache files that are sometimes created, not necessary and very big
ls -l */test.mol2.gz.db
echo "If these files were produced remove them via command line:"
echo "rm -rf vs$prefixName/*/test.mol2.gz.db"
