
set pwd = `pwd`
#set pwd_sed = '\/mnt\/nfs\/ex9\/work\/tbalius\/model_system_reveiw\/volume_calc\/t4_merski' 

# this spheres fill the whole open state.  
$DOCKBASE/proteins/showsphere/doshowsph.csh 1KXM_ori_rec_aligned_d6_noH/close_cluster.sph 1 1KXM_ori_rec_aligned_d6_noH/close_cluster_ter.pdb
grep -v TER 1KXM_ori_rec_aligned_d6_noH/close_cluster_ter.pdb > 1KXM_ori_rec_aligned_d6_noH/close_cluster.pdb

foreach file (`ls ${pwd}/????/????_*_rec_aligned.pdb`)

   #set dirname = $file:r:t 
   set dirname = ${file:r:t}_d6_noH 
   #echo $filename $file
   echo $dirname

   #mkdir $dirname
   if (-e $pwd/$dirname/rec.site) then
       echo "$pwd/$dirname/rec.site exists"
       continue
   endif

   cd $dirname
   #cd ${dirname}_d6_noH


   pwd 
   ls 
   #cp /nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/filt.params . 
   #sed 's/xtal-lig.pdb/..\/2AS1\/xtal-lig_aligned.pdb/g' /nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/filt.params >  filt.params 
   sed 's/xtal-lig.pdb/..\/1KXM_ori_rec_aligned_d6_noH\/close_cluster.pdb/g' /nfs/home/tbalius/zzz.github/DOCK/proteins/defaults/filt.params >  filt.params 
   $DOCKBASE/proteins/filt/bin/filt < filt.params  > filt.log 
   #$DOCKBASE/proteins/dms/bin/dms rec.pdb -a -g dms_filt.log -p -n -i rec.site -d 0.2 -o rec_filt.ms
   #Here, the -d flag allows us to pass the program a scalar to modify the density of the surface points. For example, with a -d set to 1.0 the density will be 5.42 pts/sq.A, while with a -d 0.2, we will get a density of 1.18 pts/sq.A.
   #$DOCKBASE/proteins/dms/bin/dms rec.pdb -a -g dms_filt.log -p -n -i rec.site -d 1.0 -o rec_filt.ms
   $DOCKBASE/proteins/dms/bin/dms rec.pdb -a -g dms_filt.log -p -n -i rec.site -d 1.5 -o rec_filt.ms
   #exit
   # ../4W52/xtal-lig.pdb this is the benzene ligand
   #    python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py rec.sph ../4W52/xtal-lig_aligned.pdb close.sph 5
   #

   python /mnt/nfs/home/tbalius/zzz.github/DOCK/proteins/thinspheres/thin_spheres.py -i rec_filt.ms -o surface_filt.sph -d 0.0 -s 0.1 > thin_spheres_filt.log
   #python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py surface_filt.sph ../4W52/xtal-lig_aligned.pdb pocket_filt.sph 6  
   #python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py surface_filt.sph ../2AS1/xtal-lig_aligned.pdb pocket_filt.sph 6  
   #python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py surface_filt.sph ../2AS1/xtal-lig_aligned.pdb pocket_filt.sph 8  
   python /nfs/home/tbalius/zzz.scripts/close_sph_mod.py surface_filt.sph ../1KXM_ori_rec_aligned_d6_noH/close_cluster.pdb pocket_filt.sph 6  
   $DOCKBASE/proteins/showsphere/doshowsph.csh pocket_filt.sph 1 pocket_filt_spheres.pdb

   cd ../
   #grep "^ATOM " ${file} > ${filename}_rec.pdb
   #exit
end

