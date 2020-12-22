
# script written by Trent Balius, 2020
set tebtools = /home/baliuste/zzz.github/teb_scripts_programs/
set pwd = `pwd`

set list = `ls ${pwd}/*/*pdb`

foreach pdb ($list) 
   #echo ${pdb:r}
   #echo ${pdb:t}
   set name = ${pdb:t}
   set dir = "${pdb:r}_chains"
   mkdir $dir 
   cd $dir
   #ls ../$name > pdbfile.txt
   ls ../$name > pdb_models.txt
   #echo $dir
   python ${tebtools}/zzz.scripts_from_alyssa_klein/pdb_split_into_chains_mod.py 
   
end
