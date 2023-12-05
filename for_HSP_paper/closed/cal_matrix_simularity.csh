
set pwd = `pwd`
set workdir = ${pwd}/014.cal_matrix_simularity/

mkdir $workdir
cd $workdir

set matfile1 = ${pwd}/014.footprint_single_point_alt/name_mmrc/vdwcom1.mmrc.leap_fp.avg.txt # no fix
set matfile2 = ${pwd}/014.footprint_single_point_old/name_mmrc/vdwcom1.mmrc.leap_fp.avg.txt # fix

cp $matfile1 mat1.txt
cp $matfile2 mat2.txt

cp ${pwd}/014.footprint_single_point_alt/name_mmrc/lab.label1.txt .
cp ${pwd}/014.footprint_single_point_old/name_mmrc/lab.label2.txt .

#syntax:  matrix csv, matrix csv, heatmap_threshold heatmap_min heatmap_max label1_filename label2_filename
 python ~/zzz.github/teb_scripts_programs/py_amber_reader/examples_analysis/quantify_simularity.py mat1.txt mat2.txt 0.0 -1.0 1.0 lab.label1.txt lab.label2.txt > log.txt

