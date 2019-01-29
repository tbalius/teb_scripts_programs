

set dir = 

#parm rec.wat.leap.prm7 
#rec_w_h means with hydrogens added with reduces.
cat << EOF >! makeref.in 
parm rec.watbox.leap.prm7 
#parm rec_w_h.wat.leap.prm7
# 10md.rst7 is the start of the second 5 ns of production
trajin 10md.rst7 1 1 
strip :WAT
trajout ref.pdb pdb
go
EOF

/nfs/soft/amber/amber14/bin/cpptraj -i makeref.in > ! makeref.log &
