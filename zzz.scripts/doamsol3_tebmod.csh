#!/bin/csh -f
# doamsol.csh

# modified by Trent E Balius Nov, 2013

set mol2file = $1

if -e temp.mol2 then 
    echo "exit . . . \n temp.mol2 exits"
    exit
endif

echo "runing amsol on $mol2file " 

ln -s $mol2file temp.mol2

set AMSOLEXE = amsol-mod4

echo " computing formal charges and generating input for AMSOL "
$DOCK_BASE/etc/mk_amslin-c.pl temp.mol2 temp

echo " running AMSOL for water solvent "
$AMSOLEXE temp.in-wat temp.o-wat  
$AMSOLEXE temp.in-hex temp.o-hex  

echo " extract data from amsol output"
        #$DOCK_BASE/etc/3Step.csh2 temp.o-wat
        #$DOCK_BASE/etc/3Step.csh2 temp.o-hex
        #$DOCK_BASE/etc/SubstrSolv2.pl temp.o-hex.d temp.o-wat.d temp.solv temp.err
        #$DOCK_BASE/etc/UpdatChrg.pl temp.mol2 temp.solv temp.nmol2 temp.err2

set process_amsol = ~tbalius/zzz.scripts/process_amsol_mol2.py 

python ${process_amsol} temp.o-wat temp.o-hex temp.mol2 output


