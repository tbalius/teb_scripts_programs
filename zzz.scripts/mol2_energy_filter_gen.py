
import sys, os, math
import mol2_python3 as mol2
#import sph_lib

# This is written by Trent Balius at FNLCR
# written in Nov, 2020

def main():


   if len(sys.argv) != 6: # if no input
       print ("ERORR:")
       print ("syntex: mol2_energy_filter mol2_file(docked poses) energy_threshold energyname cnum output ")
       print (" energyname is the name of the energy term and cnum is the column, eg 'Total Energy' where cnum is 4 or 'Footprint_Similarity_Score:' where cnum is 3")
       return
 

   infilemol2_poses     = sys.argv[1]
   val                  = float(sys.argv[2])
   ename                = sys.argv[3]
   cnum                 = int(sys.argv[4])
   outfile              = sys.argv[5]

   print ("input file (poses)     = %s"%infilemol2_poses)
   print ("energy threshold       = %f"%val)
   print ("outputprefix           = %s"%outfile)

   if infilemol2_poses.split('.')[-1] == 'mol2':
      print("reading in mol2")
      #mol2_vector  = mol2.read_Mol2_file(infilemol2_poses)
      mol2_vector  = mol2.read_Mol2_file_head(infilemol2_poses)
   if infilemol2_poses.split('.')[-1] == 'gz':
      print("reading in gz mol2 file")
      mol2_vector  = mol2.read_Mol2_file_head_gz(infilemol2_poses)


   count = 0
   for mol in mol2_vector: 
          #print(mol.header)
          lines = mol.header.split('\n')  #file1.close()
          for line in lines:
              #print(line)
              if ename in line:
                  #print(line)
                  splitline = line.split()
                  energy = float(splitline[cnum-1])
                  #print(energy) 
          if energy < val: 
             print(energy) 
             mol2.append_mol2(mol,outfile+'.mol2')
   #exit()
main()


