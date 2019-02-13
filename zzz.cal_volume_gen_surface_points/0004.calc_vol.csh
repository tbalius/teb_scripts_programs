
set pwd = `pwd`

foreach file (`ls ${pwd}/????/????_*_rec_aligned.pdb`)

   set dirname = $file:r:t 
   #echo $filename $file
   echo $dirname
   mkdir $dirname
   cd $dirname

   #python ~/zzz.scripts/volume_cal_sph.py close.sph 0.5 out
   python ~/zzz.scripts/volume_cal_sph.py close_cluster.sph 0.5 out

   cd ../
   #grep "^ATOM " ${file} > ${filename}_rec.pdb

end

