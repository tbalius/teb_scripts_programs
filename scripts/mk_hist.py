

import sys,math

filename = sys.argv[1]

fh = open(filename, 'r')

bin_tc = []

N = 50

tc_min = 0.0
tc_max = 1.0
tc_range = tc_max -tc_min

bin_val = []

tc_inc = (tc_max -tc_min) / N 
 
val = tc_inc / 2.0
for i in range(0,N):
   bin_tc.append(0)
   bin_val.append(val)
   val = val+tc_inc

count = 0
for line in fh: 
    tc = float(line.strip())
    i = int(math.floor((tc-tc_min)*((N-1)/tc_range)))
    bin_tc[i] = bin_tc[i] + 1
    if (count % 1000000) == 0:  
        print count
    count=count+1
print " "

for i in range(0,N):
    print i, bin_val[i], bin_tc[i]

