
# script written by Trent Balius, 2020

set tebtools = /home/baliuste/zzz.github/teb_scripts_programs/

set mountdir = `pwd`

#foreach pdb (`cat pdblist.txt`)
foreach pdb ("6GJ6")
#foreach pdb (`cat pdblist.txt`)
   set workdir = ${mountdir}/${pdb}_dimer_interface_protein/
   if (-e ${workdir}) then
       echo "${workdir} exists"
       continue
   endif
   mkdir ${workdir}
   cd ${workdir}
   wget https://files.rcsb.org/download/${pdb}.pdb .
   awk '{if($1=="DBREF"){print $2"_"$3, $7, $10-$9}}' ${pdb}.pdb > chains_uniprot.txt
   set thres_num_res = 100 
   set list_num_res = `awk '{if ($2 =="P01116"){print $3}}' chains_uniprot.txt`
   set count = 0
   foreach num_res ($list_num_res)
      echo $num_res
      if ($num_res > $thres_num_res) then
           #echo "i am here $count"
           @ count=$count + 1
           #echo "i am here $count"
      endif
   end
   if $count == 0 then 
       echo "skip $pdb, P01116 residues are two few"
       continue
   endif
   
   #python /home/baliuste/zzz.scripts/process_interfaces_cal_centers_for_chains.py ${pdb}.pdb > interface.txt
   #python /home/baliuste/zzz.scripts/process_interfaces_cal_centers_for_chains_substruct.py ${pdb}.pdb ${mountdir}/secondary_struct.txt > interface.txt
   #python /home/baliuste/zzz.scripts/process_interfaces_cal_centers_for_chains_substruct_bit.py ${pdb}.pdb ${mountdir}/secondary_struct.txt > interface.txt
   python ${tebtools}/zzz.scripts/process_interfaces_cal_centers_for_chains_substruct_bit.py ${pdb}.pdb ${mountdir}/secondary_struct.txt > interface.txt
end

