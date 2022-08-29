


#set pwd = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
set lig = DL2078
#set lig = DL1314_Protomer1 

foreach pose (   \
               1 \
               2 \
               3 \
)
set mountdir = ${mountdir_ori}/${mut}/${lig}/pose${pose}/
cd $mountdir
set pwd = $mountdir



  set workdir =   ${pwd}/010_rmsd_vs_mmgbsa/
  mkdir -p ${workdir}
  cd ${workdir}

  #E37C/DL2040/pose1/010_rmsd_vs_mmgbsa/full_0/mmgbsa.txt DGbind
  echo "DGbind" > mmgbsa.txt
  ls -ltr ${pwd}/010_rmsd_vs_mmgbsa/full_*/mmgbsa.txt
  #cat ${pwd}/010_rmsd_vs_mmgbsa/full_*/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
  cat ${pwd}/010_rmsd_vs_mmgbsa/full_0/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
  cat ${pwd}/010_rmsd_vs_mmgbsa/full_5/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
  cat ${pwd}/010_rmsd_vs_mmgbsa/full_50/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
 
  #awk '{print $2}' ../mmgbsa.dat >  mmgbsa.txt
  cp ../010.rmsd_4.0_mod/lig1.dat rmsd_lig.txt 

  paste rmsd_lig.txt mmgbsa.txt |awk '{print $2, $3}' > rmsd_vs_mmgbsa.txt

  python ${mountdir_ori}/plot_rmsd_mmgbsa.py rmsd_vs_mmgbsa.txt

end # pose
