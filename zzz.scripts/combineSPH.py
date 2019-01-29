import sys,  copy, math 

## Writen by Trent Balius in the Shoichet Lab, 04/21/2015
## combine spheres. 

## Sphgen expects the Fortran format:

## A3, I5, X, A4, X, 2F8.3, F9.3, X, A3, 7X, 3F7.3
## FORMAT: (I5, 3F10.5, F8.3, I5, I2, I3) 

class sphs:
    def __init__(self,header,sph_list):
        self.header      = header
        self.sph_list    = sph_list

class sph:
    def __init__(self,X,Y,Z,R,color,cluster):
        self.X = float(X)
        self.Y = float(Y)
        self.Z = float(Z)
        self.R = float(R) # radius
        self.color = color
        self.cluster = cluster

def print_sph(sph): 
    print sph.X,sph.Y,sph.Z,sph.R,sph.color,sph.cluster

def read_sph(filename):
   
    insph = open(filename,'r')

    head = ''
    headflag = True

    sphlist = []

    for line in insph: 
        if (headflag):
           head = head + line 
        else: 
           #print line
           if len(line) < 50: 
              print "line is not long enough . . . "
              exit()
           number1 = int(line[0:5]) # number of the atom with which surface point i (used to generate the sphere) is associated.
           X = float(line[6:16])
           Y = float(line[16:26])
           Z = float(line[26:36])
           R = float(line[36:44])
           number2 = int(line[44:49]) # number of the atom with which surface point j (second point used to generate the sphere) is associated
           if (len(line) == 55):
             cluster = int(line[49:51]) # this is the critical cluster
             color   = int(line[51:54])
           else:
             cluster = 0
             color   = 0
           temp_sph = sph(X,Y,Z,R,color,cluster)
           #print_sph(temp_sph)
           sphlist.append(temp_sph) 
           

        if ("cluster" in line): 
            if (not headflag):
                print "contains mutiple cluster" 
                exit()
            headflag = False
        

    spheres = sphs(head,sphlist) 
    return spheres

# this function calculates the distance between two spheres
def dist_sph(sph1,sph2):
    #print sph1.X,sph1.Y,sph1.Z
    #print sph2.X,sph2.Y,sph2.Z
    dist = math.sqrt(
           (sph1.X-sph2.X)**2.0 + 
           (sph1.Y-sph2.Y)**2.0 + 
           (sph1.Z-sph2.Z)**2.0
           )
    #print dist
    return dist

def combine_sph(sphs1,sphs2,threshold):
    sphs3 = copy.deepcopy(sphs1)

    #for i in range(len(sphs3.sph_list)): 
    #    sphs3.sph_list[i].cluster = 1 # in future we might want to change the cluster number 
    #threshold = 0.2
    for sph2 in sphs2.sph_list:
        goodSPHflag = True
        for sph1 in sphs3.sph_list: 
            if (dist_sph(sph1,sph2)<threshold): 
                goodSPHflag = False
                break
        if (goodSPHflag): 
            sphs3.sph_list.append(sph2)
    return sphs3

def write_sph(filename,spheres):
    outsph = open(filename,'w')
    print len(spheres.sph_list)
    outsph.write("DOCK spheres generated from combining sheres\n")
    outsph.write("cluster     1   number of spheres in cluster %5d\n" % len(spheres.sph_list))
    for i in range(len(spheres.sph_list)): 
	#outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d                                \n" % 
	outsph.write("%5d%10.5f%10.5f%10.5f%8.3f%5d%2d%3d\n" % 
                     (i+1,round(spheres.sph_list[i].X,3),
                          round(spheres.sph_list[i].Y,3),
                          round(spheres.sph_list[i].Z,3),
                          round(spheres.sph_list[i].R,3),i+1,
                          spheres.sph_list[i].cluster,
                          spheres.sph_list[i].color))
    outsph.close()
    return

def main():
  if len(sys.argv) != 5: # if no input
     print "ERORR"
     return
  namesph1 = sys.argv[1]
  namesph2 = sys.argv[2]
  namesphout = sys.argv[3]
  threshold = float(sys.argv[4])
  print " input: " + namesph1 + ", " + namesph2 + "\n output: " + namesphout #+ "\n\n"
  print " Threshold = " + str(threshold) + "\n\n"
  sphs1 = read_sph(namesph1)
  sphs2 = read_sph(namesph2)
  sphs3 = combine_sph(sphs1,sphs2,threshold)
  write_sph(namesphout,sphs3)
main()


