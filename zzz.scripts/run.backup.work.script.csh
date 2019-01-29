


cd /nfs/work/

set date = `date +%Y-%m-%d-h%H`


find tbalius/ -name 'run.*.csh' -o -name '0*.csh' -o -name '*.py' | tar -cvzf /nfs/home/tbalius/zzz.backup/work_backup.${date}.tar.gz --files-from -


#tar -cvzf /nfs/home/tbalius/zzz.backup/work_backup.${date}.tar.gz tbalius/T4_Lys/*.py



