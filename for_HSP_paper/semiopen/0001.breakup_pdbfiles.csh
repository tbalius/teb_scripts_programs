
mkdir 0001.files/
cd 0001.files/

grep "^.....................A" ../add_caps/SemiOpenState_refine340_locscale41_isolde_092622_2_noHs_real_space_refined_394_coot_092722_real_space_refined_396_Final_011823_real_space_refined_432_mod_caps.pdb | grep -v "ATP" > mon1_noATP.pdb
grep "^.....................A" ../add_caps/SemiOpenState_refine340_locscale41_isolde_092622_2_noHs_real_space_refined_394_coot_092722_real_space_refined_396_Final_011823_real_space_refined_432_mod_caps.pdb | grep "ATP" > ATP_mon1.pdb

grep "^.....................B" ../add_caps/SemiOpenState_refine340_locscale41_isolde_092622_2_noHs_real_space_refined_394_coot_092722_real_space_refined_396_Final_011823_real_space_refined_432_mod_caps.pdb | grep -v "ATP" > mon2_noATP.pdb
grep "^.....................B" ../add_caps/SemiOpenState_refine340_locscale41_isolde_092622_2_noHs_real_space_refined_394_coot_092722_real_space_refined_396_Final_011823_real_space_refined_432_mod_caps.pdb | grep "ATP" > ATP_mon2.pdb

