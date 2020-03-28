# /usr/bin/python

import os, sys

# This script takes the intially downloaded pdb files and filters out those containing multiple models. It takes those with multiple models and breaks them up so that each model becomes its own individual file

# This script was created by Alyssa Klein on 6/14/2019
# modifed by Trent Balius at FNLCR on March 16, 2020.  

# Define a main function that will contain two functions:
# 1) Take in the name of the pdb text file that contains the list of the *.pdb files and form the file input into a list to make it easier to use in the second function
# 2) a) Read in the lines of each of the pdb files 
#    b) Filter out those entries that contain multiple models within them
#    c) Split those with multiple models into individual files (pdbcode_1.pdb and increasing in number with each additional model for a particular entry)
#    d) If the entry does not have multiple models, create a new file for that entry with the filename pdbcode_0.pdb

# Open the pdb text file that contains the list of the initially downloaded *.pdb files
def get_pdb_list(list_file):
	#file_to_open = open("/home/kleinam/klein_kras_analysis/pdb_files_kras_80.txt", "r")
	file_to_open = open(list_file, "r")
	pdbfilelist = [] # initialize a list that will contain pdb filenames
	for line in file_to_open: # initiate a for loop to read in each line of the pdbfiles.txt file 
		pdbfile = line.strip() # strip off any excess whitespace
		#print(pdbfile) # print what is stored in the pdbfile in order to make sure the loop is working correctly
		pdbfilelist.append(pdbfile) # append the pdbfilelist list with pdbfile
		#print(pdbfilelist) 
	return pdbfilelist # return the pdbfilelist so that it can be used in the pdb_model_split function
# Separate pdb entries with multiple models into individual files
def pdb_model_split(pdbfile):
	#print(pdbfile)
	file_prefix = pdbfile.split('.')[0] # Declare a variable to be the first portion of the split pdbfile name
	fh_pdb = open(pdbfile, "r") # Open the pdbfile
	dict_model = {} # Inititate a dictionary to be used to store entries that do not contain multiple models
	model_number = 0 # Declare a variable model_number and initialize it to have a value of 0
	new_file_for_model = "" # Declare a variable set to empty so that contents from entries with multiple models can be stored in it
        flag_model = False # flag_model is true if MODEL is present in the file and false if it is not in the file.  
        frist_occurence = True 
  
	#for line in fh_pdb: # Initiate a for loop to look for entries that do not contain multiple models
	#	if "MODEL" not in fh_pdb: # if statement to look for the word "MODEL" in each line of each entry; is "MODEL" is not found, then:
	#		model_number = 0 # The model_number variable remains at 0
	#		model_name = ("model_" + str(model_number)) # Declare a variable that will later be used to the creation of the filename for the contents
	#		if not (model_number in dict_model): # if statement to see if the dictionary already has a specific key
	#			dict_model[model_number] = '' # Initialize a key if it does not exist
	#		dict_model[model_number] = dict_model[model_number] + line # Modify the dictionary entry with the key and the line(s)
	#		#break
	for line in fh_pdb: # Initiate a for loop to look within the pdb entries that do have multiple models within them
		line = line.strip () # Remove trailing whitespace
                if "MODEL" == line[0:5]:
     		    model_number = int(line[10:15])
		    print ("There are multiple models for this pdb entry: " + file_prefix + ".")
                    flag_model = True
                    dict_model[model_number] = ''
                    new_file_for_model += line + '\n' # then the new_file_for_model variable continues to have contents added to it 
                if "ATOM" == line[0:4]: 
                    if not (flag_model) and frist_occurence: 
                        print "only one model. no number assigned in file: " + pdbfile
                        frist_occurence = False
     		if line == "ENDMDL": # If statement that attempts to find "ENDMDL" string; If "ENDMDL" is found, then:
         		new_file_for_model += line + '\n' # then the new_file_for_model variable continues to have contents added to it 
         		output_file = open(file_prefix + "_model_" + str(model_number) + ".pdb", "w") # A file is open with the corresponding name
         		output_file.write(new_file_for_model) # The file that was created in the previous line is written to 
         		output_file.close()# The file that was created and written to is closed
         		#model_number += 1 # The model number increases by one
        		new_file_for_model = "" # The new_file_for_model resets to become empty so the process can begin again if needed
     		elif not line.startswith("MODEL"): # If the line does not start with "MODEL"
         		new_file_for_model += line + '\n' # then the new_file_for_model variable continues to have contents added to it 

        if not (flag_model):
                output_file = open(file_prefix + "_model_" + str(model_number) + ".pdb", "w") # A file is open with the corresponding name
                output_file.write(new_file_for_model) # The file that was created in the previous line is written to
                output_file.close()# The file that was created and written to is closed
                new_file_for_model = "" # The new_file_for_model resets to become empty so the process can begin again if needed


	fh_pdb.close() # Close the fh_pdb file
	#for model in dict_model.keys(): # For loop to use the dictionary that was created for entries that lacked multiple models
	#	#print file_prefix + "_" + model_name + ".pdb")
	#	file = open(file_prefix + "_" + model_name + ".pdb", "w") # Open a file with the corresponding filename
	#	file.write(dict_model[model]) # Write to the file the dictionary value
	#	file.close() # Close the file when it is finished being written to
			

def main(): # Define a main function to call the other functions
        if len(sys.argv) != 2: # if no input
           print "ERORR: not the right number of arguments."
           print "this script takes in to input files that contains a list of pdbfiles"
           return
        filelist = sys.argv[1]
        print("file = %s"%(filelist))
	pdbs = get_pdb_list(filelist) # set get_pdb_list() equal to pdbs so it can be used in the pdb_model_split() function
	
	for pdb in pdbs:
	   pdb_model_split(pdb)

main()







