

set filedir = /mnt/nfs/work/jklyu/AmpC/screen/large_scale_docking/AmpC_thin_spheres_2.0_2.0_and_tarted_wz_min_1000_mol2_score_filter/
set name    = "ZINC"
#set dirlist = dirlist_temp
set dirlist = dirlist_backup


rm zincid_list.txt 
touch zincid_list.txt

foreach dir (`cat ${filedir}/${dirlist} `)
  #echo ${filedir}/${dir}
  #ls -l ${filedir}/${dir}/OUTDOCK 
  #grep $name ${filedir}/${dir}//OUTDOCK | awk '{print $2}' | wc -l
  grep $name ${filedir}/${dir}/OUTDOCK | awk '{print $2}'  >> zincid_list.txt
end

cat zincid_list.txt | sort -u  >! zincid_list_uniq.txt

#cat zincid_list.txt | sort | uniq -c | awk '{if($1>1){print $0}} '| sort  

wc -l zincid_list.txt 
wc -l zincid_list_uniq.txt
