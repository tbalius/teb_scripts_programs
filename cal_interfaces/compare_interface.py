import sys


## This script was written (started) on Aug 3, 2020 by Trent Balius at FNLCR
## this script compare dimer interfaces for the same protein 
## it attemps to quantify if the same resdiues are interacting 
## We are using the TC coef.  

def read_bits(filename):

    fh = open(filename,'r')

    boolarray = []
    numdict = {}
    maxn = 0
    minn = 10000
    for line in fh: 
       splitline = line.split()
       num = int(splitline[0])
       boolv = int(splitline[1])
       if num > maxn: 
          maxn = num
       if num < minn: 
          minn = num

       boolarray.append(boolv)
       if (boolv == 1):
           #print(boolv)
           numdict[num] = 0
    #exit()
    fh.close()
    return boolarray, numdict, maxn, minn

def main():
   file1 = sys.argv[1]
   file2 = sys.argv[2]
   ofilename = sys.argv[3]
   print(file1)
   print(file2)

   ba1, na1, maxn, minn = read_bits(file1)
   print (maxn, minn);

   ba2, na2, maxn2, minn2 = read_bits(file2)
#   print (maxn2, minn2);
#   print(na1.keys())
#   print(na2.keys())

   overlap1 = 0 
   # make bit strings
   for key in na2.keys(): 
       if key in na1:
          overlap1 = overlap1 + 1

   overlap2 = 0 
   for key in na1.keys(): 
       #print(key)
       if key in na2:
          overlap2 = overlap2 + 1
          #print("I am here.")
       #exit()

   print(overlap1,overlap2)

   union = len(na1.keys()) + len(na2.keys()) - overlap1
   intersection = overlap1

   if union != 0:
      tc = intersection / union 
   else: #if union == 0
      tc = -0.0

   print("U=%d,I=%d,Tc=%8.4f\n"%(union, intersection, tc))

   fh = open(ofilename,'a')
   fh.write("%s-%s,%8.4f\n"%(file1,file2,tc))
   fh.close()

main()
