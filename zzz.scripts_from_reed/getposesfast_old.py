

# This script is written by Reed Stein and Trent Balius in April, 2017.  
# This a fast get poses script


import os
import sys
import gzip

def get_zinc_names_and_chunks_from_extract_all_sort_uniq(filename,N):
	print "running function: get_zinc_names_and_chunks_from_extract_all_sort_uniq"
	fh = open(filename,'r')
	zinc_dic = {}
        count = 0
        for line in fh:
		splitline = line.split()
		zincid = splitline[2]
		chunk  = splitline[0]
                zinc_dic[zincid] = chunk
		#print chunk, zincid 
		count = count + 1
		if count > N: 
			break
	return zinc_dic

def process_gz(filename, lig_dict, chunk, zinclist):
	print "running function: process_gz"
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

		if not (name in zinclist): #skip any ligand not in list (dictionary)
                        #print name 
			continue

                if not (name in lig_dict):
                        lig_dict[name] = [line_num, tot_e, chunk] 
			#print name, line_num, tot_e

                elif name in lig_dict and lig_dict[name][1] > tot_e:
			lig_dict[name][0] = line_num
                        lig_dict[name][1] = tot_e
			lig_dict[name][2] = chunk
			#print "update", name, line_num, tot_e

        return lig_dict

def write_out_poses(lig_dict, lig_dir):
	print "running function: write_out_poses"

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
		#print dirname_l
		line_number_list = line_number_dict[dirname_l]	
		#print line_number_dict[dirname_l] 
		db2_gz_file = lig_dir+dirname_l+"/test.mol2.gz" 

		ligandFile = gzip.open(db2_gz_file,'rb')
		new_line_count = 0
		name_found  = False
		header_flag = False

		for new_line in ligandFile:
			splitline = new_line.strip().split()

			if new_line_count in line_number_list:  # line is in the list so set flag to True for writting out
				#print(new_line)
				if len(splitline) > 1:
					if splitline[1] == "Name:":
						name_found = True	
						#output.write(new_line)
			else: # otherwise see if you are have reached a new pose if that is not in the list then stop writting. 
				if (len(splitline) > 1):
					if splitline[1] == "Name:" and name_found and new_line_count not in line_number_list:
						name_found = False

			if new_line[0] == "#" and not header_flag:
                                #print new_line
				header_flag = True
                                header = ''
				header=header+new_line
			        new_line_count += 1
				continue
                        if new_line[0] == "#":
				header=header+new_line
			        new_line_count += 1
				continue
                           
			if name_found:
				if header_flag: # line 91. if the header flag is true and it is no longer in the header and it is a pose you want to write, write the header frist. 
					output.write(header)
				output.write(new_line)

			if new_line[0] != "#": # if line does not start with a # symbol then set header flag to false. setting to false must go after line 91.  
				header_flag = False

			new_line_count += 1

        	ligandFile.close()

	output.close()

def main():

	docking_dir = sys.argv[1]

        extractname = sys.argv[2]
        number_of_poses = int(sys.argv[3])
        print "docking_dir: "+docking_dir
        print "extractname: "+extractname
	print "number_of_poses: "+str(number_of_poses)        
	extractfile = docking_dir+extractname
        print "extract file path: "+extractfile
	#os.chdir(lig_dir)

	#if os.path.isfile(lig_dir+"poses.mol2"):
	#if os.path.isfile(docking_dir+"poses.mol2"):
	if os.path.isfile("poses.mol2"):
		print "poses.mol2 already exists. Quitting."
		sys.exit()
	
	#extractfile = docking_dir+"extract_all.sort.uniq.txt"
	if not os.path.isfile(extractfile):
		print "there needs to be an extract_all.sort.uniq.txt. "
		exit()

	zinc_dic = get_zinc_names_and_chunks_from_extract_all_sort_uniq(extractfile,number_of_poses)
	#print zinc_dic.keys()
	#chunk_list = [name for name in os.listdir(".") if os.path.isdir(name) and name[0:5] == "chunk"]
	chunk_dic = {}
	chunk_list = []
	for key in zinc_dic:
		if not (zinc_dic[key] in chunk_dic):
			chunk_list.append(zinc_dic[key])
			chunk_dic[zinc_dic[key]]=0
		chunk_dic[zinc_dic[key]] = chunk_dic[zinc_dic[key]] + 1


	lig_dict = {}
	for chunk in chunk_list:
		print chunk, chunk_dic[chunk]
		gz_file = docking_dir+chunk+"/test.mol2.gz"			
		lig_dict = process_gz(gz_file, lig_dict, chunk, zinc_dic)

	write_out_poses(lig_dict, docking_dir)
	
main()
