import sys
import pdb_lib

# Written by Trent E. Balius in the Shoichet Lab at UCSF

class cord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class frame:
    def __init__(self, cords):
        self.cords = cords ## list of coordenates 



def coord_reader(filename,size):

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
    exit
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


def main():

    if (len(sys.argv) != 4): # if no input
        print " (1) pdb file name,"
        print " (1) crd file name,"
        print " (2) output file  ";
        return

    pdbfilename    = sys.argv[1]
    crdfilename    = sys.argv[2]
    output         = sys.argv[3]

    #cl = pdb_lib.read_pdb(pdb_file)
    pdb = pdb_lib.read_pdb(pdbfilename)[0]
    size = len(pdb) 

    frames = coord_reader(crdfilename,size)

    j = 0
    for f in frames:
        i = 0
        for c in f.cords:
            print "j=",j,"i=",i 
            
            pdb[i].X = c.x
            pdb[i].Y = c.y
            pdb[i].Z = c.z
            i = i + 1
        pdb_lib.output_pdb(pdb,output+"."+str(j)+".pdb")
        j=j+1


    return;
#################################################################################################################
#################################################################################################################
main()
 


