#setenv AMBERHOME /nfs/soft/amber/amber14

#setenv AMBERHOME /nfs/soft/amber/amber14
#setenv LD_LIBRARY_PATH ""
#setenv LD_LIBRARY_PATH "/usr/local/cuda-6.0/lib64/:$LD_LIBRARY_PATH"

#set pdb = "5VBE"
set mol2file = "." 
#cd ${pdb}/004.min  
#cd 004.min  
cd ${mol2file}/0004.min  
   $AMBERHOME/bin/ambpdb -p com4.mm.leap.prm7 -c 01mi.rst7 > 01mi.pdb
#   $AMBERHOME/bin/ambpdb -p lig.leap.prm7 < 01mi.lig.rst7 > 01mi.lig.pdb
