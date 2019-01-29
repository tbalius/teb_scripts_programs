
set mountdir = `pwd`
set PDBid = "4NVA"
set typelist = "_gist _gist_elstat0p9 _min _nogist"
set pdblist = `awk '{print $1}' $mountdir/workingdir/smiles/ligcode_to_pdb.txt`

cd $mountdir/workingdir
rm rmsd_for_*.txt

#foreach loop ( "A" "B" "C" "D")
#foreach loop ( "C")
#echo "$loop"
foreach pdbcode ($pdblist)

set rmsd = ""

foreach type ($typelist)

 touch rmsd_for_$PDBid${type}.txt

#if !(-e workingdir/DOCKING_$type/rmsd_${pdbcode}_CcP_$loop/rmsdcalc_scored.mol2) continue
if !(-e $mountdir/workingdir/$PDBid$type/rmsd_${pdbcode}/rmsdcalc_scored.mol2) continue

#set rmsd = `grep HA_RMSDh workingdir/DOCKING_$type/rmsd_${pdbcode}_CcP_$loop/rmsdcalc_scored.mol2 | awk '{print $3}'`
#set rmsd = `grep HA_RMSDh workingdir_mod/DOCKING_$type/rmsd_${pdbcode}_CcP_$loop/rmsdcalc_scored.mol2 | awk '{print $3}'`

#set rmsd = `grep HA_RMSDh workingdir/$PDBid$type/rmsd_${pdbcode}/rmsdcalc_scored.mol2 | awk '{print $3}'`
set rmsd = `grep HA_RMSDh $mountdir/workingdir/$PDBid$type/rmsd_${pdbcode}/rmsdcalc_scored.mol2 | awk '{print $3}'`
echo $pdbcode $type $rmsd
#echo ${pdbcode}_$loop  $rmsd >> rmsd_for_${type}_${loop}.txt
echo ${pdbcode} $rmsd >> rmsd_for_$PDBid${type}.txt
end
end
#end # loop

foreach threshold ( "0.5" "1.0" "1.5" "2.0")
#foreach threshold (  "1.0")
 echo "threshold = $threshold" 
 foreach file ( `ls rmsd_for_*.txt` )
   echo -n "$file "
   cat $file  | awk 'BEGIN{count = 0}{if ($2<'$threshold' && $2!=-1000.0){count=count+1}}END{print count}'
 end
end

paste rmsd_for_${PDBid}* > rmsd_comparison.txt

#set threshold = 1.0
#foreach threshold ( "0.5" "1.0" "1.5" "2.0")
# echo "threshold = $threshold" 

#foreach  type ($typelist)

 #paste rmsd_for_${type}_*.txt | awk '{print $2" "$4" "$6" "$8}' | awk '{min=1000;max=-1000;min_i=-1;for ( i=1; i<=NF; i++) { if(min > $i){min = $i; min_i=i}; if(max < $i){ max = $i} }; print $0 " ::: "min " " min_i}' > ! rmsd_all_loops_$type.txt

#cat rmsd_all_loops_$type.txt
#echo -n "$type "
#cat rmsd_all_loops_$type.txt | awk 'BEGIN{count = 0}{if ($6<'$threshold' && $6!=-1000.0){count=count+1}}END{print count}'

#end #type
#end #threshold
