
import sys, os, math
import mol2
#import sph_lib

# This is written by Trent Balius at FNLCR
# written in Nov, 2020
# modified form volume_cal_sph.py 

# make sure that the grid is big enough to accomidate all the mol2 files. 
def bounding_box_grid_file(mol2_vec,scale):

  # find extreme points. 
    # loop over atoms in mol2 atoms
    # mol2_vec is a list of mol2 entries. 
    
  max_x = max_y = max_z = -10000.0
  min_x = min_y = min_z =  10000.0

  buff = scale # add/substract a buffer to make sure spheres are completly contained

  for mol2 in mol2_vec: 
      for atom in mol2.atom_list:
       if (atom.X > max_x):
           max_x = atom.X+buff
       if (atom.X < min_x):
           min_x = atom.X-buff
       if (atom.Y > max_y):
           max_y = atom.Y+buff
       if (atom.Y < min_y):
           min_y = atom.Y-buff
       if (atom.Z > max_z):
           max_z = atom.Z+buff
       if (atom.Z < min_z):
          min_z = atom.Z-buff

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

# pre calc distances on a grid
def cal_grid(mol2,gridscale,xn,yn,zn,origin):
   # here the vector of values is transformed to a multidemitional array (grid)
    grid_old = []
    count = 0
    for i in range(xn):
        ydim = []
        for j in range(yn):
            zdem = []
            for k in range(zn):
                zdem.append(0)
                count = count + 1
            ydim.append(zdem)
        grid_old.append(ydim)
    
    for i in range(xn):
        x = (i * gridscale) + origin[0] 
        for j in range(yn):
            y = (j * gridscale) + origin[1] 
            for k in range(zn):
                z = (k * gridscale) + origin[2] 
                min_dist = 100000.0
                for atom in mol2.atom_list:
                    if (atom.type == 'H'): 
                        continue
                    dist = distance([x,y,z],[atom.X,atom.Y,atom.Z])
                    if dist < min_dist: 
                       min_dist = dist
                grid_old[i][j][k] = min_dist
    return grid_old


def cal_dist_closest_grid_point(grid,gridscale,xn,yn,zn,origin,atom):

        grid_i = int(round((atom.X - origin[0] ) / gridscale))
        grid_j = int(round((atom.Y - origin[1] ) / gridscale))
        grid_k = int(round((atom.Z - origin[2] ) / gridscale))

        dist = grid[grid_i][grid_j][grid_k]
        return dist

def cal_dist_tri_linear(grid,gridscale,xn,yn,zn,origin,atom):

        mod_x = (atom.X - origin[0] ) / gridscale
        mod_y = (atom.Y - origin[1] ) / gridscale
        mod_z = (atom.Z - origin[2] ) / gridscale

        grid_i = int(math.floor((atom.X - origin[0] ) / gridscale))
        grid_j = int(math.floor((atom.Y - origin[1] ) / gridscale))
        grid_k = int(math.floor((atom.Z - origin[2] ) / gridscale))

        diff_i = mod_x - float(grid_i)
        diff_j = mod_y - float(grid_j)
        diff_k = mod_z - float(grid_k)

        #dist = grid[grid_i][grid_j][grid_k]
        xgr = diff_i
        ygr = diff_j
        zgr = diff_k


        nx = grid_i
        ny = grid_j
        nz = grid_k

        a8 = grid[nx][ny][nz];
        a7 = grid[nx][ny][nz + 1] - a8
        a6 = grid[nx][ny + 1][nz] - a8;
        a5 = grid[nx + 1][ny][nz] - a8;
        a4 = grid[nx][ny + 1][nz + 1] - a8 - a7 - a6;
        a3 = grid[nx + 1][ny][nz + 1] - a8 - a7 - a5;
        a2 = grid[nx + 1][ny + 1][nz] - a8 - a6 - a5;
        a1 = grid[nx + 1][ny + 1][nz + 1] - a8 - a7 - a6 - a5 - a4 - a3 - a2;
    
        dist = a1 * xgr * ygr * zgr + a2 * xgr * ygr + a3 * xgr * zgr + a4 * ygr * zgr + a5 * xgr + a6 * ygr + a7 * zgr + a8;

        return dist


#def min_dist_mol2()


def main():


   if len(sys.argv) != 8: # if no input
       print ("ERORR:")
       print ("syntex: distance_cal_gird.py mol2_file(docked poses) mol2_file(find poses close to) scale threshold hname output yes_no")
       print ("scale dinfines the fines of the grid.")
       return
 

   infilemol2_poses     = sys.argv[1]
   infilemol2_ref       = sys.argv[2]
   scale                = float(sys.argv[3])
   dist_threshold       = float(sys.argv[4])
   hname                = sys.argv[5]
   outfile              = sys.argv[6]
   write_grid_yes_no    = sys.argv[7]

   print ("input file (poses)     = ", infilemol2_poses)
   print ("input file (reference) = ", infilemol2_ref)
   print ("scale =", scale)
   print ("threshold =", dist_threshold)
   print ("head_name =", hname)
   print ("outputprefix =", outfile)
   print ("write_grid_yes_no =", write_grid_yes_no)
   #mol2_vector  = mol2.read_Mol2_file(infilemol2_poses)
   mol2_vector  = mol2.read_Mol2_file_head(infilemol2_poses)
   mol2_ref  = mol2.read_Mol2_file(infilemol2_ref)[0]

   #close_mol2 = []
   #fho = open(outfile+'.mol2','w')


   #xn,yn,zn,dx,dy,dz,origin,values = read_in_dx_file(infiledx)
   xn,yn,zn,dx,dy,dz,origin,values = bounding_box_grid_file(mol2_vector,scale)
   gridscale = dx # assumes that they are all the same spaceing
   grid_dist = cal_grid(mol2_ref,gridscale,xn,yn,zn,origin)
   count = 0
   for mol in mol2_vector: 
       min_dist = 100000
       count_atom_lt_thes = 0
       for atom in mol.atom_list: 
           if (atom.type == 'H'): 
               continue
           #dist = cal_dist_closest_grid_point(grid_dist,gridscale,xn,yn,zn,origin,atom)
           dist = cal_dist_tri_linear(grid_dist,gridscale,xn,yn,zn,origin,atom)
           if dist < min_dist: 
              min_dist = dist
           if dist < dist_threshold: 
               count_atom_lt_thes = count_atom_lt_thes + 1   
       if min_dist < dist_threshold: 
          print("mol %d,dist=%f,num_atom_lt_threshold=%d"%(count,min_dist,count_atom_lt_thes))
          #close_mol2.append(mol)
          mol.header = mol.header+"##########  %s_dist:                    %f\n"%(hname,min_dist)
          mol.header = mol.header+"##########  %s_num_atom_lt_threshold:   %d\n"%(hname,count_atom_lt_thes)
          mol2.append_mol2(mol, outfile+'.mol2')
       count = count + 1
   
   #mol2.write_mol2(close_mol2, outfile+'.mol2')
   
   print (gridscale ,xn,yn,zn,dx,dy,dz,origin)

   #file1 = open(outfile+'vol_values.txt','w')
   #
   #count = 0
   #new_values = calc_volume(outfile,values,gridscale,xn,yn,zn,origin, sphs, file1, True)
   if (write_grid_yes_no[0] == "y"):
      print ("writting grid...")
      new_values = [] 
      for i in range(xn):
          for j in range(yn):
              for k in range(zn):
                  new_values.append(grid_dist[i][j][k])
      
      write_out_dx_file(outfile+".dx",xn,yn,zn,dx,dy,dz,origin,new_values)
   else: 
      print ("not writting grid...")
   #file1.close()
main()


