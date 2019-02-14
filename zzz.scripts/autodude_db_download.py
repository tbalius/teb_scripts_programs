
# Written by Trent E. Balius, B. Shoichet Lab at UCSF
# this get the database from the autodude webpage

import sys, os
import urllib

system = 'abl1'
url = 'http://autodude.docking.org/dude_e_db2/'

print "url = " + url

#page=requests.get(url)

webfile = urllib.urlopen(url)
page    = webfile.read()
webfile.close()

splitpage=page.split('\n')

for line in splitpage:
   if system in line: 
      file = line.replace('"',' ').split()[2]
      print url+file
      urllib.urlretrieve(url+file,file)

      exit()
