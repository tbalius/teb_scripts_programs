
import sys

## this script will get a sequence from the pdb.  

pdbfile = sys.argv[1]
#code = '1qg8' 
## make alignment file
#file = open(code+'.pdb')
file = open(pdbfile,'r')

dic_res = {}
dic_res['ALA'] =  'A'
dic_res['ARG'] =  'R'
dic_res['ASN'] =  'N'
dic_res['ASP'] =  'D'
dic_res['CYS'] =  'C'
dic_res['GLU'] =  'E'
dic_res['GLN'] =  'Q'
dic_res['GLY'] =  'G'
dic_res['HIS'] =  'H'
dic_res['ILE'] =  'I'
dic_res['LEU'] =  'L'
dic_res['LYS'] =  'K'
dic_res['MET'] =  'M'
dic_res['PHE'] =  'F'
dic_res['PRO'] =  'P'
dic_res['SER'] =  'S'
dic_res['THR'] =  'T'
dic_res['TRP'] =  'W'
dic_res['TYR'] =  'Y'
dic_res['VAL'] =  'V'

residue_list = ''
residue_list_seq = ''

resido   = '' 
resnameo = ''
chaino   = ''

chain_seq_o   = ''
chain_seq     = ''

count     = 0
count_seq = 0

for line in file:
    if line[0:10] == 'REMARK 465': 
        print line.replace('\n',' ')
    elif line[0:6] == 'SEQRES': 
        print line.replace('\n',' ')
        splitline = line.split()
        chain_seq = splitline[2]
        print chain_seq  
        if chain_seq != chain_seq_o: 
            residue_list_seq = residue_list_seq + '\nseq chian ' + chain_seq + ':\n'
            chain_seq_o = chain_seq

        for i in range(4,len(splitline)):
            residue_list_seq = residue_list_seq + dic_res[splitline[i]]
            count_seq = count_seq + 1
            if count_seq == 75:
               residue_list_seq = residue_list_seq + '\n'
               count_seq = 0

    elif line[0:6] == 'ATOM  ': 
        resid   = line[23:27] 
        resname = line[17:20]
        chain   = line[21:23] 
        #print resid, resname, chain
        if chain != chaino:
           residue_list = residue_list + '\nchian ' + chain + ':\n'
        if (resido !='' and (int(resid)-int(resido)) > 1):
            for i in range(0,int(resid) - int(resido)-1):
               residue_list = residue_list +'-'  
               count = count+1
        if resid != resido or resname != resnameo:
           residue_list = residue_list + dic_res[resname]
           count = count+1
        if count == 75:
           residue_list = residue_list + '\n'
           count = 0 

        resido   = resid 
        resnameo = resname
        chaino   = chain

print residue_list_seq
print residue_list 

