#!/usr/bin/python

###############################################################################
###############################################################################
##                                                                           ##
## This python script interfaces with the MySQL database prot_db:            ##
## The prot_db database has the following tables:                            ##
##  (1) Prot_dock -- stores the prodeomic docking information,               ##
##      each attempted virtal screen will have an entry.                     ##
##      This table has the following elements:                               ##
##      (a) ID          (eg. 79)                  :: Entry Number.           ##
##      (b) Uniprot     (eg. P00533)              ::                         ##
##      (c) PDB_code    (eg. 1M17)                ::                         ##
##      (d) DOCK_site   (eg. 3)                   :: PDB may have more than  ##
##                                                :: than one posible sight. ##
##      (e) DOCK_prep   (falled, runing, not      ::                         ##
##                       trusted, successfull)    ::                         ##
##      (f) DOCK_status (NULL, falled, runing,    ::                         ##
##                       nottrusted, successfull) ::                         ##
##      (g) VS_ligand   (NULL, Chembl)            ::                         ##
##      (h) plversion   (eg. 5)                   :: pipeline version.       ##
##                                                                           ##
## Writen by Trent E. Balius, Shoichet Lab, UCSF.                            ##
##                                                                           ##
## Using http://zetcode.com/databases/mysqlpythontutorial/ as a reference.   ##
##                                                                           ##
## The perpose of this script is to create, add to,reduce, modify,           ## 
## and otherwise interface with the database prot_db.                        ##
##                                                                           ##
###############################################################################
###############################################################################

import MySQLdb as mdb
import sys


def creat_update_database(con):
  with con:
      
      cur = con.cursor()
      cur.execute("CREATE TABLE IF NOT EXISTS \
                   Prot_dock (\
                   Id INT PRIMARY KEY AUTO_INCREMENT,\
                   Uniprot  VARCHAR(25),\
                   PDB_code VARCHAR(5),\
                   DOCK_site VARCHAR(3),\
                   DOCK_prep VARCHAR(25),\
                   DOCK_status VARCHAR(25),\
                   VSligand VARCHAR(25),\
                   plversion VARCHAR(25))\
                  ")
      cur.execute("INSERT INTO Prot_dock VALUES ('1','P00533','1M17','3','nottrusted','nottrusted','Chembl','1')")

def main ():
  con = None
  
  try:
      con = mdb.connect('zincdb1', 'tbalius', 
          'lala', 'prot_db');

      cur = con.cursor()
      cur.execute("SELECT VERSION()")

      data = cur.fetchone()
    
      print "Database version : %s " % data
      creat_update_database(con)

  except mdb.Error, e:
  
      print "Error %d: %s" % (e.args[0],e.args[1])
      sys.exit(1)
    
  finally:    
      if con:    
          con.close()

main()
