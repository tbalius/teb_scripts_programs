
mkdir 0001.files
cd 0001.files/

grep "^.....................A" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb | grep -v "ATP" > mon1_noATP.pdb
grep "^.....................A" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb | grep "ATP" > ATP_mon1.pdb

grep "^.....................B" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb | grep -v "ATP" > mon2_noATP.pdb
grep "^.....................B" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb | grep "ATP" > ATP_mon2.pdb

grep "^.....................C" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb  > RAF.pdb
grep "^.....................D" ../real_space_refined_421_coot_120322_real_space_refined_424_real_space_refined_427_Final_011823_real_space_refined_435_caps_fix.pdb  > CDC37.pdb
