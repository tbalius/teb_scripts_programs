import struct
import sys
import array

# written by Reed Stien
# Modified by Trent Balius (2019/12/10)


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
        #fileh.write('origin %6.2f %6.2f %6.2f\n' % (origin[0],origin[1],origin[2]))
        fileh.write('origin %7.4f %7.4f %7.4f\n' % (origin[0],origin[1],origin[2]))
        fileh.write('delta %6.6f 0 0\n' % dx)
        fileh.write('delta 0 %6.6f 0\n' % dy)
        fileh.write('delta 0 0 %6.6f\n' % dz)
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


#def readef read_bump(bump_file):
#
#     bump_open = open(bump_file,'r')
#     bump_read = bump_open.readlines()
#     bump_open.close()
#
#     x_coords = []
#     y_coords = []
#     z_coords = []
#
#     for line in bump_read[0:2]:
#             #print(line)
#             line = line.strip().split()
#             spacing = '0.200'
#             if line[0] == spacing:
#                     print(line)
#                     box_corner_x = float(line[1])
#                     box_corner_y = float(line[2])
#                     box_corner_z = float(line[3])
#                     x_dim = int(line[4])
#                     y_dim = int(line[5])
#                     z_dim = int(line[6])
#
#    return(x_dim, y_dim, z_dim, [box_corner_x, box_corner_y, box_corner_z])

def construct_box(dx_file_name, origin, spacing, xn, yn, zn, values):

        matrix = []
        for x in range(xn):
               y_list = []
               for y in range(yn):
                       z_list = []
                       for z in range(zn):
                               z_list.append(0)
                       y_list.append(z_list)
               matrix.append(y_list)

        index = 0
        for k in range(zn):
                for j in range(yn):
                        for i in range(xn):
                                matrix[i][j][k] = values[index]
                                index += 1

	write_out_list = []
	for i in range(xn):
		for j in range(yn):
			for k in range(zn):
				write_out_list.append(matrix[i][j][k])

        dx = spacing
        dy = spacing
        dz = spacing
        write_out_dx_file(dx_file_name,xn,yn,zn,dx,dy,dz,origin,write_out_list)

def read_bump(bump_file):

	bump_open = open(bump_file,'r')
	bump_read = bump_open.readlines()
	bump_open.close()

	x_coords = []
	y_coords = []
	z_coords = []

	for line in bump_read[0:2]:
		line = line.strip().split()
		spacing = '0.200' 
		if line[0] == spacing:
			print(line)
			box_corner_x = float(line[1])
			box_corner_y = float(line[2])
			box_corner_z = float(line[3])
			x_dim = int(line[4])
			y_dim = int(line[5])
			z_dim = int(line[6])

	x_coords = [box_corner_x]
        y_coords = [box_corner_y]
        z_coords = [box_corner_z]

	bump_string = ''	

	for line in bump_read[2:]:
		line = line.strip()
		bump_string+=line

	spacing = float(0.200) 
	for i in range(x_dim-1):
                new_val = box_corner_x+spacing
                x_coords.append(new_val)
                box_corner_x = new_val

        for i in range(y_dim-1):
                new_val = box_corner_y+spacing
                y_coords.append(new_val)
                box_corner_y = new_val

        for i in range(z_dim-1):
                new_val = box_corner_z+spacing
                z_coords.append(new_val)
                box_corner_z = new_val


	values = []	
	count = 0 
	for z in z_coords:
                for y in y_coords:
                        for x in x_coords:
				if bump_string[count] == "F":
					values.append(float(1))
				else:
					values.append(float(0))
				count += 1

	return(values, [x_dim, y_dim, z_dim], [x_coords[0], y_coords[0], z_coords[0]])
	

def main():

        
        if (len(sys.argv) != 3):
           print "Error. this script takes 2 arguments: grid filename prefix (eg. vdw) and dx filename prefix (eg. vdw_energies). "
           exit()

        inputprefix = sys.argv[1]
        outputprefix = sys.argv[2]

        vdw_file = inputprefix + '.vdw' #"vdw.vdw"
	values, dims, origin = read_bump( inputprefix + ".bmp")

	x_dim = dims[0]
	y_dim = dims[1]
	z_dim = dims[2]

	spacing = 0.200
        vdwFile = open(vdw_file, 'rb')  # b is for binary, r is for read

        # skip the frist number, marked open? 

        for i in range(0,1):
         tempArray = array.array('f') 
         tempArray.fromfile(vdwFile,1)
         tempArray.byteswap()
         print (i, tempArray)

        tempArray = array.array('f')
        tempArray.fromfile(vdwFile, x_dim * y_dim * z_dim)
        tempArray.byteswap()

	construct_box( outputprefix + "_repulsive.dx", origin, spacing, x_dim, y_dim, z_dim, tempArray)

        # skip 2 points , marked close then open ?
        for i in range(0,2):
         tempArray = array.array('f') 
         tempArray.fromfile(vdwFile,1)
         tempArray.byteswap()
         print (i, tempArray)

        tempArray = array.array('f')
        tempArray.fromfile(vdwFile, x_dim * y_dim * z_dim)
        tempArray.byteswap()
	construct_box(outputprefix + "_attractive.dx", origin, spacing, x_dim, y_dim, z_dim, tempArray)

	construct_box( outputprefix +"_bmp.dx", origin, spacing, x_dim, y_dim, z_dim, values)

        print (x_dim, y_dim, z_dim,  x_dim * y_dim * z_dim )

        # there is one point left, marked close? 
        for i in range(0,1): 
         tempArray = array.array('f') 
         tempArray.fromfile(vdwFile,1)
         tempArray.byteswap()
         print (i, tempArray)

main()
