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

#set com = "com"
#set s1  = "rec"
#set s2  = "lig"
set com = "mm"
set s1  = "m1"
set s2  = "m2"

set name = "${s1}_${s2}_${com}"

 set pdb = ""
 #set pdb = "_min"

set filedir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/mon1_mon2_N-terminal_interaction
set workdir  = $mountdir/${pdb}/014.footprint_matrix_overtime/${name}_avg_over_seeds_noATP_noMG/mon1_mon2_N-terminal_interaction_sym

mkdir -p $workdir
cd $workdir

#set list = `ls ${mountdir}/${pdb}/007.snapshot_mmgbsa_${name}_${seed}/snapshot.*.rst`

set script = "/home/${username}/zzz.github/teb_scripts_programs/py_amber_reader/"


 grep -v "avg mat" $filedir/vdw.txt_out.csv > vdw.csv
 grep -v "avg mat" $filedir/ele.txt_out.csv > ele.csv

 cp $filedir/temp.label1_converted.txt label1.txt
 cp $filedir/temp.label2_converted.txt label2.txt

 python $script/examples_analysis/match_lab.py vdw.csv 0.0 -1.0 1.0 label2.txt label1.txt > vdw.1.log
 grep -v "avg mat" vdw.csv_sym_out.csv > vdw.csv_sym_out.csv_mod
 python $script/examples_analysis/quantify_symmetric.py vdw.csv_sym_out.csv_mod 0.0 -1.0 1.0 vdw.csvxlab_sym_out.txt vdw.csvylab_sym_out.txt > vdw.2.log


 python $script/examples_analysis/match_lab.py ele.csv 0.0 -50.0 50.0 label2.txt label1.txt > ele.1.log 
 grep -v "avg mat" ele.csv_sym_out.csv > ele.csv_sym_out.csv_mod
 python $script/examples_analysis/quantify_symmetric.py ele.csv_sym_out.csv_mod 0.0 -10.0 10.0 ele.csvxlab_sym_out.txt ele.csvylab_sym_out.txt > ele.2.log


