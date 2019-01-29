#! /usr/bin/python
import sys
#import gzip
import commands

## This script will split the combine.score file into 2 files: active.score and decoy.score
## The broken molecules are filtered out.

#################################################################################################################
def StrOnList(string1,list):

    if len(list) == 0:
       print "Warning: list is empty"
       return False

    for string2 in list:
        #print string1 + '==' + string2
        if (string1 == string2):
           print string1 + '==' + string2
           return True
    return False


#################################################################################################################
def convert_list_ChEMBLEtoZINC(list):

    new_list = []
    for ele in list:
         new_ele_list = convertChEMBLEtoZINC(ele)

         if (len(new_ele_list) == 1):
             new_ele = new_ele_list[0]
             if (new_ele == ''): 
                continue
             new_list.append(new_ele)
         if (len(new_ele_list) > 1):
             for new_ele in new_ele_list:
                 new_list.append(new_ele)

    return new_list
    

#################################################################################################################
def convertChEMBLEtoZINC(string):
    ## this function will return a list of strings

    #SELECT sub_id_fk AS sub_id FROM catalog_item AS ci INNER JOIN catalog AS c ON ci.cat_id_fk=c.cat_id WHERE c.short_name='chembl15' AND ci.supplier_code='CHEMBL25';
    #commands.getoutput('ls /bin/ls')

    new_string_list = []

    new_string = commands.getoutput( 'echo "SELECT sub_id_fk AS sub_id FROM catalog_item AS ci INNER JOIN catalog AS c ON ci.cat_id_fk=c.cat_id WHERE c.short_name=\'chembl14\' AND ci.supplier_code=\''+string+'\'" |  mysql -u tbalius -plala -h zincdb1 zinc8 ' )
    split_new_string = new_string.split('\n')

    ## a ChEMBL14 id might have more than one zinc id
    if len(split_new_string) >= 3: 
        print "Warning: ChEMBL14 id has more than one zinc id"
        print len(split_new_string), string , split_new_string
        #exit()
    elif len(split_new_string) == 1:
        print "Warning: ChEMBL14 id has no zinc id"
        print len(split_new_string), string , split_new_string
        return ''
    elif len(split_new_string) == 0: 
        print "Error: len(split_new_string) == 0"
        exit()

    for i in range(1,len(split_new_string)):
        if (int(split_new_string[i])<10):
            fill = '0000000'
        elif (int(split_new_string[i])<100):
            fill = '000000'
        elif (int(split_new_string[i])<1000):
            fill = '00000'
        elif (int(split_new_string[i])<10000):
            fill = '0000'
        elif (int(split_new_string[i])<100000):
            fill = '000'
        elif (int(split_new_string[i])<1000000):
#                                    C42808294
            fill = '00'
        elif (int(split_new_string[i])<10000000):
#                                     C42808294
            fill = '0'
        elif (int(split_new_string[i])<100000000):
#                                     C42808294
            fill = ''
        if (int(split_new_string[i])>=100000000):
           print "Error: int to big"
           exit()
       
        new_string_list.append('C' +fill+ split_new_string[i])

    #print string , new_string_list

    return new_string_list


#################################################################################################################
def read_write_combine(combinefile,activefile,brokenfile):
    print "combine file ="+combinefile
    print "active file ="+activefile
    print "broken mol file ="+brokenfile

    file1 = open(combinefile,'r')
    file2 = open(activefile,'r')
    fileb = open(brokenfile,'r')
    file3 = open('active.score','w')
    file4 = open('decoy.score','w')


    lines  =  fileb.readlines()
    if (len(lines) == 0):
        print brokenfile+ " is empty."
        exit()
    brokenlist = []
    for line in lines:
        brokenlist.append(line.strip())
    #print brokenlist
    #exit()
    if len(brokenlist) == 0:
        print " Warning: something might be wrong with "+ brokenfile


    lines  =  file2.readlines()
    if (len(lines) == 0): 
        print activefile+ " is empty."
        exit()
    elif (len(lines)>1):
        print activefile+ " should only have one entree"
        exit()
    #print lines[0].split(';')[2]
    list = lines[0].split(';')[2].split(':') 
    if len(list) == 0: 
        print " something is wrong with "+ activefile 
        exit()

    list = convert_list_ChEMBLEtoZINC(list)
    
 
    lines  =  file1.readlines()
    if (len(lines) == 0):
        print combinefile+ " is empty."
        exit()

    if (len(brokenlist) == 0):
       print "brokenlist is empty" 
       exit()
    if (len(list) == 0):
       print "list is empty"
       exit()

    for line in lines:
         #splitline = line.split(' ')
         splitline = line.split()
         name = splitline[0]
         if (StrOnList(name, brokenlist)):
             print "WARNING::" + name + "is broken"
             continue
         if (StrOnList(name, list)):
            file3.write(line)
         else:
            file4.write(line)
    file1.close()
    file2.close()
    fileb.close()
    file3.close()
    file4.close()

    return 
#################################################################################################################
#################################################################################################################
def main():
    if len(sys.argv) != 4: # if no input
        print "This Script reads in:"
        print "  (1) combined file (produced by MUD tool combine.py)"
        print "  (2) list of active molecules in SEA set formate"
        print "  (3) list of broken molecules"
        print "This script will produce 2 files active and decoys combine.score files" 
        print len(sys.argv)
        return
    
    inputfile   = sys.argv[1]
    activefile  = sys.argv[2]
    brokenMolFile  = sys.argv[3]
    read_write_combine(inputfile,activefile,brokenMolFile)
    
    
#################################################################################################################
#################################################################################################################
main()
