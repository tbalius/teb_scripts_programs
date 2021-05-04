
  set pwd = `pwd`
  set workdir = $pwd/0001.pdb_files

  set scriptdir = `pwd` 
  set name = "CYS"
  #set num  = " 37"
  set num  = "165"

  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/E37C/6GJ8-E37C/DL00230-pose1-E37C.pdb"
  #set pdbname = "DL00230-pose1-E37C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00912-pose1-D153C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00912-pose2-D153C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00329-pose1-D153C.pdb"
  set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/K165C/DL00131-pose1-K165C.pdb"
  set pdbname = "DL00131-pose1-K165C.pdb"

  if -e $workdir then
      echo "$workdir exists "
      exit
  endif
  
  mkdir $workdir
  cd $workdir


 #cp /is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/E37C/6GJ8-E37C/DL00230-pose1-E37C.pdb .
 #grep GCP DL00230-pose1-E37C.pdb  > cof.pdb
 #grep UNK DL00230-pose1-E37C.pdb  > lig.pdb
 #grep "^ATOM" DL00230-pose1-E37C.pdb | grep -v "^................B" | grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb
 #grep " MG " DL00230-pose1-E37C.pdb > ion.pdb

  cp $pdbfilepath .
  grep GCP $pdbname | sed -e 's/HETATM/ATOM  /g' | grep "^ATOM " | grep -v '^.............................................................................H' > cof.pdb
  #grep GNP $pdbname  > cof.pdb
  grep UNK $pdbname  > lig.pdb
  grep "^ATOM" $pdbname | grep -v "^................B" | grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb
  #grep " MG " $pdbname > ion.pdb
  grep " MG A 203 " $pdbname > ion.pdb
  #grep " MG  B   1 " $pdbname > ion.pdb # I am just getting one ion.  


  #sed -i 's/HETATM/ATOM  /g' cof.pdb
 
  python ${scriptdir}/get_sphere_atoms_cys_covalent.py rec.pdb ${name} ${num} rec_sph
  #python ${scriptdir}/change_cys_to_ala.py rec.pdb ${name} ${num} rec_mod

   sed -e 's/'${name}'/LIG/g' -e 's/ '${num}' /   1 /g' rec_sph_SG_CB.pdb -e 's/ A /   /g' > lig_aduct.pdb
   head -1 lig.pdb | cut -c 18-20
   set ligname = `head -1 lig.pdb | cut -c 18-20`
   set ligresid = `head -1 lig.pdb | cut -c 24-27`
   sed -e 's/'$ligname'/LIG/g' -e 's/ '$ligresid' /   1 /g' -e 's/HETATM/ATOM  /g'  lig.pdb >> lig_aduct.pdb

   # change the N (or C) to O.  
   #mv cof.pdb cof_N.pdb
   mv cof.pdb cof_C.pdb
   #python ${scriptdir}/replace_atom_ele.py cof_N.pdb "N3B" "N" "O" cof 
   python ${scriptdir}/replace_atom_ele.py cof_C.pdb "C3B" "C" "O" cof 
   #
   #set line = `grep " N3B " cof.pdb `
   #set modline = `echo $line | sed -e 's/N/O/g'`
   #
   # echo $line
   # echo $modline

   #mv cof.pdb cof_N.pdb
   ##echo "sed -e s/$line/$modline/g cof_N.pdb > cof.pdb"
   #sed -e "s/$line/$modline/g" cof_N.pdb > cof.pdb
   ##exit
   ##         CONECT    5    2
   #echo "CONECT  583 2753" >> lig_aduct.pdb
   #echo "CONECT  2647 2940" >> lig_aduct.pdb

  /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_dockprep.py lig_aduct.pdb lig_aduct_mod "
  #/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_dockprep.py cof.pdb cof "
  /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_addh.py cof.pdb cof "
 

