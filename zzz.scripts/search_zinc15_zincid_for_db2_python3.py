import requests
import os,sys
#import wget

def main():

#  zindid = 'ZINC000001546066'
 filename = sys.argv[1]
 print ('filename=%s'%filename)
 fh = open(filename,'r')
 for idline in fh:
 #for zincid in fh:
    zincid = idline.strip()
    pwd = os.popen('pwd').readlines()[0].strip()
    os.mkdir(pwd+'/'+ zincid)
    #search_url = 'http://zinc15.docking.org/substances/ZINC000001546066/'
    #search_url = 'http://zinc15.docking.org/substances/'+zindid+'/'
    search_url = 'https://zinc20.docking.org/substances/'+zincid+'/protomers.txt?count=all'
    response = requests.get(search_url)
    response_string =''
    for line in response:
        decodeline = line.decode('UTF-8')
        response_string = response_string + decodeline 
    #.split('\n')
    #for line in response.content:
    for line in response_string.split('\n'):
        #decodeline = line.decode('UTF-8')
        #strline = str(decodeline).strip()
        strline = str(line).strip()
        print (strline.split('\t'))
        protid = strline.split('\t')[0] 
        num1 = protid[-6:-4]
        num2 = protid[-4:-2]
        #num3 = protid[-2]+protid[-1]
        num3 = protid[len(protid)-2:len(protid)]
        #http://files.docking.org/protomers/90/85/10/385908510.db2.gz
        proturl = 'http://files.docking.org/protomers/%s/%s/%s/%s.db2.gz'%(num1,num2,num3,protid)
        print(proturl)
        #if "protomers" in strline and "db2.gz" in strline: 
        #    proturl = strline.split('"')[1]
        #    print(proturl)
            #db2response = requests.get(proturl)
            #fh = open("db2file.db2.gz", 'w')
            #fh.write(db2response.text)
            #fh.write(str(db2response.content))
            #fh.close()
            #wget.download(proturl)
        #os.system('mkdir '+pwd+'/'+ zincid)
        os.chdir(pwd+'/'+ zincid)
        os.system('wget '+proturl )
        os.chdir(pwd)
            

main()
