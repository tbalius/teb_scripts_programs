import os
import os.path
import mol2
import sys
from collections import Counter
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


######################################################################################################################################################################################


def multimol2_removeH(input, output):
	#print "This file requires the mol2 library written by Trent Balius (AKA Xiaobo Wan) and sudipto mukherjee"

	#print "syntex: multimol2_removeH.py input_file output_file"

	infile = input
	outfile = output

	file = open(outfile,'w') # overwrite
	file.close()

	mol_list = mol2.read_Mol2_file_head(infile)
	#print len(mol_list)

	for i in range(len(mol_list)):
  		#print "mol ", i
  		mol = mol2.remove_hydrogens( mol_list[i] )
  		mol2.append_mol2(mol,outfile)


######################################################################################################################################################################################


def read_dock_multimol2_file_printmol2_files(file,setname):
    # reads in data from mol2 file produesed by dock.

    file1 = open(file,'r')

    #outputfilename = outputprefix + str("_00001.mol2") 
    #file2 = open(outputfilename,'w')
    lines  =  file1.readlines()
    count = 1

    flag = True  ## flag is true for the first lin that is not a comment.

    header = ''

    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >0 ):

             if (linesplit[0][0] != "#"):
                 flag = True
             else:
                 flag = False
                 header = header + line
                 if (len(linesplit) == 3):
                     if (linesplit[1] == "Name:"):
                         #print line
                         outputprefix = linesplit[2]+ "_" + setname
             if (flag and linesplit[0] == "@<TRIPOS>MOLECULE"):
                 if (count > 1):
                    file2.close()
                 if (count < 10):
                    outputfilename = outputprefix + str("_0000") + str(count) + str(".mol2")
                 elif (count <100):
                    outputfilename = outputprefix + str("_000") + str(count) + str(".mol2")
                 elif (count <1000):
                    outputfilename = outputprefix + str("_00") + str(count) + str(".mol2")
                 elif (count <10000):
                    outputfilename = outputprefix + str("_0") + str(count) + str(".mol2")
                 else:
                    outputfilename = outputprefix + str("_") + str(count) + str(".mol2")
                 file2 = open(outputfilename,'w')
                 file2.write(header)
                 file2.write(line)
                 count = count+1
                 #flag = False
                 header = ''
             elif (flag):
                 file2.write(line)
    return


######################################################################################################################################################################################

def find_uniq_compounds(file1, file2):
	lig_list1 = []
	lig_list2 = []
	file_list = [file1, file2]
	
	for filex in file_list:
		pose_files = open(filex)
		poses = pose_files.readlines()
		pose_files.close()

		for line in poses:
			line = line.strip().split()
			if len(line)>1 and line[1] == "Name:":
				lig_list1.append(line[2])

	lig_dict = Counter(lig_list1)
	lig_dict_copy = dict(lig_dict)
	
	for lig in lig_dict:
		if lig_dict[lig] != 2:
			del lig_dict_copy[lig]
	
	for lig in lig_dict_copy:
		lig_list2.append(lig)

	lig_list2 = sorted(lig_list2)
	return lig_list2

######################################################################################################################################################################################


def dock_read_in(id_code, pose1, pose2):
	input_file = "rmsd."+id_code+".in"
	output_file = "rmsd."+id_code+".out"
	output = open(input_file,"w")
	output.write("ligand_atom_file                                             "+pose1+"\n") 
	output.write("limit_max_ligands                                            no\n")
	output.write("skip_molecule                                                no\n")
	output.write("read_mol_solvation                                           no\n")
	output.write("calculate_rmsd                                               yes\n")
	output.write("use_rmsd_reference_mol                                       yes\n")
	output.write("rmsd_reference_filename                                      "+pose2+"\n")
	output.write("use_database_filter                                          no\n")
	output.write("orient_ligand                                                no\n")
	output.write("use_internal_energy                                          no\n")
	output.write("flexible_ligand                                              no\n")
	output.write("bump_filter                                                  no\n")
	output.write("score_molecules                                              no\n")
	output.write("atom_model                                                   all\n")
	output.write("vdw_defn_file                                                vdw_AMBER_parm99.defn\n")
	output.write("flex_defn_file                                               flex.defn\n")
	output.write("flex_drive_file                                              flex_drive.tbl\n")
	output.write("ligand_outfile_prefix                                        "+id_code+"_rmsdcalc\n")
	output.write("write_orientations                                           no\n")
	output.write("num_scored_conformers                                        1\n")
	output.write("rank_ligands                                                 no\n")
	output.close()
	
	os.system("/nfs/home/tbalius/zzz.programs/dock6.6/dock6/bin/dock6 -i "+input_file+" -o "+output_file)

######################################################################################################################################################################################


def write_out(list, outputH):
        first = 0
        n_2 = first
        for n in range(len(list[:33])):
		outputH.write(list[n])
        for line in list:
                first += 1
                line = line.strip().split()
                if len(line) > 0 and line[0] == "@<TRIPOS>BOND":
                        n_2 = first
        for j in range(33,n_2-1):
                outputH.write('%s%-5s%s'% (list[j][0:42], sybyl_to_element(list[j][42:51].strip()), list[j][51:]))
        for line in list[n_2-1:]:
                outputH.write(line)

######################################################################################################################################################################################

def sybyl_to_element(line):
        if line[:2] == "C.":
                line = line.replace(line,"C")
        if line[:2] == "N.":
                line = line.replace(line,"N")
        if line[:2] == "O.":
                line = line.replace(line,"O")
        if line[:2] == "S.":
                line = line.replace(line,"S")
        if line[:2] == "P.":
                line = line.replace(line,"P")
        return(line)

######################################################################################################################################################################################

def get_rmsd(rmsd_dict):
	output = open("rmsd.txt","w")
	
	for key in rmsd_dict:
		name = key[0]
		#print(name)
		pose1 = key[1][0]
		#print(pose1)
		pose2 = key[1][1]
		rmsd_mol2_file = name+"_rmsdcalc_scored.mol2"
		rmsd_file = open(rmsd_mol2_file)
		rmsd = rmsd_file.readlines()
		rmsd_file.close()
	
		for line in rmsd:
			line = line.strip().split()
			if len(line)>1 and line[1] == "HA_RMSDh:":
				#print("yes")
				output.write("%-25s%45s%45s%25s\n"%(name,pose1,pose2,line[2]))
	output.close()


######################################################################################################################################################################################

def plot_hist(rmsd_file, system):
	
	rmsd_file = open(rmsd_file)
	#os.system("ls")
	rmsdlines = rmsd_file.readlines()
	rmsd_file.close()
	rmsd_list = []

	for line in rmsdlines:
		line = line.strip().split()
		rmsd = float(line[3])
		rmsd_list.append(rmsd)
	
	mu = np.mean(rmsd_list)
	sigma = np.std(rmsd_list)
	#x = mu + sigma*np.random.randn(10000)
	num_bins = 20	
	n, bins, patches = plt.hist(rmsd_list, num_bins)
	#y = mlab.normpdf(bins, mu, sigma)
	#plt.plot(bins, y, 'r--')
	plt.xlabel('RMSD')
	plt.ylabel('Count')
	plt.title(system)
	plt.subplots_adjust(left=0.15)
	plt.savefig(system+"_pose_RMSD", dpi=1000)
	plt.clf()

######################################################################################################################################################################################

def main():

	pwd = os.getcwd()+"/"

	#pdb = sys.argv[1]

	docking_dir = pwd+"docking/2runEnrich/"

	os.chdir(docking_dir)
	
	
	#docking_dir_list = [name for name in os.listdir(".") if os.path.isdir(name) and name[-4:] == "gist"]

# compares to the 1st one - aka _nogist should be the first in list. 
	sys_dict = {"RMSD":["4NVA_nogist", "4NVA_gist", "4NVA_min"]}

	
	#for direc in docking_dir_list:
	#	sys_dict["RMSD"].append(direc)
	#print(sys_dict)


	for key in sys_dict:	
		dir_name = key
		#standard = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+sys_dict[key][0]
		standard = docking_dir+sys_dict[key][0]
		gist_system = sys_dict[key][1:]
		new_dir1 = docking_dir+dir_name
		print "Making directory",new_dir1
		#os.system("rm -rf "+new_dir1)
		os.system("mkdir "+new_dir1)

		print(standard)		


		for gtype in gist_system:
			system_name = gtype 
			gist = docking_dir+gtype
			print(gtype)
			new_dir2 = docking_dir+dir_name+"/RMSD_"+gtype
			#os.system("rm -rf "+new_dir2)
			print "Making directory",new_dir2
			os.system("mkdir "+new_dir2)
			print "changing into directory",new_dir2
			os.chdir(new_dir2)
			#os.system("ln -s /nfs/home/tbalius/zzz.scripts/mol2.py .")
			os.system("ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/vdw_AMBER_parm99.defn .")
			os.system("ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex.defn .")
			os.system("ln -s /nfs/home/tbalius/zzz.programs/dock6.6/dock6/parameters/flex_drive.tbl .")

			standard_poses = standard+"/ligands/allChunksCombined/poses.mol2"
			gist_poses = gist+"/ligands/allChunksCombined/poses.mol2"
			print(standard_poses, gist_poses)
			
			multimol2_removeH(standard_poses,"poses1_noh.mol2")
			multimol2_removeH(gist_poses,"poses2_noh.mol2")
		
			read_dock_multimol2_file_printmol2_files("poses1_noh.mol2", "set1")
			read_dock_multimol2_file_printmol2_files("poses2_noh.mol2", "set2")

			lig_list = find_uniq_compounds(standard_poses,gist_poses)
			if os.path.isfile("rmsd.*.in"):
				os.system("rm rmsd.*.in") 
			if os.path.isfile("rmsd.*.out"):
				os.system("rm rmsd.*.out")
			if os.path.isfile("rmsd.txt"):
				os.system("rm rmsd.txt")
			
			rmsd_dict = {} 
			
			for lig in lig_list:
				rmsd_dict[lig] = []
				dup_list = []
				dup_list_mod = []
				duplicates = os.popen("ls "+lig+"_*")
				for dup in duplicates:		
					mol2_list = []
					dup = dup.strip().split()
					dup = dup[0]
					dup_list.append(dup)
					rmsd_dict[lig].append(dup)
					rmsd_file = open(dup)
					rmsd_file_read = rmsd_file.readlines()
					rmsd_file.close()
					for line in rmsd_file_read:
						mol2_list.append(line)
					output_rmsd_file = dup.strip().split(".mol2")[0]+"_mod.mol2"
					output_rmsd = open(output_rmsd_file,"w")
					write_out(mol2_list,output_rmsd)
					output_rmsd.close()
				for i in range(len(dup_list)):
					dup_list_mod.append(dup_list[i].strip().split(".mol2")[0]+"_mod.mol2")
				#print(dup_list_mod[0],dup_list_mod[1])
				dock_read_in(lig, dup_list_mod[0],dup_list_mod[1])
			rmsd_dict = sorted(rmsd_dict.items(), key = lambda x:x[1]) 
			get_rmsd(rmsd_dict)
			plot_hist("rmsd.txt",system_name)
main()
