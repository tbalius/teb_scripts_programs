#$ -S /bin/csh
#$ -cwd
#$ -l mem_free=1G       # Memory usage, required.  Note that this is per slot
#$ -l h_rt=50:00:00     # Runtime estimate, highly recommended
#$ -V                   # Pass current environment to exec node, required
#$ -o sge.out
#$ -j yes
#$ -t 1-4879

source ~/.cshrc_amber

set list = ` ls $PWD/*.mol2 `
set mol2="${list[$SGE_TASK_ID]}"
echo $mol2

set name = ${mol2:t:r} 
echo $name

mkdir -p $name
cd $name

cp $mol2 ./lig_in.mol2

obabel -imol2 -osdf lig_in.mol2 -O lig_ob.sdf
~/programs/anaconda3/envs/oepython3/bin/python ~/work/scripts/prep_ligParams_dockPose.py -l lig_in.mol2

if !( -s lig_bcc.mol2 ) then
    echo "lig_bcc.mol2 is not found"
    echo "ligand parameterizatin failed"
    cat sqm.out
    touch ligParam_failed
    exit 
endif


### complex minimization

ln -s /mnt/nfs/ex9/work/yingyang/1_strain/8_autodude_9sys/HS90A/strain_min1/prot_prep.pdb        rec.pdb

$AMBERHOME/bin/tleap -s -f ../tleap.in > ! tleap.out

$AMBERHOME/bin/sander -O -i ../01mi.com.in -o 01mi.com.out \
-p com.leap.parm7 -c com.leap.rst7 -ref com.leap.rst7 \
-x 01mi.com.nc -inf 01mi.com.info -r 01mi.com.rst7

#set a = `grep -A5 FINAL 01mi.com.out | tail -1 | awk '{print $2}'`
#if ! ( `awk -v a="$a" -v b=0 'BEGIN{print(a<b)}' ` ) then
#    echo "\n\n\n ERROR \n\n\n FIX complex minimization\n\n\n "
#    $AMBERHOME/bin/sander -O -i ../01mi.com.in -o 01mi.com.out \
#    -p com.leap.parm7 -c com.leap.rst7 -ref com.leap.rst7 \
#    -x 01mi.com.nc -inf 01mi.com.info -r 01mi.com.rst7
#endif

$AMBERHOME/bin/ambpdb -p com.leap.parm7 -c 01mi.com.rst7 > 01mi.com.pdb

grep LIG 01mi.com.pdb > 01mi.lig.extracted.pdb
python ~/work/scripts/convert_pdb_to_crd.py 01mi.lig.extracted.pdb \
01mi.lig.extracted.rst7 01mi.lig.extracted.log

sed "/LIG/d" 01mi.com.pdb > 01mi.rec.extracted.pdb
python ~/work/scripts/convert_pdb_to_crd.py 01mi.rec.extracted.pdb \
01mi.rec.extracted.rst7 01mi.rec.extracted.log

$AMBERHOME/bin/sander -O -i ../02sp.in -o 02sp.lig.out \
-p lig.leap.parm7 -c 01mi.lig.extracted.rst7 \
-inf 02sp.lig.info -r 02sp.lig.rst7

$AMBERHOME/bin/sander -O -i ../02sp.in -o 03sp.rec.out \
-p rec.leap.parm7 -c 01mi.rec.extracted.rst7 \
-inf 03sp.rec.info -r 03sp.rec.rst7


#set c = `grep -A5 FINAL 01mi.com.out | awk '{if (NF==6){print $0}}' | grep -v "NSTEP" | awk '{print $2}'`
#if ! ( `awk -v c="$c" -v b=0 'BEGIN{print(c<b)}' ` ) then
#    echo "ERROR: Sys Blow Up \n\n"
#    touch complexMin_failed
#    exit 
#endif


### omega && global minimum

$AMBERHOME/bin/ambpdb -mol2 -sybyl -p lig.leap.parm7 -c lig.leap.rst7 > lig.leap.mol2

~/programs/anaconda3/envs/oepython3/bin/python ~/work/scripts/omega_conformers.py lig_in.mol2 200
#python ~/work/scripts/omega_conformers.py lig_ob.sdf 200

if !( -s ligand_confs.mol2 ) then
    echo 'Empty'
    ~/programs/anaconda3/envs/oepython3/bin/python ~/work/scripts/omega_conformers.py lig_oe.mol2 200
endif

python ~/work/scripts/separate_mol2_more10000.py ligand_confs.mol2 ligand_confs

rm -f omega*.mdcrd
touch omega.mdcrd
echo "omega confs" >> omega.mdcrd

foreach mol2file (`ls ligand_confs_*.mol2`)
    set prefix = $mol2file:t:r
    echo $mol2file $prefix
    obabel -imol2 $mol2file -opdb -O $prefix.pdb
    python ~/work/scripts/convert_pdb_to_mdcrd.py $prefix.pdb $prefix.crd log
    tail -n +3 $prefix.crd >> omega.mdcrd
end

rm -f ligand_confs_*

$AMBERHOME/bin/sander -O -i ../03mi.omega.in -o 03mi.omega.out \
-p lig.leap.parm7 -c lig.leap.rst7 -y omega.mdcrd \
-x 03mi.omega.mdcrd -inf 03mi.omega.info -r 03mi.omega.rst7

set a = `grep -c TIMING 03mi.omega.out`        
set val = `cat 03mi.omega.out | grep -A5 FINAL | awk '{if (NF==6){print $0}}' | grep -v "NSTEP" | awk '{if($2 == "NaN"){printf "100000\n"}else {printf "%f\n", $2}}' | sort -nr | tail -1 `
if ( $a <= 0 ) then
    echo "ERROR: omega $name\n\n"
    touch omegaMin_failed
    exit 
else if ("$val" == "") then
    echo "ligand_confs not generated  $name\n"
    touch omegaMin_failed
    exit 
endif

