

set chimerapath = "/raid3/software/chimera/chimera-1.6_64bit/bin/chimera" 

cat <<EOF > chimera_script.com
 # open files
 open 1M17.pdb 1M17.pdb
 # calculate rmsd
 rmsd #0:735-745@CA #1:735-745@CA
EOF

$chimerapath --nogui chimera_script.com


