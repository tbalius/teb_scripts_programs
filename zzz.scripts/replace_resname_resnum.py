
import sys

def mod_res_pdb(rname,rnum,inpdb,outpdb):
    fhi = open(inpdb,'r')
    fho = open(outpdb,'w')
    for lineO in fhi:
        line = lineO.strip()
        lsize = len(line)
        if lsize < 4: 
            continue
        if line[0:4] != "ATOM": 
            continue
        lrname = line[17:20]
        lrnum = line[23:26]
        newline = line
        if (lrname != rname or lrnum != rnum):
             print(line)
             print(line[0:17]+rname+line[20:23]+'%3d'%(int(rnum))+line[26:lsize])
             newline = line[0:17]+rname+line[20:23]+'%3d'%(int(rnum))+line[26:lsize]
        fho.write(newline+'\n')
        #print(lrname)
        #print(lrnum)
        #exit()


def main():

    resname = sys.argv[1]
    resnum = sys.argv[2]
    pdbfile = sys.argv[3]
    output = sys.argv[4]
    mod_res_pdb(resname,resnum,pdbfile,output) 

main()

