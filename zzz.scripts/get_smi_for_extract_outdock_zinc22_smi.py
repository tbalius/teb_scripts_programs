
# Written by Trent Balius (c) August 12, 2019
# modified on 2023
# Frederick National Lab for Cancer Research. 
# script to get smiles from zinc directories for extract all file entries

import sys,os


def get_smiles_from_extract_OUTDOCK_smi_files(input_extract_file,dpath,number,output_smiles_file):

   # this function will open up, the poses.threshold.dir.csv file, get the frist X zinc ids and the path to the dir with dock.out file.  
   # we will look into the split_database_index to get the path to where the smiles files are (an outer directory to where the tgz files of db2 files are).  

   dic_zinc_path = {}
   fh = open(input_extract_file,'r')

   zincid_sorted = []
   dic_zinc_smiles = {}
   count_lines = 0
   print ("step one. read in zincid from extract all")
   for line in fh: 
      if (count_lines >= number):
         break
      count_lines = count_lines + 1
      splitline = line.split(',')
      path = splitline[1]
      zincid = splitline[0]
      dic_zinc_path[zincid] = path
      zincid_sorted.append(zincid)
   fh.close()
   print ("step two. get path to smi files")
   flag_zinc = False
   count = 0
   #dic_zinc_path_db2 = {}
   for key in dic_zinc_path.keys(): 
      path_to_docking = dic_zinc_path[key].replace(dic_zinc_path[key].split('/')[-1],'')
      outdock = dpath+path_to_docking+'split_database_index'
      print(outdock)
      fh1 = open(outdock,'r')
      smi_dic = {}
      for line in fh1: 
         stripline = line.strip()
         print(stripline)
         smipath = stripline.replace(stripline.split('/')[-1],'').replace(stripline.split('/')[-2],'').replace('//','/')
         print(smipath)
         smi_dic[smipath] = 0
      fh1.close()
          
      print ("step two point one. get smiles")
      count = 0
      for smipath in smi_dic.keys():
          poh = os.popen('zcat %s/*.smi.gz | grep %s'%(smipath,key))
          for line in poh:
               print (line)
               #if not (key in dic_zinc_smiles.keys()): 
               if not (key in dic_zinc_smiles): 
                  dic_zinc_smiles[key] = []
               else: 
                  print("Warning:  "+key+"has more than one smi")
               dic_zinc_smiles[key].append(line.split()[0])
               count = count+1
          poh.close()
      #print(count)
      if count == 0: 
          print ("Could not find %s in %s"%(key,smipath))
          hacdir = stripline.split('/')[-3]
          hac = stripline.split('/')[-4]
          print(hacdir,hac)
          alt_dir = '/mnt/RAS-ZINK22/ZINC22_copy2_globus/2d-all'
          poh = os.popen('zcat %s/%s/%s.smi.gz | grep %s'%(alt_dir,hac,hacdir,key))
          for line in poh:
               print (line)
               #if not (key in dic_zinc_smiles.keys()): 
               if not (key in dic_zinc_smiles): 
                  dic_zinc_smiles[key] = []
               else: 
                  print("Warning:  "+key+"has more than one smi")
               dic_zinc_smiles[key].append(line.split()[0])
               count = count+1
          poh.close()
          #exit()
      #exit()

   print ("step three. write out smiles")
   fhout = open(output_smiles_file,'w')
   for zincid in zincid_sorted: 
       print(zincid)
       if not (zincid in  dic_zinc_smiles):
          print (zincid + " is not in  dic_zinc_smiles.  continue to next zincid... ")
          continue 
       #print (dic_zinc_smiles[zincid].strip())
       for smi in dic_zinc_smiles[zincid]:
           fhout.write('%s %s\n'%(smi,zincid))
   fhout.close()

def main():

   if (len(sys.argv) != 5): # if no input
        print (" (1) input file: extract_all.sort.uniq.txt")
        print (" (2) dir: directory where the docking was run. use '' if you are runing the script where docking is")
        print (" (3) number of lines  ");
        print (" (4) output file sorted smiles file");
        return

   extract = sys.argv[1]
   dirpath = sys.argv[2]
   num     = int(sys.argv[3])
   smiles  = sys.argv[4]
 
   print('extract file: %s\ndir=%s\nnumber:%d\nsmiles file:%s'%(extract,dirpath,num,smiles))

   get_smiles_from_extract_OUTDOCK_smi_files(extract,dirpath,num,smiles)
   
main()
