import sys
import copy
import math

def read_MD_rst7(filename,outputname):

    fileh = open(filename,'r')


    result_flag = False    
    count  = 0
    # read in values lines
    count = 0
    countVal = 0
    numatoms = 0
    time     = 0
    values = []
    for line in fileh:
       if count == 0: # frist line is a comment 
          print line
       elif count == 1: # second line contain one or two values is the number of atoms in the system and my have time float
          sl = line.split()
          if len(sl) > 2: 
             print "error"
             exit()
          
          numatoms = int(sl[0])
          if len(sl) == 2:
             time = float(sl[1])
             print time
       else: 
          sl = line.split()
          for ele in sl: 
              values.append(float(ele))
              countVal = countVal+1
       count = count+1

    print "numatoms = %d\nnumber of lines in file = %d\nnumber of values (may inclued volosities in addition to coords  in file = %d\n number of values /3 = %d\n" %(numatoms, count, countVal, countVal/3)

    # the last 6 values are the 3 box dimensions (X, Y, and Z side lengths) and the angles (XY, XZ, YZ)

    # find the min and max valuses
    xyzMax=[0,0,0]
    xyzMin=[100000,100000,100000]
    xyzStr = ["X","Y","Z"]
    counti = 0
    #for i in range(0, countVal-6):
    for i in range(0, (numatoms*3)):
        if counti == 3: # here we go in sets of 3. X -> 0, Y -> 1, Z -> 2 
           counti = 0
        #if counti == 0: 
        #   print i, values[i]
        if values[i] > xyzMax[counti]:
           xyzMax[counti] = values[i]
        if values[i] < xyzMin[counti]: 
           xyzMin[counti] = values[i]
        counti=counti+1

    print values[(numatoms*3)]

    pad = 0.0 # pad by some value like the diameter  of water on both sides (1.4 * 2 *2 = 5.6)
    for i in range(3):   
        print xyzStr[i]+"min&max = [",xyzMin[i],",",xyzMax[i],"]"
    diffX = xyzMax[0] - xyzMin[0] + pad
    diffY = xyzMax[1] - xyzMin[1] + pad
    diffZ = xyzMax[2] - xyzMin[2] + pad

    print "new dim = ", diffX, diffY, diffZ
    print "old dim = ", values[countVal-6] , values[countVal-5], values[countVal-4]

    fileh.close()
    return 

def main():

    if len(sys.argv) != 3:
      print "error:  this program takes 2 inputs:"
      print "   (1) filename of existing rst7 "
      print "   (2) filename for new rst7 output"
      exit()

    infilename  = sys.argv[1]
    outfilename = sys.argv[2]

    # read in file with a list of mdout files.
    print "input file:  " + infilename
    print "output file: " + outfilename
    read_MD_rst7(infilename,outfilename)

main()


