


#foreach dir ( "home"  "work" "reshwork" "ex9/work" "ex1/work" "scratch/A" )
foreach dir (  "work" "reshwork" "ex9/work" "ex1/work" "scratch/A" )

cd /nfs/$dir

set name = $dir:h

echo $name $dir

#exit

set date = `date +%Y-%m-%d-h%H`


#find tbalius/ -name 'run.*.csh' -o -name '0*.csh' -o -name '*.py' | tar -cvzf /nfs/home/tbalius/zzz.backup/work_backup.${date}.tar.gz --files-from -

find tbalius/ -name 'run.*.csh' -o -name '*README*' -o -name '0*.csh' -o -name '*.py' | tar -cvzf /nfs/home/tbalius/zzz.backup/${name}_backup.${date}.tar.gz --files-from -

#tar -cvzf /nfs/home/tbalius/zzz.backup/work_backup.${date}.tar.gz tbalius/T4_Lys/*.py

end

