
import sys, os

# written by Trent Balius, FNLCR, 2022/08/26.

# This script reads in a bunch of mol2 files and combines them into one files
# so that the file is not too big we use a score cut off to only retain molecules about the cutoff
# we also sort the mol2 by energy.
# we write out two files:
# i. one file with all poses below the cutoff (not sorted) and 
# ii. one file that is sorted and with just the miniumn energy pose for each zincid (remove duplicates) 

def open_dock_mol2(list_text,filenamein,fho,fhdo,score_txt,cutoff):

    if not os.path.exists(filenamein): 
         print(filenamein+" does not exist")
         return

    fhi = open(filenamein,'r') # input file handel

    score = 100000.0
    moltext = ""
    name = "None"
    #new_mol   = False
    flag_head = False # in the header section
    flag_mol  = False # in the molecule info section
    flag_atom = False # in the atom section
    flag_bond = False # in the bond section
    flag_res  = False # in the resdiue section
    flag_sol  = False # in the solvation section # not always printed
    for line in fhi:
        splitline = line.split()
        if "#####" in line: 
                if flag_res or flag_sol: 
                     if score <= cutoff: # only keep things that are less than the cutoff
                         list_text.append([score,name, moltext])
                         fho.write(moltext)
                         fhdo.write("%s,%s\n"%(name,filenamein))
                     moltext = ""
                     score = 100000.0
                     name = "None"
                flag_head = True
                flag_mol  = False
                flag_atom = False
                flag_bond = False
                flag_res  = False
                flag_sol  = False

        if "@<TRIPOS>MOLECULE" in line: 
                flag_head = False 
                flag_mol  = True 
                flag_atom = False 
                flag_bond = False 
                flag_res  = False 
                flag_sol  = False 

        if "@<TRIPOS>ATOM" in line:
                flag_head = False
                flag_mol  = False
                flag_atom = True
                flag_bond = False
                flag_res  = False
                flag_sol  = False

        if "@<TRIPOS>BOND" in line:
                flag_head = False
                flag_mol  = False
                flag_atom = False
                flag_bond = True
                flag_res  = False
                flag_sol  = False

        if "@<TRIPOS>SUBSTRUCTURE" in line:
                flag_head = False
                flag_mol  = False
                flag_atom = False
                flag_bond = False
                flag_res  = True
                flag_sol  = False
        if flag_head:
           if len(splitline) < 3: 
              continue
           if splitline[1] == "Name:":
              name = splitline[2]
           if splitline[1] == score_txt:
              score = float(splitline[2])
              #print (name, score)
        moltext = moltext+line
    # output the last pose.
    if score <= cutoff: # only keep things that are less than the cutoff
        list_text.append([score,name, moltext])
        fho.write(moltext)
        fhdo.write("%s,%s\n"%(name,filenamein))
    fhi.close()

def mySortFunc(e):
  return e[0]

# if the name has a dot take the part before the dot.  
# We only want to keep one. 
# e.g. Lig001.1, Lig001.2, Lig001.3 will be treated as the same ligand Lig001.  
def splitdot(n):
      split_dot_name = n.split('.')
      if len(split_dot_name) > 2: 
          print("Warning... name has more than one dot: %s"%n) 
      namep = split_dot_name[0]
      return namep
    
def sort_mol2(list_mol2_s_t,fho):
    dict_zinc = {}
    list_mol2_s_t.sort(key=mySortFunc) 
    for ele in list_mol2_s_t:
         score = ele[0]
         #name = ele[1]
         name = splitdot(ele[1])
         text = ele[2]
         #print (name, score)
         if name in dict_zinc: 
            #print ("name in list")
            continue
         dict_zinc[name] = 1 
         fho.write(text)

def write_csv(list_mol2_s_t,fho):
    dict_zinc = {}
    list_mol2_s_t.sort(key=mySortFunc)
    frist = True
    for ele in list_mol2_s_t:
         score = ele[0]
         #name = ele[1]
         name = splitdot(ele[1])
         text = ele[2]
         #print (name, score)
         if name in dict_zinc:
            #print ("name in list")
            continue
         head = ''
         csvline = ''
         comma = False
         for line in text.split('\n'):
             if '###' in line:
                 split_line = line.split()
                 if (comma):
                     head = head + ','
                     csvline = csvline + ','
                 else: 
                     comma = True
                 head = head+ split_line[1]
                 csvline = csvline + split_line[2]
         if (frist):
             #print (head)
             fho.write(head+'\n')
         #print (csvline) 
         fho.write(csvline+'\n')
         frist = False    
         dict_zinc[name] = 1



def main():    
   list_mol2 = []

   print("syntax: python make_combined_mol2_file.py dirpath1 mol2name score_txt1\n example:  python make_combined_mol2_file.py mol2listfile Chemgrid_Score: -50.0")

   filemol2list   = sys.argv[1]
   score_txt1 = sys.argv[2]
   cutoff     = float(sys.argv[3])

   print("filemol2list = %s"%filemol2list)
   print("score_txt1 = %s"%score_txt1)
   print("cutoff = %f"%cutoff)
   
   if (score_txt1 != "Chemgrid_Score:" or score_txt1 != "Grid_Score:" or score_txt1 != "Descriptor_Score:"):
       print ("score_txt1 must be Chemgrid_Score: or Grid_Score: or Descriptor_Score:")
       exit

   filename2 = "poses.threshold.mol2"
   filename3 = "poses.sort.uniq.mol2"
   filename4 = "poses.sort.uniq.csv"
   filename5 = "poses.threshold.dir.csv"
   
   
   #openhandel = os.popen('ls %s/*/%s'%(dirpath1,mol2name))
   fhi = open(filemol2list)
   files = fhi.readlines()
   fhi.close()
   
   list_mol2_score_text = []
   fho = open(filename2,'w')
   fhdo = open(filename5,'w')
   
   for line in files:
       filename1 = line.strip()
       open_dock_mol2(list_mol2_score_text,filename1,fho,fhdo,score_txt1,cutoff)
   
   fho.close()
   fhdo.close()
   fho = open(filename3,'w')
   sort_mol2(list_mol2_score_text,fho)
   fho.close()
   #fho = open(filename3+'.csv','w')
   fho = open(filename4,'w')
   write_csv(list_mol2_score_text,fho)
   fho.close()
   
main()
