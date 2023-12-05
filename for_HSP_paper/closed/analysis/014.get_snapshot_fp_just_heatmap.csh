## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
set mountdir = `pwd`

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

#set com = "mmrc"
#set s1  = "mmc"
#set s2  = "raf"

 set com = "com"
 set s1  = "rec"
 set s2  = "lig"

set name = "${s1}_${s2}_${com}"

 set pdb = ""
 #set pdb = "_min"

foreach seed ( \
 "0"   \
 "5"   \
 "50"  \
 "500" \
) 

#set workdir  = $mountdir/${pdb}/014.seed_${seed}.footprint/
set workdir  = $mountdir/${pdb}/014.footprint/${name}_seed_${seed}/

#rm -rf $workdir
#mkdir -p $workdir
cd $workdir

set list = `ls ${mountdir}/${pdb}/007.snapshot_mmgbsa_${name}_${seed}/snapshot.*.rst`
#set prm  =  ${mountdir}/${pdb}/0003md_tleap/com1.mmrc.leap.prm7
#set prm  =  ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"

#set mask1 = "1-168,170-171"
#set mask2 = "169"

set mask1 = "1-468,966"
set mask2 = "469-965,967"

foreach rst ($list)

   echo $rst
   echo $rst:r
   echo $rst:t
   #cp $rst .
   #echo python ${script}/amber_reader_mod.py $prm $rst $mask1 $mask2
   #python ${script}/amber_reader_mod.py $prm ${rst:t} $mask1 $mask2 ${rst:t:r}_fp > ${rst:t:r}_fp.log

   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -641 > lab1.txt 
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -1555 | tail -1 >> lab1.txt 
#
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -641 > lab2.txt 
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -1555 | tail -1 >> lab2.txt 

   #mv vdw${rst:t:r}_fp.avg vdw${rst:t:r}_fp.avg.txt
   #mv ele${rst:t:r}_fp.avg ele${rst:t:r}_fp.avg.txt
 
   python ${script}/examples_analysis/heatmap_matrix_mod2.py vdw${rst:t:r}_fp.avg.txt 0.0 -1.0 1.0 lab1.txt lab2.txt >  ${rst:t:r}_heatmap_matrix.VDW.log
   python ${script}/examples_analysis/heatmap_matrix_mod2.py ele${rst:t:r}_fp.avg.txt 0.0 -50.0 50.0 lab1.txt lab2.txt >  ${rst:t:r}_heatmap_matrix.ES.log
   #exit
end # rst
end # seed

