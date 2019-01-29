
## Trent Balius, Shoichet group, UCSF, 2014.08.08


# this make a graph of the ligands using graphviz. 

#import urllib, urllib2, math
#import scrape_pdb_for_uniprot as spfu
#import scrape_pdb_for_lig_mod as spfl
#import scrape_zinc_zincid as szzi
#import tanimoto_cal_axon as tancal

from graphviz import Digraph

#dot  #doctest: +ELLIPSIS
#Add nodes and edges:





print " stuff that matters::::::::::"

filein = open("uniprot_lig_tanamoto_flush.txt",'r')
fileout = open("uniprot_lig_tanamoto_mwdiff_formula_diff.txt",'w')

lig_dic  = {}
#count = 0
fcount = 1
uniprot_old = ''
for line in filein:

    if "This" in line: 
        continue

    #if count == 10: 
    #   exit()
    #count = count+1
  
    print line
    splitline = line.split()

    uniprot = splitline[0].strip(',')
    lig1 = splitline[2].strip(',')
    lig2 = splitline[3].strip(',')

    if (uniprot != uniprot_old):
        if uniprot_old != '':
            print dot_edges
            #dot.edges(dot_edges)
            #dot.edge('B', 'L', constraint='false')
            print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
            dot.render( uniprot_old+'.gv', view=True)
            print "stop " + uniprot_old
            #exit()
        print "start " + uniprot_old
        dot = Digraph(comment='Ligands for '+uniprot)
        lig_dic  = {}
        dot_edges = []
        count = 0
        #fcount = 1
        uniprot_old = uniprot


    #if (count > 8):
    #     continue

    print count, uniprot, lig1, lig2


    if not (lig1 in lig_dic):
         dot.node(str(count), lig1)
         lig_dic[lig1] = count
         count = count + 1
    if not (lig2 in lig_dic):
         dot.node(str(count), lig2)
         lig_dic[lig2] = count
         count = count + 1

    #dot_edges.append(str(lig_dic[lig1])+str(lig_dic[lig2]))
    #dot_edges.append(str(lig_dic[lig2])+str(lig_dic[lig1]))
    dot_edges.append(str(lig_dic[lig1])+'->'+str(lig_dic[lig2]))
    dot_edges.append(str(lig_dic[lig2])+'->'+str(lig_dic[lig1]))
    dot.edge(str(lig_dic[lig1]), str(lig_dic[lig2]))
    dot.edge(str(lig_dic[lig2]), str(lig_dic[lig1]))

filein.close()




