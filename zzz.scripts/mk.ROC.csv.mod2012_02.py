#! /usr/bin/python
import sys

class LIG_DATA:
    def __init__(self, score, ligand_bind):
        self.score, self.ligand_bind = score, ligand_bind
    def __cmp__(self, other):
        return cmp(self.score, other.score)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byScore(x, y):
    return cmp(x.score, y.score)
        

#################################################################################################################
def read_MOL2_files_data(MOL2_decoy,MOL2_ligand):
    file1 = open(MOL2_decoy,'r')
    
    ligand_info = []
    count_lig   = 0 
    count_true  = 0 
    count_false = 0 
    # put scores for all molecules in decoys in array
    print str(MOL2_decoy)+"\n"
    lines  =  file1.readlines()
    
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 3):
            if (linesplit[2] == "Score:"):
                ligand_score = float(linesplit[3])
                ligand_bind  = int(0)#not known to binded
                ligand_data  = LIG_DATA(ligand_score,ligand_bind)
                ligand_info.append(ligand_data)
                count_lig = count_lig + 1
                count_false = count_false + 1

    del lines 
    # put scores for all molecules in ligands in array
    file2 = open(MOL2_ligand,'r')
    lines  =  file2.readlines()
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 3):
            if (linesplit[2] == "Score:"):
                ligand_score = float(linesplit[3])
                ligand_bind  = int(1)# known to binded
                ligand_data  = LIG_DATA(ligand_score,ligand_bind)
                ligand_info.append(ligand_data)
                count_lig = count_lig + 1
                count_true = count_true + 1

    ligand_info.sort(byScore)
    return ligand_info, count_false, count_true
#################################################################################################################
def write_ROC(OUTPUTFILE,list,num_false,num_true):
    ## write a csv file the has 3 columns
    ## column1 is the size kept 
    ## column2 TP/T
    ## column3 FP/F
    file = open(OUTPUTFILE,'write')
    file.write("NUM_kept,TPRate,FPRate\n" )
    true_positive  = 0
    false_positive = 0
    for i in range(len(list)):
        if (list[i].ligand_bind == 1):
            true_positive = true_positive + 1
        elif (list[i].ligand_bind == 0):
             false_positive = false_positive + 1
        frac_true  = float(true_positive)/float(num_true)
        frac_false = float(false_positive)/float(num_false)
        file.write(str(i+1) + "," + str(frac_true) + "," + str(frac_false) + "\n" )

#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 6: # if no input
        print "This function take input files names produced by DOCK6:"
        print "  (1) mol2 of decoys"
        print "  (2) mol2 file of known binders"
        print "  (3) # of decoys docked"
        print "  (4) # of known binders docked"
        print "  (5) CSV file for a ROC curve"
        print len(sys.argv)
        return
    
    decoy_file  = sys.argv[1]
    ligand_file = sys.argv[2]
    num_dec     = int(sys.argv[3])
    num_lig     = int(sys.argv[4])
    outputfile  = sys.argv[5]
    list, num_false, num_true = read_MOL2_files_data(decoy_file,ligand_file)

    print "Decoys:"+str(num_dec)+" vs. "+str(num_false)
    print "Actives:"+str(num_lig)+" vs. "+str(num_true)
    
    write_ROC(outputfile,list,num_dec, num_lig)
    
    
#################################################################################################################
#################################################################################################################
main()
