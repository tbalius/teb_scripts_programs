## This script writes out the last frame of the 10md trajectory as a reference pdb to which we can align.
## Ref is also a useful visual reference when visualizing gist.

## TEB / MF comments -- March 2017


set username = `whoami`
setenv AMBERHOME /home/$username/zzz.programs/amber/amber18 # change me

set mountdir  = `pwd`
set mountdir_ori = "${mountdir}/Closed_fix_2023_01_19_fix_cap" #change me
set scriptdir = "${mountdir}" #change me 

   #set seed = "0"
   #set seed = "5"
   #set seed = "50"
   #set seed = "no_restaint_0"

set com = "mmrc"
set s1  = "mmc"
set s2  = "raf"

 #set com = "mm"
 #set s1  = "m1"
 #set s2  = "m2"

set name = "${s1}_${s2}_${com}"

 set pdb = ""
 #set pdb = "_min"

set prm  =  ${mountdir_ori}/${pdb}/0003md_tleap/com1.mmrc.leap.prm7

foreach seed ( \
 "0"   \
 "5"   \
 "50"  \
 "500" \
) 

#set workdir  = $mountdir/${pdb}/014.seed_${seed}.footprint/
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/movie
#set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/mon2_C-terminal_w_mon1_SRC/
set workdir = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_seed_${seed}_noATP_noMG/SRC_vs_luminal_RAF/

##set mask1 = "3,9-11,16,18,22-23,32-33,37,40,44,95-96,98,120,156,297,299,322,339-340,342,346"
#set mask2 = "472,474,476-479,486,490-491,493,500-501,505,508,512,563-564,566,588,627,765,786,807-808,810-811,861" #Semi-open numbering
##set mask2 = "645,647,649-652,659,663-664,666,673-674,678,681,685,736-737,739,761,800,938,959,980-981,983-984,1034"

#set mask1 = "291-301" #SRC loop mon1
#set mask2 = "932-942" #SRC loop mon2

#set mask1 = "1284-1292,1342-1347" #RAF luminal density and RAF interacting residues
#set mask2 = "291-301,932-942,1489-1495" #SRC loop residues and HSP interacting residues

set mask1 = "291-301,932-942"
set mask2 = "1284-1292"

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,467,470,556,559,560,561,562"
#set mask2 = "836,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,952,955,956,957,958,960,961,962,963,964,966,967,969,1023,1024,1026,1027,1030,1031,1033,1034,1035,1036,1108,1111,1114,1115,1189,1193,1197,1200,1201,1202,1203,1204,1210,1211"

#set mask1 = "195,262,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,311,313,314,315,316,317,319,320,321,322,323,324,325,326,328,355,383,385,386,389,392,393,467,470,556,559,560,561,562,836,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,952,955,956,957,958,960,961,962,963,964,966,967,969,1023,1024,1026,1027,1030,1031,1033,1034,1035,1036,1108,1111,1114,1115,1189,1193,1197,1200,1201,1202,1203,1204,1210,1211,1484,1487,1488,1489,1490,1491,1492,1493,1497"

#set mask1 = "560-571,1201-1212"

#set mask2 = "1284,1285,1286,1287,1288,1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1313,1316,1317,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1349,1352,1355,1356"

#set mask1 = "1201-1212" #mon2 C-terminal residues 609-620

#set mask2 = "291-301" #SRC mon1

#set mask1 = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,86,90,93,94,95,96,97,98,99,102,119,120,122,123,124,125,126,128,129,148,150,151,152,153,154,155,156,157,158,159,160,162,177,183,313,337,338,339,340,341,342,343,344,345,346,348"

#set mask2 = "642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,673,674,730,731,732,734,735,736,737,738,739,740,742,743,760,761,762,763,764,765,766,767,769,770,787,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,818,824,836,837,959,978,979,980,981,982,983,984,985,986,987,988,989,992,993"

#exit

#rm -rf $workdir
#mkdir -p $workdir
cd $workdir

#ls -ltr $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/
#exit

python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/amber_reader_get_labels.py $prm $mask1 $mask2 temp

#set list = `ls $mountdir/${pdb}/014.footprint_matrix_overtime_/name_${name}_seed_${seed}/vdw* | awk -F. '{print $3}' | sort -n`
set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"

python3 ${mountdir}/convert_temp_label_to_original.py temp.label1.txt
python3 ${mountdir}/convert_temp_label_to_original.py temp.label2.txt

   #python /home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/heatmap_matrix_mod2.py vdwseed${seed}.avg 0.0 -1.0 1.0   temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.VDW.log
   python ${script}/examples_analysis/heatmap_matrix_mod2.py vdwseed${seed}.avg 0.0 -1.0 1.0   temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.VDW.log
   python ${script}/examples_analysis/heatmap_matrix_mod2.py eleseed${seed}.avg 0.0 -50.0 50.0 temp.label1_converted.txt temp.label2_converted.txt >  avg_heatmap_matrix.ES.log

end # seed
