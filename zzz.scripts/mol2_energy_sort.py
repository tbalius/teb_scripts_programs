
import sys, os, math
import mol2_python3 as mol2
#import sph_lib

# This is written by Trent Balius at FNLCR
# written in Nov, 2020

def main():


   if len(sys.argv) != 3: # if no input
       print ("ERORR:")
       print ("syntex: mol2_energy_sort mol2_file(docked poses) output ")
       return
 

   infilemol2_poses     = sys.argv[1]
   outfile              = sys.argv[2]

   print ("input file (poses)     = %s"%infilemol2_poses)
   print ("outputprefix           = %s"%outfile)

   if infilemol2_poses.split('.')[-1] == 'mol2':
      print("reading in mol2")
      #mol2_vector  = mol2.read_Mol2_file(infilemol2_poses)
      mol2_vector  = mol2.read_Mol2_file_head(infilemol2_poses)
   if infilemol2_poses.split('.')[-1] == 'gz':
      print("reading in gz mol2 file")
      mol2_vector  = mol2.read_Mol2_file_head_gz(infilemol2_poses)


   count = 0
   energy_vec = []
   for mol in mol2_vector: 
          lines = mol.header.split('\n')  #file1.close()
          for line in lines:
              if 'Total' in line:
                  splitline = line.split()
                  energy = float(splitline[3])
                  energy_vec.append(energy)
   energy_vec_sort = sorted(enumerate(energy_vec), key=lambda x: x[1])
   #energy_vec_sort = sorted(enumerate(energy_vec), key=lambda x: -x[1])
   for entry in energy_vec_sort: 
       print(entry)
       print(entry[0])
       mol2.append_mol2(mol2_vector[entry[0]],outfile+'.mol2')
   #exit()
main()


