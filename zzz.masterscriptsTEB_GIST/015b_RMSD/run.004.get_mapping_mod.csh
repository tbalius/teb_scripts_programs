
# This script reads in the matrix, and creates a mapping between xtal-lig name and zinc id  
# ie 
# 25T ZINC08652421
# BEN ZINC00036634
# 1LQ ZINC00331945
# BZI ZINC00331902


 # source python
 source /nfs/soft/python/envs/complete/latest/env.csh


 set mountdir = `pwd`
 cd $mountdir/workingdir/smiles

 
python $mountdir/run.004.get_mapping_mod.py output2.tanimoto.matrix  pdbligands_mod2.smi zincligands_mod2.smi >! pdblig_to_zincname.temp.txt

awk '{print $2 " " $4}' pdblig_to_zincname.temp.txt | sort -u >! pdblig_to_zincname.txt

#rm pdblig_to_zincname.txt
#touch pdblig_to_zincname.txt
#
#set pdbliglist = ` grep -n "1\.00" output2.tanimoto.matrix | awk -F: '{print $1}'`
#
#
#foreach pdblig ($pdbliglist)
#
#  #echo -n "$pdblig : "
#  set pdbligname = `python getline.py pdbligands_mod2.smi $pdblig  | awk '{print $2}' `
#  set zincid = `grep -n "1\.00" output2.tanimoto.matrix | awk -F: '/^'$pdblig':/{print $2}' | sed 's/,/\n/g' | grep -n "1\.00" |  awk -F: '{print $1} '`
#  #echo -n "$zincid : "
#  set zincname = `python getline.py zincligands.smi $zincid  | awk '{print $2}'`
#  #echo  "===================="  
#  echo  "$pdbligname $zincname"  
#  echo  "$pdbligname $zincname" >> pdblig_to_zincname.txt 
#end 

