
set pwd = `pwd`

#set pwd_sed = '\/mnt\/nfs\/ex9\/work\/tbalius\/model_system_reveiw\/volume_calc\/t4_merski' 

mkdir 0006_for_fig
cd 0006_for_fig

#foreach file (`ls ${pwd}/*/*_rec_aligned.pdb`)
foreach file (`ls ${pwd}/????/????_*_rec_aligned.pdb`)
#foreach file (`ls ${pwd}/4W59/4W5?_?_rec_aligned.pdb`)

   set dirname = $file:r:t 
   set pdbname = $file:h:t

   #echo $file:r
   #echo $file:h
   #echo $file:e
   echo $dirname $pdbname
   #echo $pwd/$dirname/pocket_filt_spheres.pdb
   #ls $pwd/$dirname/pocket_filt_spheres.pdb
   #ls -ltr $pwd/$pdbname/*aligned.pdb 
   cp $pwd/$dirname/pocket_filt_spheres.pdb ${dirname}_pocket_filt_spheres.pdb
   cp $pwd/$pdbname/*rec*aligned.pdb .
   cp $pwd/$pdbname/xtal-lig_aligned.pdb ${pdbname}_xtal-lig_aligned.pdb
   #exit
   #ls $pwd/${dirname}_d6/close.sph ${dirname}_d6_close.sph
   cp $pwd/${dirname}_d6/close.sph ${dirname}_d6_close.sph

cp $pwd/${dirname}_d6_noH/surface_filt.sph ${dirname}_d6_noH_surface_filt.sph
cp $pwd/${dirname}_d6_noH/pocket_filt_spheres.pdb ${dirname}_d6_noH_pocket_filt_spheres.pdb


   #exit
   #grep "^ATOM " ${file} > ${filename}_rec.pdb
   #exit
end

