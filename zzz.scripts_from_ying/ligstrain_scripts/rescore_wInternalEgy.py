from __future__ import print_function
import os,sys
import numpy as np
from argparse import ArgumentParser
from collections import defaultdict
from subprocess import call


parser = ArgumentParser(description='')

parser.add_argument('--lig_complex', dest='lig_complex', default='lig_complex.txt', 
	help='single point ligand energy after minimized in the context of protein.')
parser.add_argument('--lig_global', dest='lig_glob_min', default='lig_glob_min.txt', 
	help='minimized energy of omega generated conformers representing global minimum.')

parser.add_argument('-t', '--txt', dest='score_file', metavar='<txt FILE>', 
	help='extract_all.sort.unique.txt file without internal energy.')

def main():
	opt = parser.parse_args()

	if os.path.isfile("zincID_interEgy.txt"):
		dict_zinc_inter = read_egy("zincID_interEgy.txt")
	else:
		dict_zinc_inter = read_internal_energy(opt.lig_complex, opt.lig_glob_min)
	update_score(opt.score_file, dict_zinc_inter)

def read_egy(infile):
	dict_egy = {}
	with open(infile, "r") as f:
		for oneline in f:
			ele = oneline.split()
			dict_egy[ele[0]] = float( ele[1] )
	return dict_egy

def read_internal_energy(lig_complex, lig_min):

	lig_cmp_egy = read_egy(lig_complex)
	lig_min_egy = read_egy(lig_min)
	
	fo = open("zincID_interEgy.txt", "w")
	dict_zinc_inter = {}
	for key in sorted(lig_cmp_egy.keys()):
		if key in lig_min_egy:
			dict_zinc_inter[ key ] = lig_cmp_egy[key] - lig_min_egy[key]
			fo.write("%20s\t%10.3f\n" % (key, lig_cmp_egy[key] - lig_min_egy[key]))

 	return dict_zinc_inter

def update_score(score_file, dict_zinc_inter):

	out_name = "extract_all.inter.txt" 
	fo = open(out_name, "w")

	with open(score_file, "r") as f:
		for oneline in f:
			ele = oneline.split()
			totalE = float(ele[-1])

#			if ele[2].find("ZINC") > -1:
#				zincID = ele[2]
#			else:
#				zincID = "ZI"+ele[2]

			zincID = ele[2]
			
			if zincID not in dict_zinc_inter:
				continue
			else:
				internal_energy = float(dict_zinc_inter[zincID])
				totalE += internal_energy
				if ele[2].find("ZINC") > -1:
					newline = '\t'.join(ele[:17])
					newline += "%6.2f  %6.2f  %6.2f  %6.2f   %7.2f\n" % (internal_energy, 0,0,0, totalE)
					fo.write(newline)
				else:
#					name = "ZINC" + ele[2].rsplit("_", 1)[0].split("C")[-1] # back ZINC name too long
					name = ele[2].rsplit("_", 1)[0]
					newline = '\t'.join(ele[:2])
					newline += "\t%s\t" % name
					newline += '\t'.join(ele[3:17])
					newline += "%6.2f  %6.2f  %6.2f  %6.2f   %7.2f\n" % (internal_energy, 0,0,0, totalE)
					fo.write(newline)
				
	fo.close()

#	command = "sort -k 22 -n %s > extract_all.sort.uniq.txt_%s" % (out_name, ref)
#	call(command, shell=True)
	command = "sort -k 22 -n %s > extract_all.sort.uniq.txt" % out_name
	call(command, shell=True)


if __name__ == "__main__":
    main()




"""
from __future__ import print_function
import os,sys
import numpy as np
from argparse import ArgumentParser
from collections import defaultdict
from subprocess import call


parser = ArgumentParser(description='')
parser.add_argument('--mol2',      dest='poses', metavar='<poses.mol2 FILE>', default='poses.mol2', 
	help='Read the poses.mol2 file to create a dictionary between ZINC ID and pose number.')

parser.add_argument('--lig_complex', dest='lig_complex', default='lig_complex.txt', 
	help='single point ligand energy after minimized in the context of protein.')
parser.add_argument('--lig_local', dest='lig_local_min', default='lig_local_min.txt', 
	help='minimized energy of ligand extracted from complex representing local minimum.')
parser.add_argument('--lig_global', dest='lig_glob_min', default='lig_glob_min.txt', 
	help='minimized energy of omega generated conformers representing global minimum.')
parser.add_argument('-r', '--ref', dest='ref_min', choices=['local', 'global'], 
	help='Reference minimum for ligand internal energy. local or global')

parser.add_argument('-t', '--txt', dest='score_file', metavar='<txt FILE>', 
	help='extract_all.sort.unique.txt file without internal energy.')


def main():
	opt = parser.parse_args()

	dict_pose2zinc  = read_mol2(opt.poses)

	if opt.ref_min == 'global':
		dict_zinc_inter = read_internal_energy(opt.lig_complex, opt.lig_glob_min, dict_pose2zinc)
 	elif opt.ref_min == "local":
		dict_zinc_inter = read_internal_energy(opt.lig_complex, opt.lig_local_min, dict_pose2zinc)

	update_score(opt.ref_min, opt.score_file, dict_zinc_inter)


def read_mol2(infile):
	counter = 0
	dict_pose2zinc = {}
	with open(infile, "r") as f:
		for oneline in f:
			if oneline.find("MOLECULE") > -1:
				counter += 1
				nextline = next(f)
				zincID = nextline.split()[0]
				poseName = 'poses_%05d' % (counter)
				dict_pose2zinc[poseName] = zincID
	#for key in sorted(dict_pose2zinc.iterkeys()):
	#	print(key, "---", dict_pose2zinc[key])
	return dict_pose2zinc

def read_internal_energy(lig_complex, lig_min, dict_pose2zinc):
	#command = "paste %s %s %s | awk '{print $1\" \"$2\" \"$4\" \"$6\" == \"$2-$4\" == \" $2-$6}'"

# new internal energy
#	command = "paste %s %s | awk '{print $1 \"  \" $2-$4}' > inter.txt " %(lig_complex, lig_min)
# 	call(command, shell=True)


	
	dict_zinc_inter = {}
 	with open('inter.txt', "r") as f:
 		for oneline in f:
 			if len( oneline.split() ) > 1:
 				poseName = oneline.split()[0]
 				internal_energy = oneline.split()[1]
 				zincID = dict_pose2zinc[poseName]
 				dict_zinc_inter[zincID] = internal_energy
 			else:
 				print("\nError! Check the pose and score of the following line...")
 				print(oneline)
	#for key in sorted(dict_zinc_inter.iterkeys()):
	#	print(key, "---", dict_zinc_inter[key])
 	return dict_zinc_inter

def update_score(ref, score_file, dict_zinc_inter):

	out_name = "extract_all.inter_%s.txt" % (ref)
	fo = open(out_name, "w")

	with open(score_file, "r") as f:
		for oneline in f:
			ele =  oneline.split()
			zincID = ele[2]
			totalE = float(ele[-1])
			if zincID not in dict_zinc_inter:
				continue
			internal_energy = float(dict_zinc_inter[zincID])
			totalE += internal_energy

			newline = '\t'.join(ele[:17]) 
			newline += "%6.2f  %6.2f  %6.2f  %6.2f   %7.2f\n" % (internal_energy, 0,0,0, totalE)
			#print(newline)
			fo.write(newline)
	fo.close()

#	command = "sort -k 22 -n %s > extract_all.sort.uniq.txt_%s" % (out_name, ref)
#	call(command, shell=True)
	command = "sort -k 22 -n %s > extract_all.sort.uniq.txt" % out_name
	call(command, shell=True)


if __name__ == "__main__":
    main()

"""
