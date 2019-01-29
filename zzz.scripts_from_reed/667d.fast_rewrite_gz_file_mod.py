import os
import sys
import gzip

def process_gz(filename,lig_dict, chunk):
        #this function collects the name, grids, and total energy of the best scoring pose of each ligand

        lig_list = []
        ligandFile = gzip.open(filename,'rb')
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
		#chunk_num = lig_dict[name][2].split("chunk")[-1]
                dirname    = lig_dict[name][2]
		#if chunk_num in line_number_dict:
		if dirname in line_number_dict:
			line_number_dict[dirname].append(line_num)
		else:
			line_number_dict[dirname] = [line_num]
			
	output = open("poses.mol2",'w')

	for dirname_l in line_number_dict:
		line_number_list = line_number_dict[dirname_l]	
		db2_gz_file = lig_dir+dirname_l+"/test.mol2.gz" 

		ligandFile = gzip.open(db2_gz_file,'rb')
		new_line_count = 0
		name_found  = False
		header_flag = False

		for new_line in ligandFile:
			if new_line[0] == "#" and not header_flag:
				header_flag = True
                                header = ''
				continue
                        elif new_line[0] == "#":
				header=header+new_line
				continue
                           
			splitline = new_line.strip().split()

			if new_line_count in line_number_list:  # line is in the list so set flag to True for writting out
				#print(line)
				if len(splitline) > 1:
					if splitline[1] == "Name:":
						name_found = True	
						#output.write(new_line)
			else: # otherwise see if you are have reached a new pose if that is not in the list then stop writting. 
				if (len(splitline) > 1):
					if splitline[1] == "Name:" and name_found == True and new_line_count not in line_number_list:
						name_found = False

			if name_found == True:
				if header_flag and new_line[0] != "#": # line 91. if the header flag is true and it is no longer in the header and it is a pose you want to write, write the header frist. 
					output.write(header)
				output.write(new_line)

			if new_line[0] != "#": # if line does not start with a # symbol then set header flag to false. setting to false must go after line 91.  
				header_flag = False

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
