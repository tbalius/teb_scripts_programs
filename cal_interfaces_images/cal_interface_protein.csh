
# script written by Trent Balius, 2020

set tebtools = /home/baliuste/zzz.github/teb_scripts_programs/
set chimera  = /home/baliuste/zzz.programs/Chimera/chimera-1.13.1/bin/chimera

set mountdir = `pwd`

foreach pdb (`cat pdblist.txt`)
   set workdir = ${mountdir}/${pdb}_dimer_interface_protein/
   if (-e ${workdir}) then
       continue
   endif
   mkdir ${workdir}
   cd ${workdir}
   wget https://files.rcsb.org/download/${pdb}.pdb .
   ${chimera} --nogui --script ${tebtools}/zzz.scripts/writeunitcell_mod.py ${pdb}.pdb 
   #ls unitcell_*.pdb > pdblist_unitcell.txt
   ls unitcell.pdb > pdblist.txt 
   python ${tebtools}/zzz.scripts/pdb_model_separator.py pdblist.txt 
   ls unitcell_model_*.pdb > pdblist_unitcell.txt
   #python /home/baliuste/zzz.github/teb_scripts_programs/zzz.scripts/pdb_model_separator.py pdblist.txt 
   python ${tebtools}/zzz.scripts/process_interfaces_cal_centers.py unitcell.pdb pdblist_unitcell.txt 50 > interface.txt
end

