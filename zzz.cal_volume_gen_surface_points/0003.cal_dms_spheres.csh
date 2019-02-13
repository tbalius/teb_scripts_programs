
set pwd = `pwd`

foreach file (`ls ${pwd}/????/????_*_rec_aligned.pdb`)

   set dirname = $file:r:t 
   #echo $filename $file
   echo $dirname
   mkdir $dirname
   cd $dirname

   cp $file rec.pdb
   sed -i 's/HETATM/ATOM  /g' rec.pdb

   $DOCKBASE/proteins/dms/bin/dms rec.pdb -a -g dms.log -p -n -o rec.ms

cat << EOF > INSPH
rec.ms 
R            
X            
-0.1          
4.0          
0.2          
rec.sph 
EOF

   $DOCKBASE/proteins/sphgen/bin/sphgen

   # ../4W52/xtal-lig.pdb this is the benzene ligand
   python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py rec.sph ../2AS1/xtal-lig_aligned.pdb close.sph 5

   cd ../
   #grep "^ATOM " ${file} > ${filename}_rec.pdb

end

