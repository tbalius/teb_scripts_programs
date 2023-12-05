#! /usr/bin/python3

import sys
import os

dict_path = "/mnt/projects/RAS-CompChem/static/Mayukh/HSP83_for_Lorenzo/lookup_table_Closed.txt"
file_path  = sys.argv[1]
outfile = file_path[:-4] + "_converted.txt"

resi_dict = {}

with open(dict_path, 'r') as dictfile:
  for line in dictfile:
    linesplit = line.strip().split()
    key = "%s %s" %(linesplit[3], linesplit[4])
    value = "%s %s %s" %(linesplit[0], linesplit[1], linesplit[2])
    resi_dict[key] = value

with open(file_path, 'r') as infile:
  with open(outfile, 'w') as outfile:
    for line in infile:
      resid = line.strip()
      num_index = [i for i,c in enumerate(resid) if c.isdigit()]
      lookup_res = resid[:num_index[0]] + " " + resid[num_index[0]:]
      outfile.write(resi_dict[lookup_res] + "\n")
