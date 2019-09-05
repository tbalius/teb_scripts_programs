
# Written by Trent Balius (c) August 12, 2019
# Frederick National Lab for Cancer Research. 

import sys


def get_smiles_from_extract_OUTDOCK_smi_files(input_extract_file,dpath,number,output_smiles_file):

   # this function will open up, the extract all sort uniq file, get the frist X zinc ids and the path to the dir with OUTDOCK file.  
   # It will open the OUTDOCK file and get the db2 file that contains the zinc id. 
   # this it will convert the db2 path to the path to the simles path in that dir
   # It will open that smiles file and get the smiles that corespond with the zinc id. 

   #input_extract_file = 'extract_all.sort.uniq.txt'
   #number = 1000 # number of zincid to get. 
   #output_smiles_file = 'top.smi' 
 
   dic_zinc_path = {}
   fh = open(input_extract_file,'r')

   zincid_sorted = []
   count_lines = 0
   print "step one. read in zincid for extract all"
   for line in fh: 
      if (count_lines >= number):
         break
      count_lines = count_lines + 1
      #print(line)
      splitline = line.split()
      #print(splitline[0], splitline[2])
      path = splitline[0]
      zincid = splitline[2]
      dic_zinc_path[zincid] = path
      zincid_sorted.append(zincid)
   fh.close()
   print "step two. get path to db2file"
   flag_zinc = False
   count = 0
   dic_zinc_path_db2 = {}
   for key in dic_zinc_path.keys(): 
      #print(dic_zinc_path[key])
      outdock = dpath+dic_zinc_path[key]+'/OUTDOCK'
      fh1 = open(outdock,'r')
      flag_zinc = False
      for line in fh1: 
         #print(line) 
         splitline = line.split()
         zincid = ''
         if (len(splitline) > 3): 
            zincid = splitline[1]
            #print (key, zincid)
         if key == zincid:
             #print(key)
             flag_zinc = True
         if ("close the file:" in line): 
             if (flag_zinc):
                 dic_zinc_path_db2[key] = line
                 break
             flag_zinc = False
      fh1.close()
   dic_zinc_smifile = {}
   #print("I AM HERE")
   print "step three. convert db2 path to smile path"
   for key in dic_zinc_path_db2.keys(): 
       #print(key, dic_zinc_path_db2[key])
       path = dic_zinc_path_db2[key] 
       splitpath = path.strip().split('/')
       newpath = ''
       len_split_path = len(splitpath)
       if len_split_path < 4: 
           #print path
           exit()
       for i in range(1,len(splitpath)-1):
           strpath = splitpath[i]
           newpath = newpath + '/'+strpath
       
       newpath = newpath + '/'+splitpath[len_split_path-3]+splitpath[len_split_path-2]+'.smi'
       dic_zinc_smifile[key] = newpath
       #print(newpath)

   print "step four. get smiles"
   dic_zinc_smiles = {}
   for key in dic_zinc_smifile.keys(): 
       smifile = dic_zinc_smifile[key]
       #print smifile
       fhsmi = open(smifile)
       for line in fhsmi: 
           if key in line: 
              #print line 
              if key in dic_zinc_smiles: 
                 print "In dict dic_zinc_smiles"
              dic_zinc_smiles[key] = line
              break
   print "step five. print smiles in rank order"
   fhout = open(output_smiles_file,'w')
   for zincid in zincid_sorted: 
       print dic_zinc_smiles[zincid].strip()
       fhout.write(dic_zinc_smiles[zincid].strip()+'\n')
   fhout.close()

def main():

   if (len(sys.argv) != 5): # if no input
        print " (1) input file: extract_all.sort.uniq.txt"
        print " (2) dir: directory where the docking was run. use '' if you are runing the script where docking is"
        print " (3) number of lines  ";
        print " (4) output file sorted smiles file";
        return

   extract = sys.argv[1]
   dirpath = sys.argv[2]
   num     = int(sys.argv[3])
   smiles  = sys.argv[4]
 
   print('extract file: %s\ndir=%s\nnumber:%d\nsmiles file:%s'%(extract,dirpath,num,smiles))

   get_smiles_from_extract_OUTDOCK_smi_files(extract,dirpath,num,smiles)
   
main()
