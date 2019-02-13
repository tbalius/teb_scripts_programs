
set pwd = `pwd`

foreach file (`ls ${pwd}/4W5?/4W5?_?_rec_aligned.pdb`)

   set dirname = $file:r:t 
   #echo $filename $file
   echo $dirname
   #mkdir $dirname
   cd $dirname

   python /mnt/nfs/home/tbalius/zzz.github/DOCK/proteins/thinspheres/thin_spheres.py -i rec.ms -o surface.sph -d 0.0 -s 0.1 > thin_spheres.log
   python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py surface.sph ../4W52/xtal-lig_aligned.pdb pocket.sph 6  
   $DOCKBASE/proteins/showsphere/doshowsph.csh pocket.sph 1 pocket_spheres.pdb

   cd ../
   #grep "^ATOM " ${file} > ${filename}_rec.pdb

end

