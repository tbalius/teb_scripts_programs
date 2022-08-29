## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set mountdir = `pwd`

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

 set pdb = ""
 #set pdb = "_min"

foreach seed ("0" "5" "50") 

#set workdir  = $mountdir/${pdb}/014.seed_${seed}.footprint/
set workdir  = $mountdir/${pdb}/014.footprint_everything/seed_${seed}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

set list = `ls ${mountdir}/${pdb}/007.snapshot_mmgbsa_${seed}/snapshot.*.rst`
set prm  =  ${mountdir}/${pdb}/003md_tleap/com.leap.prm7 
set script = "/home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/"


foreach rst ($list)

   echo $rst
   echo $rst:r
   echo $rst:t
   #exit
   cp $rst .
   echo python ${script}/amber_reader_mod.py $prm $rst 1-171 1-171
   #python ${script}/amber_reader.py $prm $rst 1-180,182-183 181 ${rst:r}_fp.txt
   #python ${script}/amber_reader_mod.py 
   #exit
   python ${script}/amber_reader_mod.py $prm ${rst:t} 1-171 1-171 ${rst:t:r}_fp > amber_reader.log
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/   /_/g' > lab.txt 
   cut -c 17-27 ${rst:r}.pdb | uniq | sed -e 's/ //g' > lab.txt 
   cp vdw${rst:t:r}_fp.avg vdw${rst:t:r}_fp.avg.txt
   cp ele${rst:t:r}_fp.avg ele${rst:t:r}_fp.avg.txt
 
   python /home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/heatmap_matrix_mod.py vdw${rst:t:r}_fp.avg 1.0 -1.0 1.0 lab.txt lab.txt > heatmap_matrix.VDW.log
   python /home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/heatmap_matrix_mod.py ele${rst:t:r}_fp.avg 50.0 -50.0 50.0 lab.txt lab.txt > heatmap_matrix.ES.log
   exit
end # rst
end # seed

