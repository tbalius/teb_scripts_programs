
  set pwd = `pwd`

  set scriptdir = `pwd` 
  set name = "CYS"
  #set num  = " 37"
  #set num  = "165"
  #set num  = " 59"
  #set num  = "143"
   set num  = " 37"

  set mut = E37C 
  #set lig = DL2040 
  #set lig = DL2078 
  set lig = DL1314_Protomer1 
  #set lig = DL1314_Protomer2 
  foreach pose (  \
                1 \
                #2 \
                3 \
                4 \
  )
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/E37C/6GJ8-E37C/DL00230-pose1-E37C.pdb"
  #set pdbname = "DL00230-pose1-E37C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00912-pose1-D153C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00912-pose2-D153C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/D153C/DL00329-pose1-D153C.pdb"
  #set pdbfilepath = "/is2/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/Amber_covalent_tutorial/A59C/DL00733/pose2/try-min_1.pdb"
  set pdbfilepath = "/mnt/projects/RAS-CompChem/static/zzz.shared_files_RCC/Tethering_project/Amber_covalent_tutorial/SOS_pocket_targets/docked-poses/${mut}/${mut}-${lig}_${pose}.pdb"
  set pdbname = "${mut}-${lig}_${pose}.pdb"

  # make pose4 map to pose3. 
  if $pose == 3 then 
     set oldpose = $pose
     set pose = 2
     echo "pose$oldpose from docking is stored in a dir called pose $pose" 
  else if $pose == 4 then 
     set oldpose = $pose
     set pose = 3
     echo "pose$oldpose from docking is stored in a dir called pose $pose" 
  endif

  set workdir = $pwd/${mut}/${lig}/pose${pose}/0001.pdb_files

  if -e $workdir then
      echo "$workdir exists "
      exit
  endif
  
  mkdir -p $workdir
  cd $workdir

  cp $pdbfilepath .
  #grep GNP $pdbname | sed -e 's/HETATM/ATOM  /g' | grep "^ATOM " | grep -v '^.............................................................................H' > cof.pdb
  grep GCP $pdbname | sed -e 's/HETATM/ATOM  /g' | grep "^ATOM " | grep -v '^.............................................................................H' > cof.pdb
  grep UNK $pdbname  > lig.pdb
  grep "^ATOM" $pdbname | grep -v "^................B" | grep -v '^.............................................................................H' | grep -v " MG " > rec.pdb
  #grep " MG  B   1 " $pdbname > ion.pdb # I am just getting one ion.  
  #grep " MG A 203 " $pdbname > ion.pdb # I am just getting one ion.  
  grep " MG A 202 " $pdbname > ion.pdb # I am just getting one ion.  


 
  python ${scriptdir}/get_sphere_atoms_cys_covalent.py rec.pdb ${name} ${num} rec_sph
  #python ${scriptdir}/change_cys_to_ala.py rec.pdb ${name} ${num} rec_mod

   #sed -e 's/'${name}'/LIG/g' -e 's/ '${num}' /   1 /g' -e 's/ A /   /g' rec_sph_SG_CB.pdb > lig_aduct.pdb
   cat rec_sph_SG_CB.pdb | sed -e "s/${name}/LIG/g" -e "s/ ${num} /   1 /g"  > lig_aduct.pdb
   #cat rec_sph_SG_CB.pdb | sed -e "s/${name}/LIG/g" -e "s/ ${num} /   1 /g"  -e 's/ S /   /g' > lig_aduct.pdb
   #cat rec_sph_SG_CB.pdb lig_aduct.pdb
   #ls 
   head -1 lig.pdb 
   head -1 lig.pdb | cut -c 18-20
   head -1 lig.pdb | cut -c 24-27
   set ligname = `head -1 lig.pdb | cut -c 18-20`
   #set ligresid = "`head -1 lig.pdb | cut -c 24-27`"
   set ligresid = `head -1 lig.pdb | cut -c 24-27`
   echo "*$ligresid*"
   sed -e 's/'$ligname'/LIG/g' -e "s/ $ligresid /   1 /g" -e 's/HETATM/ATOM  /g'  lig.pdb >> lig_aduct.pdb


   #exit
   # change the N (or C) to O.  
   #mv cof.pdb cof_N.pdb
   mv cof.pdb cof_C.pdb
   #python ${scriptdir}/replace_atom_ele.py cof_N.pdb "N3B" "N" "O" cof 
   python ${scriptdir}/replace_atom_ele.py cof_C.pdb "C3B" "C" "O" cof 
   #echo "CONECT  911 2637" >> lig_aduct.pdb
   # ATOM    921  SG  LIG A   1     -13.062 -14.558   4.750  1.00  0.00              
   # ATOM   2765  S1  LIG     1     -11.951 -14.917   6.433  1.00  0.00           S  
  # echo "CONECT 2765  910" >> lig_aduct.pdb
  #echo "CONECT 2688  910 2687" >> lig_aduct.pdb
   #echo "CONECT 2703 2702 2234" >> lig_aduct.pdb
   echo "CONECT 2672 2673  571" >> lig_aduct.pdb
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

  #/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_dockprep.py lig_aduct.pdb lig_aduct_mod "
  #/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_addh.py lig_aduct.pdb lig_aduct_mod Nah"
  /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_addh.py lig_aduct.pdb lig_aduct_mod keepH"
  #/home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_dockprep.py cof.pdb cof "
  /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera --nogui --script "/home/baliuste/zzz.scripts/chimera_addh.py cof.pdb cof keepH"
 
end # pose 
