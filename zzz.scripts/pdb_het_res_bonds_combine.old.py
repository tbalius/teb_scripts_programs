#! /usr/bin/python
import sys

class PDB_atom_info:
    def __init__(self, chainid, resname, resnum, X, Y, Z, boolhet):
        self.chainid = chainid
        self.resname = resname
        self.resnum  = resnum
        self.X       = X
        self.Y       = Y
        self.Z       = Z
        self.boolhet = boolhet

    def __cmp__(self, other):
        return cmp(self.chainid, other.chainid)
# this defines a compares two LIG_DATA by comparing the two scores
# it is sorted in decinding order.
def byResId(x, y):
    str1 = x.resname + x.chainid + x.resnum
    str2 = y.resname + y.chainid + y.resnum
    return cmp(str1,str2)

#################################################################################################################
def id_close_atoms(pdb_file,pdb_out):
    
    file1 = open(pdb_file,'r')
   
    temp_atom_list  = []
    het_atom_list   = []
    stand_atom_list = []
    res_list        = []
 
    lines    = file1.readlines()
   
    file1.close()
 
    resstr_cur = ' '
    for line in lines:
         linesplit = line.split() #split on white space
         if (len(linesplit) >= 1):
           #if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
            if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):

                if (ok_residue(line[17:20])):
                   if (resstr_cur == ' '):
                       resstr_cur = line[17:26]
                   
                   if resstr_cur != line[17:26]:
                      resstr_cur = line[17:26]
                      res_list.append(temp_atom_list)
                      temp_atom_list = []

                   chainid = line[21]
                   resname = line[17:20]
                   resnum  = line[23:26]
                   #print line[30:38] + "...." + line[38:46] + "...." + line[46:54]
                   X       = float(line[30:38])
                   Y       = float(line[38:46])
                   Z       = float(line[46:54])
                   boolhet = (linesplit[0] == "HETATM")
                   #if (ok_residue(resname)): # do not include waters etc.
                   temp_atom_info = PDB_atom_info(chainid,resname,resnum,X,Y,Z,boolhet)
                   temp_atom_list.append(temp_atom_info)
                   if (boolhet):
                       het_atom_list.append(temp_atom_info)
                   else:
                       stand_atom_list.append(temp_atom_info)
            

   
    if (ok_residue(line[17:20])):
       if (resstr_cur == ' '):
           resstr_cur = line[17:26]
    
       if resstr_cur != line[17:26]:
          resstr_cur = line[17:26]
          res_list.append(temp_atom_list)
          temp_atom_list = []
             
    join_list       = [] # store what is conected to what
    ## if there is a atom within bond distance then make the same residue.
    if (len(res_list)>1):
        for i in range(1,len(res_list)):
            #print "compare " +  res_list[i-1][0].resname + "   " + res_list[i-1][0].resname
            if (dist(res_list[i-1],res_list[i],0.9,1.8)):
                print res_list[i][0].resname + res_list[i][0].resnum + res_list[i][0].chainid + " is connected to " + res_list[i-1][0].resname + res_list[i-1][0].resnum + res_list[i-1][0].chainid
                join_list.append(res_list[i-1][0].resname + res_list[i-1][0].resnum + res_list[i-1][0].chainid + " " + res_list[i][0].resname + res_list[i][0].resnum + res_list[i][0].chainid)
                #print "consider SKIPPING"
                #for atom in res_list[i]: 
                #    atom.chainid = res_list[i-1][0].chainid
                #    atom.resname = res_list[i-1][0].resname
                #    atom.resnum  = res_list[i-1][0].resnum 

    # this should check if there is a bond between protien atoms and ligand atoms
    if (dist(het_atom_list,stand_atom_list,0.9,1.8)):
        print "nonstandard conected to standard"
        #print "consider SKIPPING"
    else:
        print "nonstandard not conected to standard"

    # EXAMPLE
    ## join_list   ::   join_list2
    ##    1  2            1  2
    ##    3  4            3  4 5
    ##    4  5            6  7 8 9 10
    ##    6  7           11 12
    ##    7  8
    ##    8  9
    ##    9 10
    ##   11 12

    print join_list
    join_list2       = []
    if (len(join_list)>1):
       last = ''
       sub_list = [] # to store list of residue idenifiers
       for ele in join_list:
           split_ele = ele.split(' ')  # 2 indifiers
           if (last != split_ele[0]):
               if (len(sub_list) > 0):
                  #print sub_list
                  join_list2.append(sub_list)
               sub_list = [split_ele[0]]
               sub_list.append(split_ele[1])
           else:
               print sub_list
               sub_list.append(split_ele[1])
               last = split_ele[1]

       join_list2.append(sub_list)
       
    elif (len(join_list) == 1):
         print "I AM HERE"
         sub_list = join_list[0].split(' ')
         join_list2.append(sub_list)
    else:
        print "no modification"
        
    print join_list2
    
    file2 = open(pdb_out,'w')

    CM_num = 0  ## the number of combined ligands
    R_num  = 0  ## the number of combined ligands
    str_id_current = "" 
    #new_chainid = ""
    flag_frist = True
    print "I AM HERE"
    if (len(join_list2)>0):
        for line in lines:
             endofline = len(line)
             linesplit = line.split() #split on white space
             if (len(linesplit) >= 1):
               #if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                if (linesplit[0] == "ATOM" or linesplit[0] == "HETATM"):
                       chainid = line[21]
                       resname = line[17:20]
                       resnum  = line[23:26]

                       str_id = resname+resnum+chainid 

                       # Here I am keeping track of where i am in my list of resdidues to connect.
                       if (str_id_current != str_id): 
                           if not flag_frist:
                              R_num = R_num + 1

                              if R_num == len(join_list2[CM_num]):
                                 R_num = 0
                                 CM_num = CM_num + 1
                              if (CM_num >= len(join_list2)):
                                 R_num  = 0
                                 CM_num = 0 
                              print str(CM_num)+"::"+str(R_num)+"::"+str_id_current
                                  
                           flag_frist  = True

                       # Check if the the residue is the current selected residue from the combine list.
                       # if it is not then set then set it to the curent residue.
                       if join_list2[CM_num][R_num] != str_id_current:
                           str_id_current = join_list2[CM_num][R_num]
                           print str(CM_num)+"::"+str(R_num)+"::"+str_id_current
                           flag_frist  = True


                       if (str_id_current == str_id):
                           print str_id_current +"=="+ str_id
                           if flag_frist:
                               #new_resnum  = resnum 
                               #new_chainid = chainid
                               ##if (new_chainid == ""): # set to value if never asiged before
                               ##    new_chainid = chainid
                               flag_frist  = False

                           if CM_num < 10:
                              new_resname = 'CM'+str(CM_num) 
                              new_resnum  = resnum 
                              new_chainid = chainid
                           elif CM_num < 100:
                              new_resneme = 'C'+str(CM_num)
                              new_resnum  = resnum 
                              new_chainid = chainid
                           else: 
                              print "CM_num > 100" 
                              exit(0)
                           file2.write(line[0:17]+new_resname+' '+new_chainid+' '+new_resnum + line[26:endofline])
                       else:
                           file2.write(line)
                           


    print "done"
    return 

#################################################################################################################
#################################################################################################################
def dist(res1,res2,di,dj):

    # if both are not het atoms then return false
    # as long as on is het then precede
    if  ( not res1[0].boolhet and  not res2[0].boolhet):
        return False

    count = 0 # count the number of contact points 
    for atom1 in res1:
        for atom2 in res2:
            di2       = di**2
            dj2       = dj**2

            X_diff_2 = (atom1.X - atom2.X)**2.0
            Y_diff_2 = (atom1.Y - atom2.Y)**2.0
            Z_diff_2 = (atom1.Z - atom2.Z)**2.0
            dist2    = (X_diff_2 + Y_diff_2 + Z_diff_2)

            #if (dist2 > di2 and dist2 < dj2):
            if ( dist2 < dj2):
                #print "Atoms are close" + " dist2 = " + str(dist2)
                print "likely bond::" + atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
                count =  count + 1

            if (dist2 < di2):
                print "Warning: Atoms are too close," + " dist2 = " + str(dist2)
                #print atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
                #print str(atom1.X) +" "+ str(atom1.Y) +" "+ str(atom1.Z) + "---" + str(atom2.X) +" "+ str(atom2.Y) +" "+ str(atom2.Z)
                #return False

    if (count > 3):
       print "Too meny close atoms, count = " + str(count)
       print atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
       print "This most likely is because there is duel occupence"
       return False

    if (count > 0 and count < 4):
        return True
    
    #print "how did i get here?"
    #print atom1.resname + atom1.resnum + atom1.chainid + "---" + atom2.resname + atom2.resnum + atom2.chainid
    return False
#################################################################################################################
#################################################################################################################
def ok_residue(resname):
    # read in solvent residue types from file.

    if (resname == 'HOH'):
        return False
    if (resname == ' NA'):
        return False

    return True
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 3: # if no input
        print "This function takes as input a pdb file"
        print "id connected residues"
        print "writes a modified pdbfile with hetatoms combinded into redidue if short bond."
        print len(sys.argv)
        return
    
    pdb_file  = sys.argv[1]
    pdb_out   = sys.argv[2]

    id_close_atoms(pdb_file,pdb_out)
    
    
#################################################################################################################
#################################################################################################################
main()
