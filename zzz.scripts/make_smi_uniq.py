

# Writte by Trent Balius, FNLCR, April 6, 2021

import sys 

def main():
   file1 = sys.argv[1]
   file2 = sys.argv[2]
   
   print("input = %s"%(file1))
   print("output = %s"%(file2))
   
   fh1 = open(file1,'r')
   
   dic_id_count = {}
   dic_id_line = {}
   
   
   
   for line in fh1:
       sline = line.split()
       sid = sline[1]
       if sid in dic_id_count:
          dic_id_count[sid]=dic_id_count[sid]+1
       else: 
          dic_id_count[sid]=1
          dic_id_line[sid] = line.strip()
       
   
   fh1.close()
   
   fh2 = open(file2,'w')
   for key in sorted(dic_id_line.keys()):
       fh2.write('%s\n'%(dic_id_line[key]))
   fh2.close()
   
   # print the ids that have more than on entree in the file. 
   
   for key in sorted(dic_id_count.keys()):
       if dic_id_count[key] > 1: 
          print(key,dic_id_count[key])
   
main()
