#!/usr/bin/python

import sys, os

def open_dock_out(dict_id,filename,score_txt):
  fh = open(filename,'r')
  name = ''
  score = 100000.0
  for line in fh:
    splitline = line.split()
    if len(splitline) < 2:
      continue
    if splitline[0] == "Molecule:":
      #name = splitline[1]
      split_dot_name = splitline[1].split('.')
      if len(split_dot_name) > 2: 
          print("Warning... name has more than one dot: %s"%splitline[1]) 
      name = split_dot_name[0]
    if splitline[0] == score_txt:
      score = float(splitline[1])
      if name in dict_id:
        if dict_id[name] > score:
          dict_id[name] = score
      else:
        dict_id[name] = score
      print (name, score)
  fh.close()

def mySortFunc(e):
  return e[0]

def write_extract(dict_id,file1,file2):
  fho = open(file1,'w')
  data = []
  for key in dict_id:
    name = key
    score = dict_id[name]
    ostring = "../AB/ABaaaaaa/t00003/ABaaaaaa0025  27991 %16s 1                    2702       2702    0.10  11         1      1612      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f\n"%(name, score)
    fho.write(ostring)
    data.append([score,name])
  fho.close()
  data.sort(key=mySortFunc)
  fho = open(file2,'w')
  for ele in data:
    name = ele[1]
    score = ele[0]
    ostring = "../AB/ABaaaaaa/t00003/ABaaaaaa0025  27991 %16s 1                    2702       2702    0.10  11         1      1612      1     1     0.00    0.00    0.00   0.00    0.00    0.00    0.00    0.00    0.00    %6.2f\n"%(name, score)
    fho.write(ostring)
  fho.close()

dict_id1 = {}
dirpath1 = sys.argv[1]
score_txt1 = sys.argv[2]

if (score_txt1 != "Chemgrid_Score:" or score_txt1 != "Grid_Score:" or score_txt1 != "Descriptor_Score:"):
  print ("score_txt1 must be Chemgrid_Score: or Grid_Score: or Descriptor_Score:")
  exit
filename2 = "extract_all.uniq.txt"
filename3 = "extract_all.sort.uniq.txt"

isdir = os.path.isdir(dirpath1)
if not (isdir):
  print("Error %s is not a dir"%dirpath1)
  exit()

openhandel = os.popen('ls %s/*/dock.out'%dirpath1)

for line in openhandel:
  filename1 = line.strip()
  open_dock_out(dict_id1,filename1,score_txt1)
write_extract(dict_id1,filename2,filename3)
