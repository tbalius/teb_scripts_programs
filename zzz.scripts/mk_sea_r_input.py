
import sys

## 2012/12
## Writen by Trent Balius in the Shoichet Group
## Reads in SEA output, processes it, and writes input for R to make network plot.

def print_matrix(filehandle,matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if len(matrix) != len(matrix[i]):
               print "Error: len(matrix) != len(matrix[i])"
               exit()
            if (j == 0): 
                filehandle.write('%e' % matrix[i][j])
            else:
                filehandle.write(',%e' % matrix[i][j])
        filehandle.write('\n')

def process_file(input,inputlabel,output_prefix,threshold):
  
   file1 = open(input,'r')
   file2 = open(inputlabel,'r')
   file3 = open(output_prefix+'.csv','w')
   file4 = open(output_prefix+'_forR.txt','w')
   file5 = open(output_prefix+'_matrix.txt','w')
   file6 = open(output_prefix+'_labels.txt','w')

   ## make dictionary for sets
   dic = {}
   count = 0
   for line in file2:
       if (count == 0):  ## then is the header.
          count = count + 1
          continue
       splitline = line.split(',')
       if not (splitline[0] in dic ):
           dic[splitline[0]] = count
           count = count + 1
   file2.close()
   print dic

   m = count - 1  ## number of entrees

   matrix = []
   for i in range(m):
       row = []
       for j in range(m):
           row.append(1.0)
       matrix.append(row)
   


   count = 0
   for line in file1:
       if (count == 0):  ## then is the header.
          count = count + 1
          continue
       splitline = line.split(',')
       if not (splitline[0] in dic ) or not (splitline[1] in dic ):
          print "Error: discrencies between " + input + " and " + inputlabel + "."

       val = float(splitline[2])
       id1 = dic[splitline[0]]
       id2 = dic[splitline[1]]

       
       file3.write("%d,%d,%e\n" % (id1, id2, val) )

       #if (val < threshold and id1 != id2):
       if (val < threshold and id1 > id2): ## only write the edge onces
          #file4.write("%d %d\n" % (id1, id2) )
          file4.write("%d %d %e\n" % (id1, id2, val) )
       if (val < threshold): 
          matrix[id1-1][id2-1] = val
   file4.close()
   file3.close()

   print_matrix(file5,matrix)
   file5.close()

   # intialize the list
   list_for_dic = []
   for i in range(len(dic.keys())):
       list_for_dic.append('')
   
   # populate the list
   for name in dic.keys():
       list_for_dic[dic[name]-1] =  ('%d,%s\n' % (dic[name],name))
       #list_for_dic[dic[name]] =  str(dic[name]) + name + '\n'

   # write the list to a file
   for i in range(len(dic.keys())):
       file6.write(list_for_dic[i])

   file6.close() 

   return 

def main():
  if len(sys.argv) != 5: # if no input
     print "python mk_sea_r_input.py sea_output.scores.csv sea_output.sets.csv temp -10.0 "
     print "10^-10 will be the threshold"
     return

  inputdata     = sys.argv[1]
  inputlabel    = sys.argv[2]
  output_prefix = sys.argv[3]
  threshold     = 10.0**float(sys.argv[4])
  print "threshold = %e" % (threshold)
  process_file(inputdata,inputlabel,output_prefix,threshold)
 
main()

