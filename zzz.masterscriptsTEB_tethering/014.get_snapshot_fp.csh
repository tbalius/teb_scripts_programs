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
set workdir  = $mountdir/${pdb}/014.footprint/seed_${seed}/

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
   echo python ${script}/amber_reader_mod.py $prm $rst 1-168,170-171 169
   #python ${script}/amber_reader.py $prm $rst 1-180,182-183 181 ${rst:r}_fp.txt
   #python ${script}/amber_reader_mod.py 
   #exit
   python ${script}/amber_reader_mod.py $prm ${rst:t} 1-168,170-171 169 ${rst:t:r}_fp
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/   /_/g' > lab.txt 
   cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' > lab.txt 
   mv vdw${rst:t:r}_fp.avg vdw${rst:t:r}_fp.avg.txt
   mv ele${rst:t:r}_fp.avg ele${rst:t:r}_fp.avg.txt
 
   python /home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/plot_fp_mod.py vdw${rst:t:r}_fp.avg lab.txt 0.2
   python /home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/plot_fp_mod.py ele${rst:t:r}_fp.avg lab.txt 5.0
   #exit
end # rst
end # seed

