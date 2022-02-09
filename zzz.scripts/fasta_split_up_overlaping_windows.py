
# written by Trent Balius
# 2022/01/12

# this script reads in a fasta file and will split it up into overlaping subfiles
# it uses a window size and a window offset to construct these overlaping windows.

import sys


def main():
   if len(sys.argv) != 4: 
      print "Error. not the right number of arguments."
      print "inputs: fasta file name, window size, window offset"
      exit()
   
   
   filename = sys.argv[1]
   window_size   = int(sys.argv[2])
   window_offset = int(sys.argv[3])

   print("filename = %s\nwindow_size=%i\nwindow_offset=%i\n"%(filename,window_size,window_offset))

   if (window_size < window_offset): 
       print "window_size must be bigger than window_offset. "
       exit()

   # make a new file name with out fasta at the end.   
   filename_prefix = ''

   filename_splitstring = filename.split('.')

   if (filename_splitstring[-1] == "fasta"):
       filename_prefix = filename_splitstring[0]
       for i in range(1,len(filename_splitstring)-1): # put everything in prefix seperated by "." exept the last (which is 'fasta')
           filename_prefix = filename_prefix +'.'+filename_splitstring[i]
   else:  
       print("file dose not end in 'fasta'.")
       filename_prefix = filename 
       exit()
   print ("prefix = %s\n"%filename_prefix) 
   
   fh = open(filename,'r')
   
   
   arr  = ''
   count = 0 
   for line in fh: 
       count=count+1
       print(line)
       if (count == 1): 
           name = line.strip()
           continue
       arr = '%s%s'%(arr,line.strip())
   print arr
   print len(arr)
   for i in range(0,len(arr)):
        print(arr[i])
   fh.close()
   #exit()
   
   #fh2 = open(fastafilename+'full','w')
   
   #fh2.write(name+"\n")
   #fh2.write(resabbstr+'\n')
   #fh2.close()

   #window_size = 1000
   #window_offset = 200

   
   start = 0
   end = start + window_size   

   count = 1
   while end <= len(arr):  
      fastafilename = "%s.%03i.%04i-%04i.fasta"%(filename_prefix,count,start,end)
      fh3 = open(fastafilename,'w')
      fh3.write('%s%s'%(name,'\n'))
      count2 = 0
      for i in range(start,end):
          if count2 == 60: 
             fh3.write('\n')
             count2=0
          fh3.write(arr[i])
          count2=count2+1
      fh3.close()
      start = start + window_offset
      end = start + window_size
      if end > len(arr) and end < len(arr)+window_offset: # we want to get the window upto the end. 
         end = len(arr)
      count=count+1

main()   
