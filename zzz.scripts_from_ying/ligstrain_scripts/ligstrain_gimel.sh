#! /bin/tcsh
#


#====== INPUT section =======#

# ligands mol2 file
set lig_file = 'poses.mol2'

# receptor pdb file 
set prot_file = 'rec.crg.pdb'

# amber mask for atom restrain during minimization
set prot_mask = ':LIG>:3.5&!(@H=)'
echo $prot_mask

#====== END of INPUT ========#
set mntdir = `pwd`

mkdir -p calc_lig_strain
cd       calc_lig_strain

/nfs/home/yingyang/programs/anaconda3/envs/oepython3/bin/python \
/nfs/home/yingyang/work/scripts/split_mol_pybel.py ${mntdir}/${lig_file} 0

set num  = ` ls *.mol2 | wc -l `
echo $num

source /nfs/home/yingyang/.cshrc_amber
$AMBERHOME/bin/pdb4amber -i $prot_file -o prot_prep.pdb -y

cat << EOF > qsub.lig_strain.csh
#\$ -S /bin/csh
#\$ -cwd
#\$ -l mem_free=1G       # Memory usage, required.  Note that this is per slot
#\$ -l h_rt=50:00:00     # Runtime estimate, highly recommended
#\$ -V                   # Pass current environment to exec node, required
#\$ -o sge.out
#\$ -j yes

source /nfs/home/yingyang/.cshrc_amber

obabel -imol2 -osdf lig_in.mol2 -O lig_ob.sdf
/nfs/home/yingyang/programs/anaconda3/envs/oepython3/bin/python \
/nfs/home/yingyang/work/scripts/prep_ligParams_dockPose.py -l lig_in.mol2

if !( -s lig_bcc.mol2 ) then
    echo "lig_bcc.mol2 is not found"
    echo "ligand parameterizatin failed"
    cat sqm.out
    touch ligParam_failed
    exit 
endif


### complex minimization

ln -s ${mntdir}/${prot_file}        rec.pdb

\$AMBERHOME/bin/tleap -s -f tleap.in > ! tleap.out

\$AMBERHOME/bin/sander -O -i 01mi.com.in -o 01mi.com.out \
-p com.leap.parm7 -c com.leap.rst7 -ref com.leap.rst7 \
-x 01mi.com.nc -inf 01mi.com.info -r 01mi.com.rst7


set a = \`grep -A5 FINAL 01mi.com.out | tail -1 | awk '{print \$2}'\`
if ! ( \`awk -v a="\$a" -v b=0 'BEGIN{print(a<b)}' \` ) then
    echo "\n\n\n ERROR \n\n\n FIX complex minimization\n\n\n "
    \$AMBERHOME/bin/sander -O -i ../01mi.com.in -o 01mi.com.out \
    -p com.leap.parm7 -c com.leap.rst7 -ref com.leap.rst7 \
    -x 01mi.com.nc -inf 01mi.com.info -r 01mi.com.rst7
endif

\$AMBERHOME/bin/ambpdb -p com.leap.parm7 -c 01mi.com.rst7 > 01mi.com.pdb

grep LIG 01mi.com.pdb > 01mi.lig.extracted.pdb
python /nfs/home/yingyang/work/scripts/convert_pdb_to_crd.py 01mi.lig.extracted.pdb \
01mi.lig.extracted.rst7 01mi.lig.extracted.log

sed "/LIG/d" 01mi.com.pdb > 01mi.rec.extracted.pdb
python /nfs/home/yingyang/work/scripts/convert_pdb_to_crd.py 01mi.rec.extracted.pdb \
01mi.rec.extracted.rst7 01mi.rec.extracted.log

\$AMBERHOME/bin/sander -O -i 02sp.in -o 02sp.lig.out \
-p lig.leap.parm7 -c 01mi.lig.extracted.rst7 \
-inf 02sp.lig.info -r 02sp.lig.rst7

\$AMBERHOME/bin/sander -O -i 02sp.in -o 03sp.rec.out \
-p rec.leap.parm7 -c 01mi.rec.extracted.rst7 \
-inf 03sp.rec.info -r 03sp.rec.rst7


set c = \`grep -A5 FINAL 01mi.com.out | awk '{if (NF==6){print \$0}}' | grep -v "NSTEP" | awk '{print \$2}'\`
if ! ( \`awk -v c="\$c" -v b=0 'BEGIN{print(c<b)}' \` ) then
    echo "ERROR: Sys Blow Up \n\n"
    touch complexMin_failed
    exit 
endif


### omega && global minimum

\$AMBERHOME/bin/ambpdb -mol2 -sybyl -p lig.leap.parm7 -c lig.leap.rst7 > lig.leap.mol2

python /nfs/home/yingyang/work/scripts/omega_conformers.py lig_in.mol2 200

if !( -s ligand_confs.mol2 ) then
    echo 'Empty'
    python /nfs/home/yingyang/work/scripts/omega_conformers.py lig_oe.mol2 200
endif

rm -f omega*.mdcrd
python /nfs/home/yingyang/work/scripts/separate_mol2_more10000.py ligand_confs.mol2 ligand_confs

touch omega.mdcrd
echo "omega confs" >> omega.mdcrd

foreach mol2file (\`ls ligand_confs_*.mol2\`)
    set prefix = \$mol2file:t:r
    echo \$mol2file \$prefix
    obabel -imol2 \$mol2file -opdb -O \$prefix.pdb
    python /nfs/home/yingyang/work/scripts/convert_pdb_to_mdcrd.py \$prefix.pdb \$prefix.crd log
    tail -n +3 \$prefix.crd >> omega.mdcrd
end

rm -f ligand_confs_*

\$AMBERHOME/bin/sander -O -i 03mi.omega.in -o 03mi.omega.out \
-p lig.leap.parm7 -c lig.leap.rst7 -y omega.mdcrd \
-x 03mi.omega.mdcrd -inf 03mi.omega.info -r 03mi.omega.rst7

set a = \`grep -c TIMING 03mi.omega.out\`        
set val = \`cat 03mi.omega.out | grep -A5 FINAL | awk '{if (NF==6){print \$0}}' | grep -v "NSTEP" | awk '{if(\$2 == "NaN"){printf "100000\n"}else {printf "%f\n", \$2}}' | sort -nr | tail -1 \`
if ( \$a <= 0 ) then
    echo "ERROR: omega \$name\n\n"
    touch omegaMin_failed
    exit 
else if ("\$val" == "") then
    echo "ligand_confs not generated  \$name\n"
    touch omegaMin_failed
    exit 
endif

EOF

cat << EOF >! tleap.in
set default PBradii mbondi2
source leaprc.protein.ff14SB
source leaprc.gaff

loadamberparams lig.frcmod
LIG = loadmol2  lig_bcc.mol2

prot   = loadpdb rec.pdb
sys    = combine {prot LIG}

saveamberparm prot   rec.leap.parm7 rec.leap.rst7
saveamberparm sys    com.leap.parm7 com.leap.rst7
saveamberparm LIG    lig.leap.parm7 lig.leap.rst7

quit
EOF

cat << EOF1 > ! 01mi.com.in
01mi.in: minimization with GB/SA
&cntrl
imin = 1, maxcyc = 2500, ntmin = 2, drms = 0.005, 
igb = 1, gbsa = 1,
ntx = 1, ntc = 1, ntf = 1,
ntb = 0, ntp = 0,
ntwx = 50, ntwe = 0, ntpr = 50, ntwr = 50,
cut = 999.9,
ntr = 1, restraint_wt = 250.00,
restraintmask='$prot_mask'
/

# ntr = 0,
EOF1

cat << EOF > ! 02sp.in
02sp.in: minimization with GB/SA
&cntrl
imin = 1, maxcyc = 1, ncyc = 1,  ntmin = 2,
igb=1, gbsa = 1,
ntx = 1, ntc = 1, ntf = 1,
ntb = 0, ntp = 0,
ntwx = 0, ntwe = 0, ntpr = 1,
cut = 999.9,
ntr = 0,
/
EOF

cat << EOF1 > ! 03mi.omega.in
01mi.in: minimization with GB/SA
&cntrl
imin = 5, maxcyc = 5000, ntmin = 2, 
igb = 1, gbsa = 1,
ioutfm = 0, 
ntx = 1, ntc = 1, ntf = 1,
ntb = 0, ntp = 0,
ntwx = 1, ntwe = 0, ntpr = 100,
cut = 999.9,
ntr = 0,
/
EOF1
