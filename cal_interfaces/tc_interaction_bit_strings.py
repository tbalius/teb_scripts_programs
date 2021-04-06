
## This script was written in 2020 by Trent Balius at FNLCR

import os

lines = os.popen('ls  *_dimer_interface_protein/*.bits').readlines()
N = len(lines)

#ofh = open('tc_compare_one.txt','w')

for i in range(0,N):
    for j in range(i+1,N):
       file1 = lines[i].strip()
       file2 = lines[j].strip()
       print("file1=%s\nfile2=%s\n"%(file1,file2))
       os.system('python compare_interface.py %s %s tc_compare_two.txt'%(file1,file2)) 
#       ofh.write("file1=%s, file2=%s, tc=%f\n"%(file1,file2,tc))
#ofh.close()

