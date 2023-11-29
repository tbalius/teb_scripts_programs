import sys
import pdb_lib
import copy

def add_ACE(pdb_mol,resid,pdb_mol_new):

    ##              C (ACE )
    ##     vec2    ^
    ##            /  vec3
    ##   CA --> N
    ##   ^
    ##  /  vec 1
    ## C 
    ## 
    ##  vec3 ~= vec1  so a good guess for N = C + vec1 

    #resdiue = pdb_mol[resid]

    flag_past = False
    
    #print (resid)
    for i in range(len(pdb_mol)):
        if (int(pdb_mol[i].resnum)  == int(resid)) : 
             print (pdb_mol[i].atomname, pdb_mol[i].atomnum)
             if (pdb_mol[i].atomname == " N  "): 
                atomN=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomN)
             if (pdb_mol[i].atomname == " C  "): 
                atomC=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomC)
             if (pdb_mol[i].atomname == " CA "): 
                atomCA=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomCA)
    vec1 = [atomCA[0]-atomC[0],atomCA[1]-atomC[1],atomCA[2]-atomC[2]]
    vec2 = [atomN[0]-atomCA[0],atomN[1]-atomCA[1],atomN[2]-atomCA[2]]

    ACE = [atomN[0]+vec1[0],atomN[1]+vec1[1],atomN[2]+vec1[2]]
    print (ACE)

    #pdb_mol_new = []
    old = pdb_mol[0]
    for i in range(len(pdb_mol)):
        if (int(pdb_mol[i].resnum) > (resid-1) and not flag_past):
            print(i,"add ACE")
            flag_past = True 
            temp = copy.copy(old)
            temp.X = ACE[0]
            temp.Y = ACE[1]
            temp.Z = ACE[2]
            temp.atomname = ' C  '
            temp.resname =  'ACE'
            #temp.resnum =  str(int(temp.resnum) + 1)
            temp.resnum =  str(resid-1)
            pdb_mol_new.append(temp)
            
        pdb_mol_new.append(pdb_mol[i])
        old = pdb_mol[i]
                #print (atomN)
        #pdb_mol[i].chainid = new_name;
    if (not flag_past):
        print(i,"add ACE")
        flag_past = True
        temp = copy.copy(old)
        temp.X = ACE[0]
        temp.Y = ACE[1]
        temp.Z = ACE[2]
        temp.atomname = ' C  '
        temp.resname =  'ACE'
        #temp.resnum =  str(int(temp.resnum) + 1)
        temp.resnum =  str(resid-1)
        pdb_mol_new.append(temp)


def dot(v,u):

   if (len(v) !=len(u)):
       print ("error")
       exit()
   val = 0
   for i in range(len(v)):
       val = val + v[i]*u[i]
   return val

def proj(v,u,su):
   # project v onto u.  
   if (len(v) !=len(u)):
       print ("error")
       exit()
   #su = []
   s = dot(v,u)/dot(u,u)
   for i in range(len(v)):
       su.append(0.0)
       su[i] = s*u[i]

def add_NME(pdb_mol,resid,pdb_mol_new):
    print("IN add_NME")
    ##              N (NME)
    ##       v1    ^
    ##            /  v3
    ##   CA --> C
    ##            \
    ##         v2  v
    ##              O
    ## 
    ##         o 
    ##        ^ | v4
    ##   v2  /  v
    ##      o-->o
    ##        v1*
    ##
    ##  v1* = proj(v2,v1) 
    ##  v4 = v1*-v2,  so a good guess for N = C + v1* + v4 =  C + 2v1* - v2

    flag_past = False
    #pdb_mol_new = []
    #resdiue = pdb_mol[resid]
    
    print (resid)
    for i in range(len(pdb_mol)):
        #print (pdb_mol[i].resnum)
        #exit()
        if (int(pdb_mol[i].resnum)  == int(resid)) :
             print (pdb_mol[i].atomname, pdb_mol[i].atomnum)
             if (pdb_mol[i].atomname == " O  "):
                atomO=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomO)
             if (pdb_mol[i].atomname == " C  "):
                atomC=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomC)
             if (pdb_mol[i].atomname == " CA "):
                atomCA=[pdb_mol[i].X, pdb_mol[i].Y, pdb_mol[i].Z]
                print (atomCA)
    v1 = [atomCA[0]-atomC[0],atomCA[1]-atomC[1],atomCA[2]-atomC[2]]
    v2 = [atomO[0]-atomC[0], atomO[1]-atomC[1], atomO[2]-atomC[2]]
    v1s = [] # s == star
    proj(v2,v1,v1s)
    print(len(v1s))
    NME = [atomC[0]+2.0*v1s[0]-v2[0],atomC[1]+2.0*v1s[1]-v2[1],atomC[2]+2.0*v1s[2]-v2[2]]
    print (NME)

    old = pdb_mol[0]
    for i in range(len(pdb_mol)):
        if (int(pdb_mol[i].resnum) > resid and not flag_past):
            print(i,"add NME")
            flag_past = True
            temp = copy.copy(old)
            temp.X = NME[0]
            temp.Y = NME[1]
            temp.Z = NME[2]
            temp.atomname = ' N  '
            temp.resname =  'NME'
            temp.resnum =  str(int(temp.resnum) + 1)
            pdb_mol_new.append(temp)
            #break

        #if ((len(pdb_mol)+1) == i): 
        #    break 
        pdb_mol_new.append(pdb_mol[i])
        old = pdb_mol[i]
    if (not flag_past):
        print(i,"add NME")
        flag_past = True
        temp = copy.copy(old)
        temp.X = NME[0]
        temp.Y = NME[1]
        temp.Z = NME[2]
        temp.atomname = ' N  '
        temp.resname =  'NME'
        temp.resnum =  str(int(temp.resnum) + 1)
        pdb_mol_new.append(temp)



def main():
   filename = sys.argv[1]
   #num      = int(sys.argv[2])
   #type_ter = sys.argv[3]     
   #which = int(sys.argv[4]) # wich chain/portion of protein,  protein is devied up by TERs and ENDs.  
   fileprefix = sys.argv[2]
   #if (type_ter != "N" and type_ter != "C"): 
   #    print("%s is not valid choise. "%type_ter)
   #    print("must be N or C, ACE will be add if N-terminal and NME will be added if C-terninal")
   
   pdbchains = pdb_lib.read_pdb(filename) 
   pdbchains_new = []
   print (len(pdbchains))
   for c in pdbchains:
       new = []
       new2 = []
       print(len(c))
       if len(c) == 0: 
          continue
       start_num = int(c[0].resnum)
       stop_num = int(c[len(c)-1].resnum)
       print(c[0].chainid,start_num,c[len(c)-1].chainid,stop_num)
       #print(c[0].chainid)
       #print(c[len(c)-1].chainid)
       if (c[0].boolhet):
          print(" \n\n skip...\n\n")
          pdbchains_new.append(c)
          continue
       #add_NME(c,start_num,new)
       #add_ACE(new,stop_num,new2)
       add_ACE(c,start_num,new)
       add_NME(new,stop_num,new2)
       pdbchains_new.append(new2)
#   count = 1
#   cat_chains = []
#   for pdbmol in pdbchains: 
#       replace_chain_name(pdbmol,' ')
#       append_chain(pdbmol,cat_chains)
   pdb_lib.output_pdbchains(pdbchains_new,'%s.pdb'%(fileprefix)) 
main()
