import os
import sys
import gzip

def process_gz(file,lig_dict, chunk):
        #this function collects the name, grids, and total energy of the best scoring pose of each ligand

        lig_list = []
        ligandFile = gzip.open(file,'rb')
        lig_line = []

	line_count = 0
        for line in ligandFile:
                if len(lig_line) == 3:
                        lig_list.append(lig_line)
                        lig_line = []

                line1 = line.strip().split()
                if len(line1) > 1:
                        if line1[1] == "Name:":
				lig_line.append(line_count)
                                lig_line.append(line1[2])
                        elif line1[1] == "Total":
                                lig_line.append(line1[3])

		line_count += 1

        for comp in lig_list:
                line_num = comp[0]
                name = comp[1]
                tot_e = float(comp[2])

                if name not in lig_dict:
                        lig_dict[name] = [line_num, tot_e, chunk] 

                elif name in lig_dict and lig_dict[name][1] > tot_e:
			lig_dict[name][0] = line_num
                        lig_dict[name][1] = tot_e
			lig_dict[name][2] = chunk

        return lig_dict

def write_out_poses(lig_dict, lig_dir):

	line_number_dict = {}

	for name in lig_dict:
		line_num = lig_dict[name][0]
		chunk_num = lig_dict[name][2].split("chunk")[-1]
		if chunk_num in line_number_dict:
			line_number_dict[chunk_num].append(line_num)
		else:
			line_number_dict[chunk_num] = [line_num]
			
	output = open("poses.mol2",'w')

	for chunk_num in line_number_dict:
		line_number_list = line_number_dict[chunk_num]	
		db2_gz_file = lig_dir+"chunk"+str(chunk_num)+"/test.mol2.gz" 

		ligandFile = gzip.open(db2_gz_file,'rb')
		new_line_count = 0
		name_found = False
		for new_line in ligandFile:
			splitline = new_line.strip().split()

			if new_line_count in line_number_list:
				#print(line)
				if len(splitline) > 1:
					if splitline[1] == "Name:":
						name_found = True	
						output.write(new_line)
			elif len(splitline) > 1:
				if splitline[1] == "Name:" and name_found == True and new_line_count not in line_number_list:
					name_found = False
				elif splitline[1] != "Name:" and name_found == True:
					output.write(new_line)
			elif name_found == True:
				output.write(new_line)

			new_line_count += 1

        	ligandFile.close()

	output.close()

def main():

	pwd = os.getcwd()+"/"

	docking_dir = sys.argv[1]
	dock_type = sys.argv[2]

	lig_dir = pwd+docking_dir+"/DOCKING_"+dock_type+"/ligands/"
	os.chdir(lig_dir)

	if os.path.isfile(lig_dir+"poses.mol2"):
		print "poses.mol2 already exists. Quitting."
		sys.exit()
	
	chunk_list = [name for name in os.listdir(".") if os.path.isdir(name) and name[0:5] == "chunk"]

	lig_dict = {}
	for chunk in chunk_list:
		print(chunk)
		gz_file = lig_dir+chunk+"/test.mol2.gz"			
		os.chdir(lig_dir+chunk)
		lig_dict = process_gz(gz_file, lig_dict, chunk)
		os.chdir(lig_dir)

	write_out_poses(lig_dict, lig_dir)
	
main()
