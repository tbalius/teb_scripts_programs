
import sys, os, math

# This script is written by Trent E Balius on 2023/05/26.  
# This will parrallel the matrix calculation for the per-residue energy calculation. 



# this is taken from py_amber_reader.py
def find_range(listv):
  # examples: 1-4,7-10,34-59
  list_split = listv.split(',')
  int_list = []

  for i in range(len(list_split)):
      interval = list_split[i].split('-')
      if (len(interval) == 1):
         tmp_int_list = []
         tmp_int_list.append(int(interval[0]))
      elif (len(interval) == 2):
         tmp_int_list = range(int(interval[0]),int(interval[1])+1)
      else:
        print ("error")
        sys.exit(0)
      for i in range(len(tmp_int_list)):
         int_list.append(tmp_int_list[i])
         #print (tmp_int_list[i])

  #for i in range(len(int_list)):
  #    int_list[i] = int_list[i] - 1

  return int_list


def make_subset( ori_list, numperss,  numss, remainder, list_of_subset_lists):

   # ori_list : the original list to sub divided amoung the subsets
   # numperss :  number of elements to be placed in each subset.  remainders will be distributed to the frist few subsets so some will have one additional entry. 
   # numss : this is the number of subsets. 
   # remainder : the number of entries to be distributed on top of numperss. 
   # list_of_subset_lists : this is the point to return subsets

   # list_of_subset_lists should be empty. 
   # we are passing a pointer.  
   if len(list_of_subset_lists) !=0: 
       print("Error. list_of_subset_lists should be empty...")
       exit()

   lenl = len(ori_list)

   # loop over the list and make subsets of lists
   count1 = 0 # number of subsets
   count2 = 0 # number of values in current subset
   subset_list = []
   for i in range(lenl):
       #print(i,count1,count2,remainder)
       if ( count2==0):
           if( count1 < remainder): # if staring new sublist and we are less than the reminder then add one more to the list.  
               cnumperss = numperss+1 # current number to go into sublist
           else:
               cnumperss = numperss 

       subset_list.append(ori_list[i])

       if ( count2 < cnumperss-1):
           count2 = count2+1
       else:
           count2=0 # reset counter of elements of subset. 
           count1=count1+1 # increment the list of subsets
           list_of_subset_lists.append(subset_list)
           subset_list = []

#  # for debugging 
#  print(len(list_of_subset_lists))
#  for i in range(len(list_of_subset_lists)):
#       print(i," ",len(list_of_subset_lists[i]))
#       for j in range(len(list_of_subset_lists[i])):
#           print(i," ",j," ",list_of_subset_lists[i][j])

def make_str(list1):
    txt = ''
    lenl = len(list1)
    count = 0
    for ele in list1:
        #print (ele)
        txt=txt+str(ele)
        if (count < lenl-1): # do not write a comma if it is the last element
           txt=txt+','
        count=count+1
    return txt
        

def submit_jobs(list1,list2,prm,crd):

    jobnum = 0

    current = cwd = os.getcwd()
    #for li in range(len(list1)):
    #    si = make_str(list1[li])
    for li in list1:
        si = make_str(li)
        for lj in list2:
            sj = make_str(lj)
            # write a shell script
            txt = ''
            txt = txt+'#!/bin/csh\n'
            txt = txt+'#SBATCH -t 120:00:00\n'
            txt = txt+'#SBATCH --partition=norm-oel8\n'
            txt = txt+('#SBATCH --output=stdout.%d\n'%jobnum)
            txt = txt+'\n'
            txt = txt+ 'set script = "/home/baliuste/zzz.github/teb_scripts_programs/py_amber_reader/"\n'
            txt = txt+ ('python ${script}/amber_reader_frame_by_frame.py %s %s "%s" "%s" rst_fp_%d justavg > rst_fp_%d.log\n'%(prm,crd,si,sj,jobnum,jobnum))
            jobnum = jobnum+1

            workdir = current+"/job_%05d"%jobnum
            os.mkdir(workdir)
            os.chdir(workdir)

            filename = 'submit_%05d.csh'%jobnum
            fh = open(filename,'w')
            fh.write(txt)
            fh.close()
            cmd = "sbatch "+filename
            os.system(cmd)
    os.chdir(current)
            
def main():
     
    num_per_subset = 10
    
    print ("syntax: python script mask1 mask2 parm7 mdcrd(in ascii or rst7 in ascii)") 
    print ("        example input:")
    print ("          mask1 = 1-640,1555")
    print ("          mask2 = 642-1281,1556")
    print ("          prm   = one.prm")
    print ("          crd   = one.rst")
    if (len(sys.argv) != 5): 
       print ("Error.  Wrong number of inputs.  this script requiers 4 inputs")
       exit()
   
    mask1 = sys.argv[1]
    mask2 = sys.argv[2]
    prm   = sys.argv[3]
    crd   = sys.argv[4]

    print("mask1 ="+mask1 )
    print("mask2 ="+mask2 )
    print("prm   ="+prm   )
    print("crd   ="+crd   )
    
    list1 = find_range(mask1)
    list2 = find_range(mask2)
    
    len1 = len(list1)
    len2 = len(list2)
    
    print("length 1 = %d"%len1)
    print("length 2 = %d"%len2)
    
    
    nsubsets1 = int(math.floor(len1/num_per_subset))
    nsubsets2 = int(math.floor(len2/num_per_subset))
    
    remainder1 = len1%num_per_subset
    remainder2 = len2%num_per_subset
    
    if remainder1 > 0: 
       print("set1: distributing remainder to the frist %d subset(s))"%remainder1)
       #njobs1 = njobs1+1
    
    if remainder2 > 0: 
       #njobs2 = njobs2+1
       print("set2: distributing remainder to the frist %d subset(s)"%remainder2)
    
    print("number of subsets 1 = %d"%nsubsets1)
    print("number of subsets 2 = %d"%nsubsets2)
    
    print("number of jobs = %d"%(nsubsets1*nsubsets2))
    
    
    # make the subsets: 
    
    list_of_subset_lists1 = []
    make_subset( list1, num_per_subset,  nsubsets1, remainder1, list_of_subset_lists1)
    
    list_of_subset_lists2 = []
    make_subset( list2, num_per_subset,  nsubsets2, remainder2, list_of_subset_lists2)
    
    submit_jobs(list_of_subset_lists1,list_of_subset_lists2,prm,crd)

main()

