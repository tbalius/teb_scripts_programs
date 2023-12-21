 2015  cd for_HSP_paper/
 2016  ls -ltr 
 2017  git add semiopen/*
 2018  git add semiopen/prm_crds/*
 2019  git add semiopen_crosslinked/*
 2020  git add semiopen_crosslinked/prm_crds/
 2021  git add semiopen_crosslinked/prm_crds/*
 2022  git commit 
 2023  git commit -a
 2024  cd closed/prm_crds/
 2025  ls -ltr 
 2026  ~/zzz.programs/amber/amber18/bin/ambpdb --help
 2027  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb --help
 2028  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 < com1.watbox.leap.rst7 > com1.watbox.leap.pdb
 2029  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 < 04mi.rst7 > 04mi.pdb
 2030  ls -ltr 
 2031  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c < 04mi.rst7 > 04mi.pdb
 2032  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c 04mi.rst7 > 04mi.pdb
 2033  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c 18md_replica1.rst7 > 18md_replica1.pdb
 2034  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c 18md_replica2.rst7 > 18md_replica2.pdb
 2035  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c 18md_replica3.rst7 > 18md_replica3.pdb
 2036  ~/zzz.programs/amber/amber22_ambertools23/amber22/bin/ambpdb -p com1.watbox.leap.prm7 -c 18md_replica4.rst7 > 18md_replica4.pdb
 2037  ls -ltr 
 2038  vim 18md_replica1.pdb 
 2039  ls -ltr 
 2040  history | tail -50 >  README.txt
