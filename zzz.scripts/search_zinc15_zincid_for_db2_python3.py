import requests
import os
#import wget

def main():

  zindid = 'ZINC000001546066'
  #search_url = 'http://zinc15.docking.org/substances/ZINC000001546066/'
  search_url = 'http://zinc15.docking.org/substances/'+zindid+'/'
  response = requests.get(search_url)
  #for line in response.content:
  for line in response:
      strline = str(line)
      #strline = line
      if "protomers" in strline and "db2.gz" in strline: 
          proturl = strline.split('"')[1]
          print(proturl)
          #db2response = requests.get(proturl)
          #fh = open("db2file.db2.gz", 'w')
          #fh.write(db2response.text)
          #fh.write(str(db2response.content))
          #fh.close()
          #wget.download(proturl)
          pwd = os.popen('pwd').readlines()[0]
          os.system('mkdir '+pwd+'/'+ zindid)
          os.system('wget '+proturl )
          

main()
