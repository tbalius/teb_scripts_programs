
set pwd  = `pwd`

set logchange = 0.5 
#set logchange = 1.0 

#set run1 = "vs_run1"
#set run1 = "vs_run2_gist0.3"
#set run2 = "vs_run3_nogist"

#set run1 = vs_run10_gist0.3_sph_MES_save10
#set run1 = vs_run12_fullgist_sph_MES_save10
#set run2 = vs_run11_nogist_sph_MES_save10
#set run1 = vs_run1001_fullgist
#set run2 = vs_run1002_nogist
set run1 = vs_run1005_fullgist_ph4
set run2 = vs_run1006_nogist_ph4

#set run1 = "vs_run5_justB"
#set run1 = "vs_run8_justB_scale0.3"
#set run2 = "vs_run6_justB_nogist"


#python get_list_logrankchange.py $run1/extract_all.sort.uniq_new.txt $run2/extract_all.sort.uniq_new.txt 3.0
#python get_list_log10rankchange.py $run1/extract_all.sort.uniq.txt $run2/extract_all.sort.uniq.txt 1.0
python get_list_log10rankchange.py $run1/extract_all.sort.uniq.txt $run2/extract_all.sort.uniq.txt ${logchange}

mv rankchangebeter1.txt ${run1}_${run2}_rankchangebeter1.txt
mv rankchangebeter2.txt ${run1}_${run2}_rankchangebeter2.txt
mv rankonly1.txt        ${run1}_${run2}_rankonly1.txt
mv rankonly2.txt        ${run1}_${run2}_rankonly2.txt

awk -F, '{print $1}' ${run1}_${run2}_rankchangebeter1.txt >! ${run1}_${run2}_rankchangebeter1_list.txt
awk -F, '{print $1}' ${run1}_${run2}_rankchangebeter2.txt >! ${run1}_${run2}_rankchangebeter2_list.txt

foreach run ($run1 $run2)

cd $pwd/$run
ls -l extract_all.sort.uniq.txt
python ~/zzz.scripts/remove_zincid_from_extract_all.py extract_all.sort.uniq.txt ${pwd}/${run1}_${run2}_rankchangebeter1_list.txt
mv extract_all.sort.uniq_new.txt extract_all.sort.uniq_rank_compare_${run1}and${run2}_best${run1}.txt

python ~/zzz.scripts/remove_zincid_from_extract_all.py extract_all.sort.uniq.txt ${pwd}/${run1}_${run2}_rankchangebeter2_list.txt
mv extract_all.sort.uniq_new.txt extract_all.sort.uniq_rank_compare_${run1}and${run2}_best${run2}.txt

wc -l ${pwd}/${run1}_${run2}_rankchangebeter1_list.txt
wc -l ${pwd}/${run1}_${run2}_rankchangebeter2_list.txt

$DOCKBASE/analysis/getposes.py -l 5000 -x 1 -f extract_all.sort.uniq_rank_compare_${run1}and${run2}_best${run1}.txt -o rank_compare.${run1}and${run2}_best${run1}.mol2
$DOCKBASE/analysis/getposes.py -l 5000 -x 1 -f extract_all.sort.uniq_rank_compare_${run1}and${run2}_best${run2}.txt -o rank_compare.${run1}and${run2}_best${run2}.mol2

end
