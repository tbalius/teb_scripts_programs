

rm rmsd_for_*.txt

set list = `awk '{print $1}' ligcode_to_pdb.txt`

#foreach pdbcode ($list)
foreach loop ( "A" "B" "C" "D")
#foreach loop ( "C")

echo $loop

set rmsd_str = ""

# standard "gist scaled by zerro"
# "gist-EswPlusEww_ref2" is gist scaled by -1.0

foreach type ( \
# "gist-EswPlusEww_ref2_scale2.0" \
  "standard" \
# "gist-EswPlusEww_ref2_scale-0.5" \
  "gist-EswPlusEww_ref2" \
  "gist-EswPlusEww_ref2_ener_t0.1_dens_t1.0" \
# "gist-EswPlusEww_ref2_scale-1.5" \
# "gist-EswPlusEww_ref2_scale-2.0" \
# "gist-EswPlusEww_ref2_scale-7.0" \
 #"gist_Esw_plus_Eww_ref2_precompute1.4" \
 #"gist_Esw_plus_Eww_ref2_coarse2" \
)

 echo -n " $type "
 #touch rmsd_for_${type}.txt

#if !(-e workingdir/DOCKING_$type/rmsd_${pdbcode}_CcP_$loop/rmsdcalc_scored.mol2) continue

#set rmsd = `grep HA_RMSDh workingdir/DOCKING_$type/rmsd_${pdbcode}_CcP_$loop/rmsdcalc_scored.mol2 | awk '{print $3}'`
#grep HA_RMSDh workingdir/DOCKING_$type/rmsd_*_CcP_$loop/rmsdcalc_scored.mol2 | awk 'BEGIN{sum=0;sum2=0;count=0}{if ($3 != -1000.0){sum = sum+$3;sum2=sum2+($3*$3);count=count+1}}END{print sum,"/"count," = ",sum/count " ; stan dev = " sqrt(sum2/count - (sum/count)^2)}'
#grep HA_RMSDh workingdir/DOCKING_$type/rmsd_*_CYTc_$loop/rmsdcalc_scored.mol2 | awk 'BEGIN{sum=0;sum2=0;count=0}{if ($3 != -1000.0){sum = sum+$3;sum2=sum2+($3*$3);count=count+1}}END{print sum,"/"count," = ",sum/count " ; stan dev = " sqrt(sum2/count - (sum/count)^2)}'

#ls -l workingdir/DOCKING_$type/
#ls -l workingdir/DOCKING_$type/rmsd_*_CcP_$loop/rmsdcalc_scored.mol2

#grep HA_RMSDh workingdir/DOCKING_$type/rmsd_*_CcP_$loop/rmsdcalc_scored.mol2 | awk 'BEGIN{sum=0;sum2=0;count=0}{if ($3 != -1000.0){sum = sum+$3;sum2=sum2+($3*$3);count=count+1}}END{mean=sum/count;std=sqrt(sum2/count - (sum/count)^2);print sum,"/"count," = ",mean " ; stan dev = ", std,";",mean,"+/-",std }'
grep HA_RMSDh workingdir_mod/DOCKING_$type/rmsd_*_CcP_$loop/rmsdcalc_scored.mol2 | awk 'BEGIN{sum=0;sum2=0;count=0}{if ($3 != -1000.0){sum = sum+$3;sum2=sum2+($3*$3);count=count+1}}END{mean=sum/count;std=sqrt(sum2/count - (sum/count)^2);print sum,"/"count," = ",mean " ; stan dev = ", std,";",mean,"+/-",std }'
end # type
end # loop
#end # pdbcode
