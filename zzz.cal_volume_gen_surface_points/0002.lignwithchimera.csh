#!/bin/csh 
## this script was written by Trent Balius in the Rizzo Group, 2011
## modified in the Shoichet Group, 2013-2014


#set mountdir = `pwd`
set mountdir = `pwd`

# reference
set file1 = "$mountdir/1CMQ/1CMQ_ori_rec.pdb"

#foreach file (`ls $mountdir/4W5?/4W5?_?_rec.pdb`)
foreach pdb (`cat $mountdir/pdblist.txt`)

   ls $mountdir/${pdb}/${pdb}_?_rec.pdb
   if (-e $mountdir/${pdb}/${pdb}_A_rec.pdb) then
       set filelist = `ls $mountdir/${pdb}/${pdb}_?_rec.pdb`
   else 
       set filelist = $mountdir/${pdb}/${pdb}_ori_rec.pdb 
       if (-z $mountdir/${pdb}/${pdb}_ori_rec.pdb) then 
         echo "ori does not exist."
         continue
       endif
   endif
   foreach file ($filelist)
   set filename = $file:r
   set file2 = "$file"
   set chimerapath = "/nfs/soft/chimera/current/bin/chimera"
   echo ${filename} 
   if (-e ${filename}_aligned.pdb) then
      echo "${filename}_aligned.pdb exists"
      continue
      #exit
   endif
cat << EOF > chimera.com
# template #0
open $file1 
# rec
open $file2 

# move original to gist. it is harder to move the gist grids. 
mmaker #0 #1 
#matrixcopy #1 #2
#matrixcopy #1 #3

write format pdb  1 ${filename}_aligned.pdb
EOF

   #/sbhome0/sudipto/RCR/projects_BNL/chimera/bin/chimera --nogui chimera.com > & chimera.com.out
   ${chimerapath} --nogui chimera.com > & chimera.com.out

end # file
end # pdb
#end # pdbcode


set file2 = "$mountdir/2AS1/2AS1_A_rec.pdb"
set file3 = "$mountdir/2AS1/xtal-lig.pdb"
set file3out = "$mountdir/2AS1/xtal-lig_aligned.pdb"

cat << EOF > chimera.com
# template #0
 open $file1 
# rec
 open $file2 
# lig
 open $file3 
# move original to gist. it is harder to move the gist grids. 
 mmaker #0 #1 
 matrixcopy #1 #2
 write format pdb  2 $file3out
EOF

${chimerapath} --nogui chimera.com > & chimera.com.out

