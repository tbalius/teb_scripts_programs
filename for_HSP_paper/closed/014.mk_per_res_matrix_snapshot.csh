## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
set mountdir = `pwd`

 set com = "mmrc"
 set name = $com

 set pdb = ""

set workdir  = $mountdir/${pdb}/014.footprint_single_point/name_${name}/

rm -rf $workdir
mkdir -p $workdir
cd $workdir

echo "${mountdir}/${pdb}/0004.min/*.rst7"
ls ${mountdir}/${pdb}/0004.min/*.rst7

set list = `ls ${mountdir}/${pdb}/0004.min/*.rst7`
set prm  =  ${mountdir}/${pdb}/0003md_tleap/com1.mmrc.leap.prm7 
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"


#set mask1 = "1283-1469"
#set mask2 = "1-1282,1470-1556"
set mask1 = "1-640,1555"
set mask2 = "642-1281,1556"


python ${script}/amber_reader_get_labels.py $prm $mask1 $mask2 lab 

foreach rst ($list)
   echo $rst
   echo $rst:r
   echo $rst:t
   cp $rst .
   #echo python ${script}/amber_reader_mod.py $prm $rst $mask1 $mask2
   #python ${script}/amber_reader_mod.py $prm ${rst:t} $mask1 $mask2 ${rst:t:r}_fp > ${rst:t:r}_fp.log
   echo python ${script}/amber_reader_frame_by_frame.py $prm ${rst:t} $mask1 $mask2 ${rst:t:r}_fp
   python ${script}/amber_reader_frame_by_frame.py $prm ${rst:t} $mask1 $mask2 ${rst:t:r}_fp > ${rst:t:r}_fp.log


   # 1469 - 1283 = 186 -> 186 + 1 = 187
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -1469 | tail -187 > lab1.txt 
   # 1556 - 1470 = 86 -> 86 + 1 = 87
   # 2-10 -> 9 residues
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -1282 > lab2.txt 
   #cut -c 17-27 ${rst:r}.pdb | uniq | grep -v LIG  | sed -e 's/ //g' | head -1556 | tail -87 >> lab2.txt 

   mv vdw${rst:t:r}_fp.avg vdw${rst:t:r}_fp.avg.txt
   mv ele${rst:t:r}_fp.avg ele${rst:t:r}_fp.avg.txt
 
   #python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/plot_fp_mod.py vdw${rst:t:r}_fp.avg lab.txt 0.2
   #python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/plot_fp_mod.py ele${rst:t:r}_fp.avg lab.txt 5.0
   python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/heatmap_matrix_mod2.py vdw${rst:t:r}_fp.avg.txt 0.0 -1.0 1.0 lab.label1.txt lab.label2.txt >  ${rst:t:r}_heatmap_matrix.VDW.log
   python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/heatmap_matrix_mod2.py ele${rst:t:r}_fp.avg.txt 0.0 -50.0 50.0 lab.label1.txt lab.label2.txt >  ${rst:t:r}_heatmap_matrix.ES.log
   #exit
end # rst
#end # seed

