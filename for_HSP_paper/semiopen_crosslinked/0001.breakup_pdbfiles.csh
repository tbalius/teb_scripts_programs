
cd 0001.files/

grep "^.....................A" ../add_caps/real_space_refined_032_coot_041923_real_space_refined_034_mod_capped.pdb | grep -v "ATP" > mon1_noATP.pdb
grep "^.....................A" ../add_caps/real_space_refined_032_coot_041923_real_space_refined_034_mod_capped.pdb | grep "ATP" > ATP_mon1.pdb

grep "^.....................B" ../add_caps/real_space_refined_032_coot_041923_real_space_refined_034_mod_capped.pdb | grep -v "ATP" > mon2_noATP.pdb
grep "^.....................B" ../add_caps/real_space_refined_032_coot_041923_real_space_refined_034_mod_capped.pdb | grep "ATP" > ATP_mon2.pdb

