
import sys, os, math
import mol2
import sph_lib

# This is written by Trent Balius in the Shoichet Lab, UCSF
# written in Dec, 2016
#


def bounding_box_grid_file(sphs,scale):

  # find extreme points. 
    # loop over spheres
  max_x = max_y = max_z = 0.0
  min_x = min_y = min_z = 10000.0

  buff = scale # add/substract a buffer to make sure spheres are completly contained

  for sph in sphs:
      # add/subtract radius.
      if (sph.X+sph.radius > max_x):
          max_x = sph.X+sph.radius+buff
      if (sph.X-sph.radius < min_x):
          min_x = sph.X-sph.radius-buff
      if (sph.Y+sph.radius > max_y):
          max_y = sph.Y+sph.radius+buff
      if (sph.Y-sph.radius < min_y):
          min_y = sph.Y-sph.radius-buff
      if (sph.Z+sph.radius > max_z):
          max_z = sph.Z+sph.radius+buff
      if (sph.Z-sph.radius < min_z):
          min_z = sph.Z-sph.radius-buff

  print "max corner = ", max_x, max_y, max_z 
  print "min corner = ", min_x, min_y, min_z 

  # define bounding box. these are the values the a dx file needs
  dif_x = max_x - min_x
  dif_y = max_y - min_y
  dif_z = max_z - min_z
  xn = int(math.ceil(dif_x / scale)) # lenth in x
  yn = int(math.ceil(dif_y / scale)) # lenth in y
  zn = int(math.ceil(dif_z / scale)) # lenth in z

  dx = scale   
  dz = scale   
  dy = scale   

  origin = [min_x, min_y, min_z]
  # generate grid.
  values = []
  for i in range(xn*yn*zn):
      values.append(0.0)


  return xn,yn,zn,dx,dy,dz,origin,values 

def write_out_dx_file(file,xn,yn,zn,dx,dy,dz,origin,values):

   
  fileh = open(file,'w')
#object 1 class gridpositions counts 40 40 40
#origin 35.31 27.576 18.265
#delta 0.5 0 0
#delta 0 0.5 0
#delta 0 0 0.5
#object 2 class gridconnections counts 40 40 40
#object 3 class array type float rank 0 items 64000 data follows

  fileh.write('object 1 class gridpositions counts %d %d %d\n' % (xn,yn,zn))
  fileh.write('origin %6.3f %6.3f %6.3f\n' % (origin[0],origin[1],origin[2]))
  fileh.write('delta %6.3f 0 0\n' % dx)
  fileh.write('delta 0 %6.3f 0\n' % dy)
  fileh.write('delta 0 0 %6.3f\n' % dz)
  fileh.write('object 2 class gridconnections counts %d %d %d\n' % (xn,yn,zn))
  fileh.write('object 3 class array type float rank 0 items %d data follows\n' % len(values))

  count = 1
  for value in values:
       if (value == 0.0): 
          fileh.write('%d' % 0)
       else:
          fileh.write('%f' % value)
       # print newline after 3rd number.
       if (count == 3): 
            fileh.write('\n')
            count = 0
       # print space after number but not at the end of the line.
       else:
            fileh.write(' ')
       count = count + 1

  # if the last line has less than 3 numbers then print the a newline.
  if (count < 3):
       fileh.write('\n')
  fileh.close()


def distance(v1,v2):
    if (len(v1)!=len(v2)):
       print "error" 
       exit()
    dist = 0.0
    for i in range(len(v1)):
        dist = dist + (v1[i]-v2[i])**2.0
    dist = math.sqrt(dist)
    return dist

def cal_grid(values,gridscale,xn,yn,zn,origin):
   # here the vector of values is transformed to a multidemitional array (grid)
    grid_old = []
    count = 0
    for i in range(xn):
        ydim = []
        for j in range(yn):
            zdem = []
            for k in range(zn):
                zdem.append(values[count])
                count = count + 1
            ydim.append(zdem)
        grid_old.append(ydim)
    return grid_old


######################################################################
# this function calculates volume of a set of spheres. 
######################################################################

def calc_volume(fileprefix,values,gridscale,xn,yn,zn,origin,sphs,fileh,return_vals):
# file - log file
# values gist values 
# gridscale - the grid spacing


    # loop over each sphere. 

    dict_gridpoint = {} # for each grid point have a list of atoms it is in

    
    sum_per_atom = []
    for atom_i,atom in enumerate(sphs):
        sum_per_atom.append(0.0)

        radius = atom.radius
        #print atom.type, atom.X, atom.Y, atom.Z, atom.type, dt[atom_i], radius

        grid_i = round((atom.X - origin[0] ) / gridscale)
        grid_j = round((atom.Y - origin[1] ) / gridscale)
        grid_k = round((atom.Z - origin[2] ) / gridscale)

        if (grid_i<0.0 or grid_j<0.0 or grid_k<0.0):
           print "ERROR. . . "
           exit()

        radius_gridpoint = math.ceil(radius / gridscale) + 1
        #print radius, gridscale, radius_gridpoint
        #print  grid_i,grid_j, grid_k

        start_i = max([(grid_i - radius_gridpoint),0.0])
        stop_i  = min([(grid_i + radius_gridpoint),xn])
        start_j = max([(grid_j - radius_gridpoint),0.0])
        stop_j  = min([(grid_j + radius_gridpoint),yn])
        start_k = max([(grid_k - radius_gridpoint),0.0])
        stop_k  = min([(grid_k + radius_gridpoint),zn])

        for i in range(int(start_i),int(stop_i)): # looping over the cube about the center of the atom 
            x = (i * gridscale) + origin[0] 
            for j in range(int(start_j),int(stop_j)):
                y = (j * gridscale) + origin[1] 
                for k in range(int(start_k),int(stop_k)):
                    z = (k * gridscale) + origin[2] 
                    dist = distance([x,y,z],[atom.X,atom.Y,atom.Z])
                    if (dist <= radius):
                        count = i*(yn*zn)+j*(zn) + k
                        if not (count in dict_gridpoint):
                           dict_gridpoint[count] = [atom_i]
                        else:
                           dict_gridpoint[count].append(atom_i)

    molN = len(dict_gridpoint.keys())
    boxN = len(values)
    boxV = xn*gridscale*yn*gridscale*zn*gridscale

    molV = float(molN)/float(boxN)*boxV

    print "molN=",molN,"  boxN=",boxN,"  boxV=",boxV
    print "molV=",molV
    
    fileh.write('%s,%f\n'%("molN",molN))
    fileh.write('%s,%f\n'%("boxN",boxN))
    fileh.write('%s,%f\n'%("boxV",boxV))
    fileh.write('%s,%f\n'%("molV",molV))


    new_values = []
    # make a new grid with only the voxels in the ligand are non-zerro

    if (return_vals):
        new_values = []
        #for i,val in enumerate(values):
        for i in range(len(values)):
            #print i 
            #if i in dict_gridpoint.keys():
            if i in dict_gridpoint:
               new_values.append(1.0)
            else:
               new_values.append(0.0)

    return new_values

def main():


   if len(sys.argv) != 4: # if no input
       print "ERORR:"
       print "syntex: volumn_cal.py sphere_file scale outputprefix"
       print "sphere file that defines the binding site (low dielectric sphere recomended) "
       print "scale dinfines the fines of the grid."
       return
 

   infilesph     = sys.argv[1]
   scale         = float(sys.argv[2])
   outfile       = sys.argv[3]

   print "input file = ", infilesph
   print "scale =", scale
   print "outputprefix =", outfile
   sphs  = sph_lib.read_sph(infilesph,'A','A')

   #xn,yn,zn,dx,dy,dz,origin,values = read_in_dx_file(infiledx)
   xn,yn,zn,dx,dy,dz,origin,values = bounding_box_grid_file(sphs,scale)

   gridscale = dx # assumes that they are all the same spaceing
   
   print gridscale ,xn,yn,zn,dx,dy,dz,origin   

   file1 = open(outfile+'gist_values.txt','w')

   count = 0
   new_values = calc_volume(outfile,values,gridscale,xn,yn,zn,origin, sphs, file1, True)
   write_out_dx_file(outfile +str(count) +"new_gist.dx",xn,yn,zn,dx,dy,dz,origin,new_values)
   file1.close()
main()


