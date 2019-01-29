import sys
import scrape_uniprot_for_name as sufn 

if ( len(sys.argv) != 2):
    print "needs a uniprot code file list"
    exit()

query = sys.argv[1]
d = sufn.get_query(query)
d = d.replace('{',' ').replace('}',' ')
print d

