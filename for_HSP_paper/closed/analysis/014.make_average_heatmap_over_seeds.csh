## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
#set scriptdir = "${mountdir}" #change me 

#set com = "mmrc"
#set s1  = "mmc"
#set s2  = "raf"

 set com = "mm"
 set s1  = "m1"
 set s2  = "m2"

set name = "${s1}_${s2}_${com}"

 set pdb = ""

#set prm  =  ${mountdir_ori}/0003md_tleap/com4.mm.leap.prm7
set prm = ${mountdir_ori}/${pdb}/0003md_tleap/com1.mmrc.leap.prm7

#set interactiondir = distance-based_sel
#set interactiondir = SRC_loops
#set interactiondir = mon1_C-terminal_w_mon2_SRC
#set interactiondir = mon2_C-terminal_w_mon1_SRC

#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/${interactiondir}_avg
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/SRC_vs_luminal_RAF/
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/mon1_mon2_C-terminal_w_RAF/
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/distance-based_sel_bigplot_avg/
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/distance-based_sel/
set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/mon1_mon2_N-terminal_interaction/

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,453,456"
#set mask2 = "663,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,779,782,783,784,785,787,788,789,790,791,793,794,796,850,851,853,854,857,858,860,861,862,863,935,938,941,942"

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,467,470,556,559,560,561,562,836,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,952,955,956,957,958,960,961,962,963,964,966,967,969,1023,1024,1026,1027,1030,1031,1033,1034,1035,1036,1108,1111,1114,1115,1189,1193,1197,1200,1201,1202,1203,1204,1210,1211,1484,1487,1488,1489,1490,1491,1492,1493,1497"

#set mask2 = "1284,1285,1286,1287,1288,1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1313,1316,1317,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1349,1352,1355,1356"

#Mon1-Mon2 distance-based sel

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,467,470,556,559,560,561,562"

#set mask2 = "836,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,952,955,956,957,958,960,961,962,963,964,966,967,969,1023,1024,1026,1027,1030,1031,1033,1034,1035,1036,1108,1111,1114,1115,1189,1193,1197,1200,1201,1202,1203,1204,1210,1211"

#set mask1 = "291-301,932-942"
#set mask2 = "1284-1292"

#set mask1 = "560-571,1201-1212"

#set mask2 = "1284,1285,1286,1287,1288,1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1313,1316,1317,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1349,1352,1355,1356"

set mask1 = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,86,90,93,94,95,96,97,98,99,102,119,120,122,123,124,125,126,128,129,148,150,151,152,153,154,155,156,157,158,159,160,162,177,183,313,337,338,339,340,341,342,343,344,345,346,348"

set mask2 = "642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,673,674,730,731,732,734,735,736,737,738,739,740,742,743,760,761,762,763,764,765,766,767,769,770,787,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,818,824,836,837,959,978,979,980,981,982,983,984,985,986,987,988,989,992,993"

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
   #set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/${interactiondir}/
   #set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/SRC_vs_luminal_RAF/
   #set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/mon1_mon2_C-terminal_w_RAF/
   #set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/distance-based_sel_bigplot/
   #set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/distance-based_sel/
   set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/mon1_mon2_N-terminal_interaction/
   cp ${filedir}/vdwseed${seed}.avg .
   cp ${filedir}/eleseed${seed}.avg .
   cp ${filedir}/totseed${seed}.avg .
   echo "vdwseed${seed}.avg 10000" >> vdw.txt
   echo "eleseed${seed}.avg 10000" >> ele.txt
   echo "totseed${seed}.avg 10000" >> tot.txt
end # seed

#cp ${filedir}/temp.label1.txt .
#cp ${filedir}/temp.label2.txt .

#cp $filedir/temp.label1_converted.txt $filedir/temp.label2_converted.txt .
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

python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/amber_reader_get_labels.py $prm $mask1 $mask2 temp

#set list = `ls $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/vdw* | awk -F. '{print $3}' | sort -n`
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"

 python3 ${mountdir}/convert_temp_label_to_original.py temp.label1.txt
 python3 ${mountdir}/convert_temp_label_to_original.py temp.label2.txt

 #python ${mountdir}/heatmap_matrix_avg_multiple_csv.py vdw.txt 0.0 -1.0 1.0   temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.VDW.log
 #python ${mountdir}/heatmap_matrix_avg_multiple_csv.py ele.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.ELE.log
 #python ${mountdir}/heatmap_matrix_avg_multiple_csv.py tot.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.TOT.log
 python ${script}/heatmap_matrix_avg_multiple_csv.py vdw.txt 0.0 -1.0 1.0   temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.VDW.log
 python ${script}/heatmap_matrix_avg_multiple_csv.py ele.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.ELE.log
 python ${script}/heatmap_matrix_avg_multiple_csv.py tot.txt 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.TOT.log

