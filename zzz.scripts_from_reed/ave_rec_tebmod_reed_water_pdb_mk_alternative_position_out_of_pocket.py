import os, sys
import numpy as np
import scipy 
from scipy import stats
from numpy import linalg as la

### originally written by Tbalius@aol.com, edited by SteinStein


def collect_aves(file):

	open_rec = open(file, 'r')
	read_rec = open_rec.readlines()
	open_rec.close()

	x_list = []
	y_list = []
	z_list = []
	for line in read_rec:
		splitline = line.strip().split()
		at_type = line[0:6].strip()
                if at_type == "HETATM" or at_type == "ATOM":
			res_name = line[16:21].strip()
			#atom_name = line[11:16].strip()
			#atom_num = int(line[6:11].strip())
			#chain = line[21].strip()
			#res_num = int(line[22:30].strip())
			x = float(line[30:38].strip())
			y = float(line[38:46].strip())
			z = float(line[46:54].strip())
			#occ = float(line[55:60].strip())
			#bfact = float(line[60:66].strip())
			#atom_name2 = line[76:79].strip()
			x_list.append(x)
			y_list.append(y)
			z_list.append(z)

	ave_x = np.mean(x_list)
	ave_y = np.mean(y_list)
	ave_z = np.mean(z_list)

	#for i in range(len(x_list)):
	#	x_list[i] = x_list[i] - ave_x
	#	y_list[i] = y_list[i] - ave_y
	#	z_list[i] = z_list[i] - ave_z
	
	return(ave_x, ave_y, ave_z, x_list, y_list, z_list)

def translate(ave_rec_x, ave_rec_y, ave_rec_z, ave_wat_x, ave_wat_y, ave_wat_z):

	x_dist = ave_rec_x - ave_wat_x
	y_dist = ave_rec_y - ave_wat_y
	z_dist = ave_rec_z - ave_wat_z

	magnitude = np.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
	print(magnitude)

	multiplier = -15/magnitude
	#new_coords = [ave_wat_x + (multiplier * x_dist), ave_wat_y + (multiplier * y_dist), ave_wat_z + (multiplier * z_dist)]
	new_coords = [(multiplier * x_dist), (multiplier * y_dist), (multiplier * z_dist)]

	return(new_coords)

def make_translate_duplicated(filein, new_coords):

    #file1 = gzip.open(filein,'r')
    file1 = open(filein,'r')
    lines = file1.readlines()

    file1.close()

    file2 = open("waters_moved.pdb",'w')

    new_lines = []
    x_adder = new_coords[0]
    y_adder = new_coords[1]
    z_adder = new_coords[2]

    for line in lines:
         linesplit = line.split() #split on white space  
         if linesplit[0] == "REMARK":
             file2.write(line)
         elif linesplit[0] == "ATOM" or linesplit[0] == "HETATM":
             new_lines.append(line)
             xt = float(line[30:38])
             yt = float(line[38:46])
             zt = float(line[46:54])

    for line in new_lines:
          # we want the invariant to be when all the waters are out of the binding sight.
          # so we make the translated water have conformation A.
          line = line[0:16] + 'A' + line[17:len(line)]
          xt = float(line[30:38])
          yt = float(line[38:46])
          zt = float(line[46:54])
          file2.write('%s  %7.3f %7.3f %7.3f %s' % (line[0:29],(xt+x_adder),(yt+y_adder),(zt+z_adder),line[55:len(line)]))
          #file2.write(line+'\n')
          # the old position when the waters are in the sight have conforation B. 
          line = line[0:16] + 'B' + line[17:len(line)]
          file2.write(line)
          #line[16] = 'B'

    file2.close()
    return

def main():

	rec_file = sys.argv[1]
	#water_file = sys.argv[2]

	ave_rec_x, ave_rec_y, ave_rec_z, recvx, recvy, recvz = collect_aves(rec_file)

	vecs = [recvx, recvy, recvz]
	M0 = np.cov(vecs)
	#print cov_out
	M = np.zeros((3,3))
	M1 = np.zeros((3,3))
        for i,v1 in enumerate(vecs):
		for j,v2 in enumerate(vecs):
			cov_out = np.cov(v1,v2)
			cor_out = scipy.stats.pearsonr(v1, v2)
			print cor_out
			M1[i,j] = cor_out[0]
			M[i,j] = cov_out[0][1]
        #cov_out = np.cov(recvx, recvy)	
        #exit()
	print M1
	print M0
	print M
        #print cov_out
	#w,v = la.eig(M)
	print "eigandecomp covariance matrix"
	w,v = la.eig(M)
	print w
        print v
	print "eigandecomp corelation matrix"
	w,v = la.eig(M1)
	print w
        print v
        #exit()
	#ave_wat_x, ave_wat_y, ave_wat_z = collect_aves(water_file)
	#output = open("ave_center.pdb",'w')
	#output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (5,"O", "HOH", 1, ave_rec_x, ave_rec_y, ave_rec_z, float(1.00), float(0.00), "O"))
	#output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (6,"O", "HOH", 1, ave_wat_x, ave_wat_y, ave_wat_z, float(1.00), float(0.00), "O"))
	#output.close()

	#new_water_coords = translate(ave_rec_x, ave_rec_y, ave_rec_z, ave_wat_x, ave_wat_y, ave_wat_z)

	magnitude = la.norm(v[2])
        print magnitude
	#make_translate_duplicated(water_file, -w[2]/3.0 * v[2])
	#scale = 3.
	scale = 0.01
	
	output = open("new_center.pdb",'w')
	output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (5,"C", "HOH", 1, ave_rec_x, ave_rec_y, ave_rec_z, float(1.00), float(0.00), "C"))
	output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (5,"C", "HOH", 1, ave_rec_x-w[0]/scale * v[0][0], ave_rec_y-w[0]/scale * v[0][1], ave_rec_z-w[0]/scale * v[0][2], float(1.00), float(0.00), "C"))
	output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (5,"C", "HOH", 1, ave_rec_x-w[1]/scale * v[1][0], ave_rec_y-w[1]/scale * v[1][1], ave_rec_z-w[1]/scale * v[1][2], float(1.00), float(0.00), "C"))
	output.write("ATOM  %5d  %-3s %3s   %3d  %10.3f%8.3f%8.3f%6.2f%6.2f           %s\n" % (5,"C", "HOH", 1, ave_rec_x-w[2]/scale * v[2][0], ave_rec_y-w[2]/scale * v[2][1], ave_rec_z-w[2]/scale * v[2][2], float(1.00), float(0.00), "C"))
	output.close()



main()
