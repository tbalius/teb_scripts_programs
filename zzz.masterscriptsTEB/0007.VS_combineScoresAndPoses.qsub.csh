#!/bin/csh 

#This script combines VS results into a scores file (extract_all) and a poses file (getposes) to view in chimera

 set d37 = "$DOCK_BASE/src/dock37tools"

 #set prefixName = "frags-now-marvin"
 #set prefixName = "frags-now-marvin_3O1D_tart"
 #set prefixName = "leads-now-marvin"
 #set prefixName = "leads-now-marvin_3O1D_tart"
 #set prefixName = "natural-products"
 #set prefixName = "natural-products_3O1D_tart"

 set mountdir = `pwd`
 echo "mountdir = $mountdir"
 
 foreach prefixName (\
   "frags-now-marvin_3O1D_tart" \
   "leads-now-marvin_3O1D_tart" \
   "natural-products_3O1D_tart" \
 )


 set workdir = "$mountdir/vs_$prefixName" 

 cd $workdir

 rm extract_all* top.*.mol2

cat << EOF > qsub.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -q all.q
#\$ -o stdout
#\$ -e stderr

 cd $workdir
 # ignore bad poses with scores greater than -20.0
 echo $d37/extract_all.py -s -20.0
 $d37/extract_all.py -s -20.0
 $d37/getposes.py -z -l 1000 -x 1 -f extract_all.sort.uniq.txt -o top.1000.mol2  
EOF

 qsub qsub.csh 

 end #prefixName 
