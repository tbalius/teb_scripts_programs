#! /usr/bin/python
import sys
import gzip

#f = gzip.open('/home/joe/file.txt.gz', 'rb')
#file_content = f.read()
#f.close()

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
def read_multiPDB_files_data(mPDB_decoy,mPDB_ligand):
    print "decoy file ="+mPDB_decoy
    print "ligand file ="+mPDB_ligand


    
    namesplit = mPDB_decoy.split('.') #split on '.'
    l = len(namesplit)
    print l
#    for i in range(l):
#        print str(i) + " : " + namesplit[i]
 

    print namesplit[l-1] + '== gz'
    if ( namesplit[l-1] == 'gz'):
       print "reading in  gziped file"
       file1 = gzip.open(mPDB_decoy,'r')
    elif (namesplit[l-1] == 'pdb'): 
       print "reading in multiPDB file"
       file1 = open(mPDB_decoy,'r')
    else: 
       print mPDB_decoy+"::wrong file formate"
   

    namesplit = mPDB_ligand.split('.') #split on '.'
    l = len(namesplit)

    print namesplit[l-1] + '== gz' 

    if ( namesplit[l-1] == 'gz'):
       print "reading in  gziped file"
       file2 = gzip.open(mPDB_ligand,'r')
    elif (namesplit[l-1] == 'pdb'):
       print "reading in multiPDB file"
       file2 = open(mPDB_ligand,'r')
    else:
       print mPDB_ligand+"::wrong file formate"



 
    ligand_info = []
    count_lig   = 0 
    count_true  = 0 
    count_false = 0 
    # put scores for all molecules in decoys in array
    #print str(mPDB_decoy)+"\n"
    lines  =  file1.readlines()
    
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 5):
            if (linesplit[1] == "Energy"):
                ligand_score = float(linesplit[4])
                ligand_bind  = int(0)#not known to binded
                ligand_data  = LIG_DATA(ligand_score,ligand_bind)
                ligand_info.append(ligand_data)
                count_lig = count_lig + 1
                count_false = count_false + 1

    del lines 
    # put scores for all molecules in ligands in array
    #file2 = open(mPDB_ligand,'r')
    lines  =  file2.readlines()
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 5):
            if (linesplit[1] == "Energy"):
                ligand_score = float(linesplit[4])
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
        print "  (1) multiPDB of decoys"
        print "  (2) multPDB file of known binders"
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
    list, num_false, num_true = read_multiPDB_files_data(decoy_file,ligand_file)

    print "Decoys:"+str(num_dec)+" vs. "+str(num_false)
    print "Actives:"+str(num_lig)+" vs. "+str(num_true)
    
    write_ROC(outputfile,list,num_dec, num_lig)
    
    
#################################################################################################################
#################################################################################################################
main()
