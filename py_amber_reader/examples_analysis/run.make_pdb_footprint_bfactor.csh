

#set namefull = "d1_1-201.d2_202-402"
#set name1    = "1-201"
#set name2    = "202-402"

#set namefull = "1-803.804-816"
#set name1    = "1-803"
#set name2    = "804-816"

#set namefull = "d1_1-201.d3_403-601"
#set name1    = "1-201"
#set name2    = "403-601"

set namefull = "d2_202-402.d4_602-803"
set name1    = "202-402"
set name2    = "602-803"

ls vdwfp.${namefull}.avg.png.vec1.txt vdwfp.${namefull}.avg.png.vec2.txt elefp.${namefull}.avg.png.vec1.txt elefp.${namefull}.avg.png.vec2.txt 

python /nfs/home/tbalius/zzz.scripts/pdb_put_new_bfactor.py ../01mi.pdb vdwfp.${namefull}.avg.png.vec1.txt ${name1}  vdwfp.${namefull}.avg.vec1
python /nfs/home/tbalius/zzz.scripts/pdb_put_new_bfactor.py ../01mi.pdb vdwfp.${namefull}.avg.png.vec2.txt ${name2} vdwfp.${namefull}.avg.vec2

python /nfs/home/tbalius/zzz.scripts/pdb_put_new_bfactor.py ../01mi.pdb elefp.${namefull}.avg.png.vec1.txt ${name1}  elefp.${namefull}.avg.vec1
python /nfs/home/tbalius/zzz.scripts/pdb_put_new_bfactor.py ../01mi.pdb elefp.${namefull}.avg.png.vec2.txt ${name2} elefp.${namefull}.avg.vec2



