
import sys
import os.path

## 2012/12
## Writen by Trent Balius in the Shoichet Group
## reads in DOCK output "OUTDOCK".
## in future, we may want to use the combined output file "combine.score".
## this script will create a csv file with all ligands with all receptors. 

#class dockdata:
#    def __init__(self, score, ligand_bind):
#        self.id    = int(id)
#        self.name  = name
#        self.score = float(score)

MIS_VAL = 100000.0


def read_OUTDOCK_file(file,score,dic,count):
     print file

     ## this funtion reads in the scores from the dock output
     file1 = open(file,'r')
     flag_read_data = False

     #score = []
     ## initialize vector 
     for i in range(len (dic)):
         score.append(MIS_VAL)

     for line in file1:

        splitline = line.split()

        if (len(splitline) == 0):
           #print splitline 
           #print line
           continue

        if (splitline[0] == "mol#"):
            flag_read_data = True

        if (splitline[0] == "EOF"):
            flag_read_data = False

        if (flag_read_data):
           #print line

           if (splitline[1] == "id_num"):
               continue

           if (splitline[0] != "E"):
               continue

           if not (splitline[1] in dic ):
              dic[splitline[1]] = count
              count             = count + 1
              score.append(float(splitline[7]))
           else: ## the name already exist in the dictionary, it already has a value stored on the list
              if (score[dic[splitline[1]]] > float(splitline[7])):
                  #print line + splitline[7]
                  score[dic[splitline[1]]] = float(splitline[7]) ## if the new score is more favorable then 
                                                                ## what is curently on the list replace it.
     file1.close()
     return score, dic, count

""" this we
def read_COMBINE_SCORE_file(file,dic,count):
     ## this funtion reads in the scores from the combined.score file
     file1 = open(file,'r')

     ## initialize vector 
     for i in range(len (dic)):
         score.append(MIS_VAL)

     for line in file1:

        splitline = line.split()

        if (len(splitline) == 0):
           continue

        if (len(splitline) == 1):
           ## this have an id but no scores. 
           continue

        if not (splitline[1] in dic ):
           dic[splitline[1]] = count
           count             = count + 1
           score.append(float(splitline[7]))
        else: ## the name already exist in the dictionary, it already has a value stored on the list
           if (score[dic[splitline[1]]] > float(splitline[7])):
               #print line + splitline[7]
               score[dic[splitline[1]]] = float(splitline[7]) ## if the new score is more favorable then 
                                                                ## what is curently on the list replace it.
     file1.close()
     return score, dic, count
"""


def process_files(inputvec,numvec, output):
  
   if sum(numvec) != len(inputvec):
      print "Error: number of files is inconsetant with numbers of files for each receptor specified" 
      exit()

   ## make dictionary for sets
   dic = {}
   all_score = []
   count = 0
   score = []

   count_nv      = 0
   num_next_rec  = numvec[0]  # acumuattion of numvec, kepts track of howmeny files before next receptor
#   flag_next_rec = False 
 
   for index,input in enumerate(inputvec):
      score, dic, count = read_OUTDOCK_file(input,score,dic,count)
     
      if (index == (num_next_rec-1)):
         print "index == (num_next_rec-1)"
         num_next_rec = num_next_rec + numvec[count_nv]
         count_nv = count_nv + 1
     
#      if (flag_next_rec): ## each recptor may have multiple dock OUT files assoiated with them 
         ## we will read in multipule input files 
         ## if input files for receptor 6 has a molicule that none of the files 1-5 have then the molecules is appended to 
         ## the dictionary and is placed at the end of the list.  Thus we will need to pad the ends of the other
         ## vectors with +100.0 (or some number) to indicate that this molecule was not scored.  
         if (len(all_score) > 0):
           if (len(all_score[0]) != len(score)):
               print "Adding zerros to the end of other score"
               for i in range(len(all_score)):
                   print i, len(all_score[i])
                   #count = len(all_score[i])
                   #while count < len(score):
                   while len(all_score[i]) < len(score):
                      all_score[i].append(MIS_VAL)
                      #count = count+1
               #sys.exit()
         all_score.append(score)
         score = []


   file2 = open(output + '.csv','w')
   namelist = dic.keys()
   for name in namelist:
       #file2.write( "%s,%d,%f\n" %( name, dic[name],  score[dic[name]]))
       file2.write( "%s,%d" %( name, dic[name]))
       for i in range(len(all_score)):
           file2.write( ",%f" %( all_score[i][dic[name]]))
       file2.write( "\n")
   file2.close()
 
   return 

def process_input_file(input):

    # inputfile formate:  
    # rec 1 has N files
    # path1
    # paht2
    # ...
    # pathN
    # ...
    # rec i has M files
    # path1
    # ...
    # path M

    inputfiles = []
    recname    = []
    numvec     = [] # list of integers
    count      = 0

    flagfirst = True

    file1 = open(input,'r')
    for line in file1:
        splitline = line.split()
        if (len(splitline) == 5):
           if (not flagfirst ): ## here we will check that the receptor has the right numbers of files
               if (count != numvec[len(numvec)-1]):
                   print "Error: counted files dose not macht the information line."
                   print count, numvec[len(numvec)-1], recname[len(recname)-1]
                   exit()
               count = 0
           else:
               flagfirst = False

           if not (splitline[0] == "rec" and splitline[2] == "has" and splitline[4] == "files"):
               print "name file is not formated correctly"
               print "line: rec 'Name' has 'Num' files"
               exit()
           recname.append(splitline[1])
           numvec.append(int(splitline[3]))
        elif (len(splitline) == 1):
           file = splitline[0]
           if (not os.path.exists(file)):
              print file + " does not exist."
              sys.exit()
           if (os.stat(file)[6]==0):
              print file + " is empty."
              sys.exit()
           inputfiles.append(file)
           count = count + 1
        else:
           print "Error: file has a blank line"

    if (count != numvec[len(numvec)-1]): ## check for the last one.
        print "Error: counted files dose not macht the information line."
        print count, numvec[len(numvec)-1], recname[len(recname)-1]
        exit()
    file1.close() 

    minvec = min(numvec)
    maxvec = max(numvec)
    if maxvec != minvec:
       print "Warrning: the number of files for each receptor ranges from %d to %d " % (minvec,maxvec)
    else:
       print "each receptor has %d files." % maxvec

    return inputfiles, numvec 


def main():
  if len(sys.argv) != 3 : # if no input
     print "python mkmat inputfile.txt output_prefix (csv file)"
     print "len(sys.argv)  = " + str( len(sys.argv))
     return 

  inputfile     = sys.argv[1]  
  output_prefix = sys.argv[2]
  #print inputvec,output_prefix
  inputfiles, numvec = process_input_file(inputfile)
  process_files(inputfiles,numvec,output_prefix)
main()

