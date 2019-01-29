
import sys
import math
import os.path

## 2014/12
## Writen by Trent Balius in the Shoichet Group
## reads in DOCK output "ExtractAll file".

#class dockdata:
#    def __init__(self, score, ligand_bind):
#        self.id    = int(id)
#        self.name  = name
#        self.score = float(score)

MIS_VAL = 100000.0
R       = 1.9872041*(10.0**(-3.0))
T       = 297.25

def read_Extract_file(infile,outfile):
     print file

     ## this funtion reads in the scores from the dock output
     file1 = open(infile,'r')
     file2 = open(outfile,'w')

     dic_zinc = {}
     dic_uniq_line = {}
     dic = {}

     dic_label = {}
     dic_label["2"] = "A"
     dic_label["3"] = "B"
     dic_label["4"] = "C"
     dic_label["5"] = "C"
     # dic_label[5] = "F" # F is the same loop as C but with on sidechain in alternative position,  we should treat as C
     file2.write("zincname,confA,confB,confC\n")


     # make a dictionary of zinc codes containing an array
     for line in file1:

        splitline = line.split()

        if (len(splitline) == 0):
           #print splitline 
           #print line
           continue

        #print splitline  
        #zinc = splitline[2]
        #rec_conf = splitline[3]
        zinc = splitline[2].split('.')[0]
        rec_conf_barcode = splitline[3]
        rec_conf_num = splitline[3].split('.')[1]
        rec_conf = dic_label[rec_conf_num]

        molnum = splitline[1]
        matchnum = splitline[9]
        energy =  float(splitline[21])
  
        # looks like some times the same pose (energy and loop pref) is written out more than once 
        # the following if statement will remove the redundance. 
        uniq_id = molnum+" "+zinc+" "+rec_conf_barcode+" "+matchnum+" "+str(energy)
        if uniq_id in dic_uniq_line:
           dic_uniq_line[uniq_id] = dic_uniq_line[uniq_id] + 1
           print line, dic_uniq_line[uniq_id]
           continue
        else:
           #print line
           dic_uniq_line[uniq_id]=1

        print rec_conf_barcode, rec_conf_num, rec_conf 
        if not (zinc in dic_zinc):
            dic_zinc[zinc] = []
        if not (zinc+rec_conf in dic):
            dic[zinc+rec_conf] = 1
        else:
            dic[zinc+rec_conf] = dic[zinc+rec_conf] + 1
            #continue
        occ    =  math.exp(-1.0 * energy / (R*T))
        dic_zinc[zinc].append([rec_conf, occ, rec_conf_barcode])
        print zinc, rec_conf, energy, occ

     keys = dic_zinc.keys()
     # loop over zinc codes in dictionary  
     for key in keys:
         tot = 0
         # make dictionary of all barcodes
         dic_barcode = {} #make a dictionary for each zinc code (molecule)
         for ele in dic_zinc[key]:
             barcode = ele[2]
             dic_barcode[barcode] = [0, 0.0, ""] # store a count and an energy 

         #calculate the total occupancy for each loop barcode
         # look at the top 10 and at lest one for all states
         count = 0
         for ele in dic_zinc[key]:
             conf = ele[0]
             occ = ele[1]
             barcode = ele[2]
             #if count > 9 and (dic_barcode[barcode][0] > 1):  
             #   continue
             dic_barcode[barcode][0] = dic_barcode[barcode][0]+1
             dic_barcode[barcode][1] = dic_barcode[barcode][1]+occ
             dic_barcode[barcode][2] = conf
             count = count+1
         # cal total occupancy

         print "number of state = " + str(len(dic_barcode.keys()))
         for barcode in dic_barcode.keys():
             tot = tot + dic_barcode[barcode][1]

         print "\n"+key+":"
         sort_occ = [0.0, 0.0, 0.0] # A,B,C
         for barcode in dic_barcode.keys():
             conf = dic_barcode[barcode][2]
             occ = dic_barcode[barcode][1]/tot
             if conf == "A":
                sort_occ[0] = sort_occ[0]+occ
             elif conf == "B":
                sort_occ[1] = sort_occ[1]+occ
             elif conf == "C":
                sort_occ[2] = sort_occ[2]+occ
             else:
                print "Error"
                exit(0)
             print conf + "    " + str(occ)

         #for ele in dic_zinc[key]:
         #    conf = ele[0]
         #    occ = ele[1]/tot
         #    if conf == "A":
         #       sort_occ[0] = occ
         #    elif conf == "B":
         #       sort_occ[1] = occ
         #    elif conf == "C":
         #       sort_occ[2] = occ
         #    else:
         #       print "Error"
         #       exit(0)
         #    print conf + "    " + str(occ)
         file2.write("%s,%f,%f,%f\n" % (key,sort_occ[0],sort_occ[1],sort_occ[2]))

     file1.close()
     file2.close()
     return 



def main():
  if len(sys.argv) != 3 : # if no input
     print "python process_extract_dock_occ.py extact_all.sort out" 
     print "len(sys.argv)  = " + str( len(sys.argv))
     return 

  inputfile     = sys.argv[1]  
  outputfile     = sys.argv[2]  
  read_Extract_file(inputfile,outputfile)
main()

