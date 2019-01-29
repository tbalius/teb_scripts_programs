import sys,  gzip

## Writen by Trent Balius in the Shoichet Group (modifed from code from the rizzo group)


def average(vec):
    sum = 0
    count = 0 
    for ele in vec:
        sum = sum + ele
        count = count + 1
    return (sum/count)
    


def make_translate_duplicated(filein,fileout):

    #file1 = gzip.open(filein,'r')
    file1 = open(filein,'r')
    lines = file1.readlines()
    file1.close()
  
    file2 = open(fileout,'w')

    new_lines = []
    x = []
    y = []
    z = []

    for line in lines:
         linesplit = line.split() #split on white space  
         if linesplit[0] == "REMARK":
             file2.write(line)
         elif linesplit[0] == "ATOM" or linesplit[0] == "HETATM":
             #print line[71:73] +" " + ele
             new_lines.append(line)
             xt = float(line[30:38])
             yt = float(line[38:46])
             zt = float(line[46:54])
             x.append(xt)
             y.append(yt)
             z.append(zt)
             #file2.write(line[0:54]+'  1.00  0.00           '+ ele +'\n')
         #elif linesplit[0] == "TER":
         #    file2.write('END\n')
         #elif linesplit[0] == "END":
         #    file2.write('END\n')

    centrod_x = average(x)
    centrod_y = average(y)
    centrod_z = average(z)
    print centrod_x, centrod_y, centrod_z
    for line in new_lines:
          #line = strip(line)
          # we want the invariant to be when all the waters are out of the binding sight.
          # so we make the translated water have conformation A.
          line = line[0:16] + 'A' + line[17:len(line)]
          xt = float(line[30:38])
          yt = float(line[38:46])
          zt = float(line[46:54])
          file2.write('%s  %7.3f %7.3f %7.3f %s' % (line[0:29],(xt+100.0),(yt+100.0),(zt+100.0),line[55:len(line)]))
          #file2.write(line+'\n')
          # the old position when the waters are in the sight have conforation B. 
          line = line[0:16] + 'B' + line[17:len(line)]
          file2.write(line)
          #line[16] = 'B'

    file2.close()
    return

def main():
  if len(sys.argv) != 3: # if no input
     print "ERORR"
     return
  filein = sys.argv[1]
  fileout = sys.argv[2]
  make_translate_duplicated(filein,fileout)
main()


