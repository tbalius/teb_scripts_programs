# /usr/bin/python 

# This script takes in the contents of the .pdb files for the corresponding pdb codes, opens it, scans the file for the chains, and then splits the chains into individual files.

# The purpose of this script is to make sequence alignment easier.

# This script was created by Alyssa Klein on 06/13/2019.
# This script was modified by Trent Balius in 2020.

# Define a main function that will contain two functions:
# The first will take in a file name (the one containing the *.pdb file names) and then read in each line of each pdb file
# The second will take the lines from each of the pdb files and will split each of the pdb entries into chains through the creation of files for each chain
# The result will be individual files for each chain for each pdb entry. Ligands should now be separated from the receptors.

# The `get_pdb_list()` function opens the .txt file with the names of the *.pdb files and reads in each line of each file, and the function ends with closing of the file(s).
def get_pdb_list():
        file_to_open = open("pdb_models.txt", "r") # Open the file containing the names of the files. Change to pdb_model_files.txt when model loop works
        pdbfilelist =[]
        for line in file_to_open: # Initiate a for loop to read in each line of the files in the .txt file that was opened in the previous line of code
                pdbfile = line.strip() # Declare a variable to strip each line of whitespace
                #print(pdbfile) # Print the pdbfile variable to make sure the file is being read in properly and that the whitespace was removed
                pdbfilelist.append(pdbfile)
        return pdbfilelist

# The `pdb_split_by_chain` function will take the lines of pdb files and split each pdb entry up into chains by creating an individual file for each chain 
def pdb_split_by_chain(pdbfile):
        print (pdbfile)
        #file_prefix = pdbfile.split('.')[0]
        file_prefix = pdbfile.split('/')[-1].split('.')[0]
        fh_pdb = open(pdbfile , "r") # open pdbfile (pdbfiles.txt with the whitespace stripped off) in read mode to read in lines of each pdb file
        #lines = fh_pdb.readlines()# Read in the lines of each *.pdb file; [0] can be used at end of line first to make sure script is working
        #print(lines) # Prints the lines of each entry. Just to make sure the script is working correctly/
        #fileh_pdb.close() # Close the pdbfile when all of the lines of each pdb file are read in
        #exit()
        dict_chain =  {} # Initialize an empty dictionary to eventually store the keys and values that correspond to the chain ID and the line(s) containing the chain 
        #for line in lines: # Initiate a for loop to look through the contents of each file to find the chain IDs
        for line in fh_pdb: # Initiate a for loop to look through the contents of each file to find the chain IDs
                if "ATOM" == line[0:4]:
                        chain = line[21] # Choose the character that denotes the chain designation in the line of the file beginning with "ATOM" (use 0-based counting)
                        #print line, chain
                        if not (chain in dict_chain): # If statement that basically says that if the chain ID letter is not yet in the dictionary, to initiate it
                                dict_chain[chain] = '' # This line creates value of the chain ID under the chain key
                        dict_chain[chain] = dict_chain[chain] + line # This adds the line where the chain ID was found to the dictioonary with the chain ID
                                #print(dict_chain[chain])        

        fh_pdb.close() # Close the pdbfile when all of the lines of each pdb file are read in
        for chain in dict_chain.keys(): # Initiate a second for loop to write the lines of the pdb files into separate chain files for each pdb code 
                print (file_prefix +"_" + chain + ".pdb")
                file = open(file_prefix +"_" + chain + ".pdb", "w") # Open a file corresponding to the pdbcode, the chain ID and a .pdb extension
                file.write(dict_chain[chain]) # Write the dict_chain[chain] value to the file created in the previous line of code
                file.close() # Close the file that was created and written to 
        
def main(): # Define a main function in order to call the other functions that have been created
       
        pdbs = get_pdb_list() # Set pdbs equal to the get_pdb_list() function so that its output can be used in the pdb_splt_by_chain_function

        for pdb in pdbs: # for loop to use the pdb_split_by_chain() function
           pdb_split_by_chain(pdb)


main()

                        
