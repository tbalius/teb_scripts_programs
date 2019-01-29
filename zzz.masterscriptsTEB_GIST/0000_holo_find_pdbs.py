import sys,urllib,urllib2, os




def download_pdbs(pwd, query_result, system, input_pdb):

	new_dir = pwd+system+"/"
	os.system("mkdir "+new_dir)
	os.chdir(new_dir)
	os.system("cp /mnt/nfs/work/rstein/RotationProjectDUDEGIST/"+input_pdb+"/rec.pdb .")

	pdb_list = []

	for pdb in query_result.split('\n'):
		if len(pdb) > 0:	
                       pdb = pdb.split(':')[0]
                       pdb_list.append(pdb)
                       url = 'http://www.rcsb.org/pdb/files/'+pdb+'.pdb1' # biological subunit
                       urllib.urlretrieve(url, pdb + ".pdb")
                       #file = pdb + ".pdb"
                       print pdb
	return(pdb_list)


def write_chimera(pdb_list):

	output = open("chimera.com",'w')
	
	pdb_dict = {}
	count = 1
	output.write("open rec.pdb\n")
	for pdb in pdb_list:
		pdb_dict[count] = pdb
		output.write("open "+pdb+".pdb\n")
		count += 1 

	output.write("mmaker #0 #1-"+str(count)+"\n")
	for i in range(1,count):
		pdb_out_name = pdb_dict[i]
                output.write("write format pdb "+str(i)+" "+pdb_out_name+"_holo_aligned.pdb\n")
	
	output.close()	
	#print(pdb_dict)
	os.system("/nfs/soft/chimera/current/bin/chimera --nogui chimera.com")

	

def query(queryText):

	url = 'http://www.rcsb.org/pdb/rest/search'
	req = urllib2.Request(url, data=queryText)
	f = urllib2.urlopen(req)
	result = f.read()
	if result:
		print "Found number of PDB entries:", result.count('\n')
	else:
		print "Failed to retrieve results"
	
	return result

def scrap_pdb_for_uniprot(pdbcode):

	url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + pdbcode
	
	webfile = urllib.urlopen(url)
	page    = webfile.read()
	webfile.close()
	  
	splitpage=page.split('\n')
	
	for line in splitpage:
		line1 = line.strip().split()
		if len(line1) == 2 and line1[0] == '<div' and line1[1][0:7] == 'id="ent':
			uniProt = line1[1].split('ity')[1]
			uniProt = uniProt.split('"')[0]
			print(uniProt)
			return uniProt


def query_uniprotinput(uniprotinput):

	queryText = """<orgPdbCompositeQuery version="1.0">
	    <resultCount>98</resultCount>
	    <queryId>8018CCDD</queryId>
	 <queryRefinement>
	  <queryRefinementLevel>0</queryRefinementLevel>
	  <orgPdbQuery>
	    <version>head</version>
	    <queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
	    <description>Simple query for a list of Uniprot Accession IDs: P00811</description>
	    <queryId>34A859DE</queryId>
	    <resultCount>98</resultCount>
	    <runtimeStart>2017-02-09T20:34:10Z</runtimeStart>
	    <runtimeMilliseconds>4</runtimeMilliseconds>
	    <accessionIdList>%s</accessionIdList>
	  </orgPdbQuery>
	 </queryRefinement>
	 <queryRefinement>
	  <queryRefinementLevel>1</queryRefinementLevel>
	  <conjunctionType>and</conjunctionType>
	  <orgPdbQuery>
	    <version>head</version>
	    <queryType>org.pdb.query.simple.NoLigandQuery</queryType>
	    <description>Ligand Search : Has free ligands=yes</description>
	    <queryId>4916EF31</queryId>
	    <resultCount>94463</resultCount>
	    <runtimeStart>2017-02-09T20:34:10Z</runtimeStart>
	    <runtimeMilliseconds>1621</runtimeMilliseconds>
	    <haveLigands>yes</haveLigands>
	  </orgPdbQuery>
	 </queryRefinement>
	</orgPdbCompositeQuery>
	""" % uniprotinput

	return(queryText)




def main():

	pwd = os.getcwd()+"/"

	input_pdb = sys.argv[1]
	system = sys.argv[2]

	uniprotinput = scrap_pdb_for_uniprot(input_pdb)

	print(uniprotinput)
	queryText = query_uniprotinput(uniprotinput)
	result = query(queryText)

	pdb_list = download_pdbs(pwd, result, system, input_pdb)
	write_chimera(pdb_list)

main()
