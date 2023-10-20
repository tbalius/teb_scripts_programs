#!/usr/bin/python

import sys, os

def open_dock_out(dict_id,filename,score_txt,sval):
  fh = open(filename,'r')
  name = ''
  score = 100000.0
  for line in fh:
    splitline = line.split()
    if len(splitline) < 2:
      continue
    #if splitline[0] == "opening":
    #    filename = splitline[1].replace(":","")
    #    #print(filename)
    if splitline[0] == "Molecule:":
      #print(line)
      #name = splitline[1]
      split_dot_name = splitline[1].split('.')
      if len(split_dot_name) > 2: 
          print("Warning... name has more than one dot: %s"%splitline[1]) 
      name = split_dot_name[0]
    if splitline[0] == score_txt:
      #print(line)
      score = float(splitline[1])
      if score > sval: # go to next line and skip if the score is to large
         continue
      if name in dict_id:
        if dict_id[name][0] > score:
          dict_id[name][0] = score
      else:
        dict_id[name] = [score, filename]
      print (name, score)
  fh.close()

def mySortFunc(e):
  return e[0]

def write_extract(dict_id,file1,file2):
    fho = open(file1,'w')
    data = []
    for key in dict_id:
      name = key
      score = dict_id[name][0]
      filename = dict_id[name][1]
      ostring = "%s      1 %16s 1                       1           1    0.00   1         1         1      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f\n"%(filename, name, score)
      fho.write(ostring)
      data.append([score,name,filename])
    fho.close()
    data.sort(key=mySortFunc)
    fho = open(file2,'w')
    for ele in data:
      filename = ele[2]
      name = ele[1]
      score = ele[0]
      ostring = "%s       1 %16s 1                    1       1    0.00   1         1         1      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f\n"%(filename, name, score)
      fho.write(ostring)
    fho.close()

def main():

    print ("this script take 3 arguments: \n   (1) path to where the dock.out files are loctated: (dir/*/dock.out) ")
    print ("   (2) score_type: Chemgrid_Score, Grid_Score, or Descriptor_Score")
    print ("   (3) score cutoff value: the script will only output thing below this value")

    dict_id1 = {}
    dirpath1 = sys.argv[1]
    score_txt1 = sys.argv[2]
    if len(sys.argv) == 4: 
       val = float(sys.argv[3])
    elif len(sys.argv) == 3:
       val = 10.0
    else: 
       print("wrong number of inputs. ")
       exit(0) 
    
    if (score_txt1 != "Chemgrid_Score:" or score_txt1 != "Grid_Score:" or score_txt1 != "Descriptor_Score:"):
      print ("score_txt1 must be Chemgrid_Score: or Grid_Score: or Descriptor_Score:")
      exit
    filename2 = "extract_all.uniq.txt"
    filename3 = "extract_all.sort.uniq.txt"
    
    isdir = os.path.isdir(dirpath1)
    if not (isdir):
      #print("Error %s is not a dir"%dirpath1)
      #exit()
      print("Warning... %s is not a dir"%dirpath1)
    
    openhandel = os.popen('ls %s/dock.out'%dirpath1)
    
    for line in openhandel:
      filename1 = line.strip()
      open_dock_out(dict_id1,filename1,score_txt1,val)
    write_extract(dict_id1,filename2,filename3)
main()
