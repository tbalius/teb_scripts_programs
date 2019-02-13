
set pwd = `pwd`
#4W59_A_rec_aligned/outgist_values.txt:molV 302.875000
#4W58_A_rec_aligned/outgist_values.txt:molV 306.875000
#4W57_B_rec_aligned/outgist_values.txt:molV 309.250000
#foreach file (`ls ${pwd}/4W59/4W5?_?_rec_aligned.pdb ${pwd}/4W58/4W5?_?_rec_aligned.pdb ${pwd}/4W57/4W5?_?_rec_aligned.pdb`)
foreach file (`ls ${pwd}/????/????_*_rec_aligned.pdb`)

   set dirname = $file:r:t 
   #echo $filename $file
   echo $dirname
   mkdir ${dirname}_d6_noH
   cd ${dirname}_d6_noH

   #cp $file rec.pdb
   grep -v ' H$' $file > rec.pdb
   sed -i 's/HETATM/ATOM  /g' rec.pdb

   #exit
   $DOCKBASE/proteins/dms/bin/dms rec.pdb -a -g dms.log -p -n -o rec.ms

cat << EOF > INSPH
rec.ms 
R            
X            
-0.1          
3.0          
0.2          
rec.sph 
EOF

   $DOCKBASE/proteins/sphgen/bin/sphgen

   # ../4W52/xtal-lig.pdb this is the benzene ligand
   #python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py rec.sph ../4W52/xtal-lig_aligned.pdb close.sph 6
   python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py rec.sph ../2AS1/xtal-lig_aligned.pdb close.sph 6
   python ~/zzz.scripts/volume_cal_sph.py close.sph 0.5 out

   python ~/zzz.github/teb_scripts_programs/zzz.scripts/close_sph_cluster.py rec.sph ../2AS1/xtal-lig_aligned.pdb close_cluster.sph

   cd ../
   #grep "^ATOM " ${file} > ${filename}_rec.pdb

end

