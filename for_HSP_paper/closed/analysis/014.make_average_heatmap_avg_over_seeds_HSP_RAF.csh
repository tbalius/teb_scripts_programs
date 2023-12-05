## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017
set username = `whoami`
setenv AMBERHOME /home/${username}/zzz.programs/amber/amber18

set mountdir  = `pwd`
#set mountdir_ori = "/mnt/projects/RAS-CompChem/static/work/HSP83_for_Lorenzo/Semi"
#set scriptdir = "/mnt/projects/RAS-CompChem/static/Mayukh/Diamond_FNL1333"

#set com = "com"
#set s1  = "rec"
#set s2  = "lig"
 set com = "mmrc"
 set s1  = "mmc"
 set s2  = "raf"

set name = "${s1}_${s2}_${com}"

 set pdb = ""

#set prm  =  ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7

 set interactiondir = distance-based_sel_bigplot
#set interactiondir = mon1_mon2_C-terminal_w_RAF
#set interactiondir = distance-based_sel
#set interactiondir = SRC_loops
#set interactiondir = mon1_C-terminal_w_mon2_SRC
#set interactiondir = mon2_C-terminal_w_mon1_SRC



set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/${interactiondir}_avg

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,453,456"
#set mask2 = "663,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,779,782,783,784,785,787,788,789,790,791,793,794,796,850,851,853,854,857,858,860,861,862,863,935,938,941,942"


if (-e $workdir) then
   echo "$workdir exists ... "
   ls -ltr $workdir
   exit
endif

mkdir -p $workdir
cd $workdir

touch vdw.txt
touch ele.txt
touch tot.txt

foreach seed ( \
 "0"   \
 "5"   \
 "50"  \
 "500" \
) 
   set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/${interactiondir}/
   cp ${filedir}/vdwseed${seed}.avg .
   cp ${filedir}/eleseed${seed}.avg .
   cp ${filedir}/totseed${seed}.avg .
   echo "vdwseed${seed}.avg 10000" >> vdw.txt
   echo "eleseed${seed}.avg 10000" >> ele.txt
   echo "totseed${seed}.avg 10000" >> tot.txt
end # seed

cp $filedir/temp.label1_converted.txt $filedir/temp.label2_converted.txt .
# SRC_loops does not have converted labels?  
#if ($interactiondir == SRC_loops) then
#  cp  $filedir/temp.label1.txt . 
#  ln -s temp.label1.txt temp.label1_converted.txt 
#  cp  $filedir/temp.label2.txt .
#  ln -s  temp.label2.txt temp.label2_converted.txt 
#else
#  cp $filedir/temp.label1_converted.txt $filedir/temp.label2_converted.txt .
#endif

#ls -ltr $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/
#exit

#set list = `ls $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/vdw* | awk -F. '{print $3}' | sort -n`
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"

# python3 ${mountdir}/convert_temp_label_to_original.py temp.label1.txt
# python3 ${mountdir}/convert_temp_label_to_original.py temp.label2.txt

 python ${script}/examples_analysis/heatmap_matrix_avg_multiple_csv.py vdw.txt 0.0 -1.0 1.0   temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.VDW.log
 python ${script}/examples_analysis/heatmap_matrix_avg_multiple_csv.py ele.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.ELE.log
 python ${script}/examples_analysis/heatmap_matrix_avg_multiple_csv.py tot.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.TOT.log




