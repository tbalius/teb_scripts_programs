import sys
#import pdb_lib

# Written by Trent E. Balius, 2021 at FNLCR. 
# created from other scripts writen at UCSF and Stony Brook 

class cord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class frame:
    def __init__(self, cords):
        self.cords = cords ## list of coordenates 



def coord_reader(filename):

 print "IN coord_reader"
 file = open(filename,'r')
# lines = file.readlines()

 frames = []
 cords  = []
 count  = 0
 line_count = 0
#size = -1

# frist read in numbers
 vals = []
 for line in file:
   if line_count == 0:
       line_count = line_count + 1
       continue
   if line_count == 1:
       print ("number of cordanates = %s \n",line)
       size = int(line.split()[0])
       line_count = line_count + 1
       continue
   data = line.split()
   if line_count > 0:
   #if line_count > 1:
     i = 0
     while i < len(data):
         vals.append(data[i])
         i=i+1
   line_count = line_count + 1
 file.close()

 print "read in coord file"
# now convet vals to frames 
#  for val in vals()
 if (len(vals)%3 != 0 ):
    print "error len(vals)%3 = %d"%(len(vals)%3)
    exit(0)
 i = 0
 while i < len(vals):
       if count == size:
          temp_frame = frame(cords)
          frames.append(temp_frame)
          print "# of Frames now:",len(frames)
          cords  = []
          count  = 0
       x = float(vals[i])
       y = float(vals[i+1])
       z = float(vals[i+2])
       temp_cord = cord(x,y,z)
       cords.append(temp_cord)
       i = i + 3
       count = count + 1
 temp_frame = frame(cords)
 frames.append(temp_frame)


 return frames

def coord_writer(filename,cords,name):

 print "OUT coord_writer"
 filec = open(filename,'w')
 filec.write('%s\n'%(name))
 filec.write('%7d\n'%(len(cords)))
# lines = file.readlines()
 for i,crd in enumerate(cords):
     filec.write('%12.7f%12.7f%12.7f'%(crd.x,crd.y,crd.z))
     if (((i+1) % 2) == 0):
         #print i
         filec.write('\n')
 if (((i+1) % 2) != 0):
     #print i
     filec.write('\n')
 filec.close()
# frist read in numbers


 return



def main():

    if (len(sys.argv) != 5): # if no input
        print " (1) crd file name,"
        print " (2) crd file name,"
        print " (3) output file  ";
        print " (4) val for mixing"
        return

    crdfilename1    = sys.argv[1]
    crdfilename2    = sys.argv[2]
    output          = sys.argv[3]
    val             = float(sys.argv[4])
    if (val >= 1.0): 
       print ("Error: val must be less than 1.0")
       exit()

    frames1 = coord_reader(crdfilename1)
    frames2 = coord_reader(crdfilename2)

    if (len(frames1) != len(frames2)): 
        print ("Error must be same number of frames. ")
        exit(0)

    for j in range(len(frames1)):
        f1 = frames1[j]
        f2 = frames2[j]

        if (len(f1.cords) != len(f2.cords)): 
            print ("Error must be same number of cords. ")
            exit(0)

        temp_cords = []
        for i in range(len(f1.cords)):
            print ("j=",j,"i=",i)
            
            x = (val)*f1.cords[i].x + (1-val)*f2.cords[i].x
            y = (val)*f1.cords[i].y + (1-val)*f2.cords[i].y
            z = (val)*f1.cords[i].z + (1-val)*f2.cords[i].z
            temp_cord = cord(x,y,z)
            temp_cords.append(temp_cord)

        coord_writer(output+"."+str(j)+".rst7",temp_cords,output+"."+str(j))


    return;
#################################################################################################################
#################################################################################################################
main()
 


