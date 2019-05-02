from __future__ import print_function
import os,sys
import numpy as np
from argparse import ArgumentParser
from collections import defaultdict
from subprocess import call
import pandas as pd

parser = ArgumentParser(description='')

parser.add_argument('--com', dest='com', default='01mi.com.out', help='.')
parser.add_argument('--lig', dest='lig', default='02sp.lig.out', help='.')
parser.add_argument('--rec', dest='rec', default='03sp.rec.out', help='.')

parser.add_argument('--mol2',      dest='poses', metavar='<poses.mol2 FILE>', default='poses.mol2', 
	help='Read the poses.mol2 file to create a dictionary between ZINC ID and pose number.')
parser.add_argument('-t', '--txt', dest='score_file', metavar='<txt FILE>', 
	help='original extract_all.sort.unique.txt file.')

def main():
	opt = parser.parse_args()


	global dict_zinc2pose
	global dict_pose2zinc
	dict_zinc2pose, dict_pose2zinc = {}, {}
	if os.path.isfile('zinc_pose.txt'):
		with open('zinc_pose.txt', "r") as f:
			for line in f:
				zincID, poseName = line.split()[0], line.split()[1]
				dict_zinc2pose[zincID] = poseName
				dict_pose2zinc[poseName] = zincID
	else:
		dict_zinc2pose, dict_pose2zinc = read_mol2(opt.poses)

	#cwd = os.getcwd()
	#dir = './004_complex_min/'
	fo = open('extract_all_amber.txt', "w")

	os.chdir('./004_complex_min/')
	poses_list = []
	for name in os.listdir('.'):
		if os.path.isdir(name):
			poses_list.append(name)
	print(len(poses_list))

	for i in range( len(poses_list) ):
		poseName = poses_list[i]
		egy = {}
		call("grep -A12 FINAL %s/01mi.com.out > tmp.txt" % poses_list[i], shell=True)
		egy['com'] = read_egy()
		call("grep -A11 FINAL %s/02sp.lig.out > tmp.txt" % poses_list[i], shell=True)
		egy['lig'] = read_egy()
		call("grep -A11 FINAL %s/03sp.rec.out > tmp.txt" % poses_list[i], shell=True)
		egy['rec'] = read_egy()
		#print(egy)
		#df = pd.DataFrame(egy, index=['ENERGY','BOND', 'ANGLE', 'DIHED', 'VDWAALS', 'EEL', 'EGB', '1-4 VDW', '1-4 EEL', 'RESTRAINT', 'ESURF'])
		#print(df)
		#df.to_csv('tmp.csv')
		egy_vdw  = egy['com'][4]  - egy['rec'][4]  - egy['lig'][4]
		egy_elst = egy['com'][5]  - egy['rec'][5]  - egy['lig'][5]
		egy_gb   = egy['com'][6]  - egy['rec'][6]  - egy['lig'][6]
		egy_surf = egy['com'][10] - egy['rec'][10] - egy['lig'][10]
		totalE = egy_elst+egy_vdw+egy_gb+egy_surf
		zincID = dict_pose2zinc[poseName]
		fo.write("xxx 1 %s 1 1 1 1 1 1 1 1 1 %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %8.4f\n"
			% (zincID, egy_elst, 0, egy_vdw, egy_gb, egy_surf, 0, 0, 0, 0, totalE) )
	os.remove('tmp.txt')
	os.chdir('../')
	fo.close()

	command = "sort -k 22 -n extract_all_amber.txt > extract_all.sort.uniq.txt"
	call(command, shell=True)
	command = "sort -k 22 -n extract_all_amber.txt > extract_all.sort.uniq.txt_amber"
	call(command, shell=True)


def read_egy():

	egys = []
	with open('tmp.txt', "r") as f:
		for oneline in f:
			if oneline.find("ENERGY") > -1:
				ele = next(f).split()
				egys.append(float(ele[1]))
			elif oneline.find("BOND") > -1:
				ele = oneline.split()
				egys.extend([float(ele[2]), float(ele[5]), float(ele[8])])
			elif oneline.find("VDWAALS") > -1:
				ele = oneline.split()
				egys.extend([float(ele[2]), float(ele[5]), float(ele[8])])
			elif oneline.find("RESTRAINT") > -1:
				ele = oneline.split()
				egys.extend([float(ele[3]), float(ele[7]), float(ele[10])])
			elif oneline.find("ESURF") > -1:
				ele = oneline.split()
				egys.append(float(ele[2]))
			#elif oneline.find("EAMBER") > -1:
			#	ele = oneline.split()
			#	egys.append(float(ele[2]))

	return egys

def read_mol2(infile):
	fo = open('zinc_pose.txt', "w")
	counter = 0
	zinc2pose, pose2zinc = {}, {}
	with open(infile, "r") as f:
		for oneline in f:
			if oneline.find("MOLECULE") > -1:
				counter += 1
				nextline = next(f)
				zincID = nextline.split()[0]
				poseName = 'poses_%05d' % (counter)
				zinc2pose[zincID] = poseName
				zinc2pose[poseName] = zincID
	for key in sorted(zinc2pose.iterkeys()):
		fo.write("%20s\t%10s\n" % (key, zinc2pose[key]) )
	fo.close()
	return zinc2pose, pose2zinc


if __name__ == "__main__":
    main()
