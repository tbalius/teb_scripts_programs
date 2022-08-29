


#set pwd = `pwd`
set mountdir_ori = `pwd`
set mut = E37C
#set lig = DL2040
set lig = DL2078
#set lig = DL1314_Protomer1 

set mountdir = ${mountdir_ori}/${mut}/${lig}/poses_all/
cd $mountdir
set pwd = $mountdir



  set workdir =   ${pwd}/010_rmsd_vs_mmgbsa/
  mkdir -p ${workdir}
  cd ${workdir}

  #E37C/DL2040/pose1/010_rmsd_vs_mmgbsa/full_0/mmgbsa.txt DGbind
  echo "DGbind" > mmgbsa.txt
  ls -ltr ${mountdir_ori}/${mut}/${lig}/pose1/010_rmsd_vs_mmgbsa/mmgbsa.txt

  cat ${mountdir_ori}/${mut}/${lig}/pose1/010_rmsd_vs_mmgbsa/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
  cat ${mountdir_ori}/${mut}/${lig}/pose2/010_rmsd_vs_mmgbsa/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
  cat ${mountdir_ori}/${mut}/${lig}/pose3/010_rmsd_vs_mmgbsa/mmgbsa.txt | grep -v DGbind >> mmgbsa.txt
 
  #awk '{print $2}' ../mmgbsa.dat >  mmgbsa.txt
  cp ../010.rmsd_4.0_mod/lig1.dat rmsd_lig.txt 

  paste rmsd_lig.txt mmgbsa.txt |awk '{print $2, $3}' > rmsd_vs_mmgbsa.txt

  python ${mountdir_ori}/plot_rmsd_mmgbsa.py rmsd_vs_mmgbsa.txt

