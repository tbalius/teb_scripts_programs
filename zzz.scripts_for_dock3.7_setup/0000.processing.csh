
  cut -c 1-21 rec.pdb > rec_temp1.pdb
  cut -c 23-78 rec.pdb > rec_temp2.pdb
  #paste -d' ' rec_temp1.pdb rec_temp2.pdb > rec_mod2.pdb
  paste -d' ' rec_temp1.pdb rec_temp2.pdb > rec_mod.pdb

  grep "GNP" rec_mod.pdb >cof.pdb
  grep -v "GNP" rec_mod.pdb >rec_mod_no_cof.pdb 

