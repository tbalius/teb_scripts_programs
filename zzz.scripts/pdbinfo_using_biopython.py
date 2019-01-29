#! /usr/bin/python2.6

import Bio.PDB as BP
from Bio.PDB.ResidueDepth import residue_depth
import sys, os, copy

## define globle variable. 

##     Standard residdues:
residue_list = ['ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL' ]

##     non-standared:
nonstand_resid_list = ['MSE', 'ORN', '4BF', 'TYS', 'CCS', 'CSW' ]
#residue_list = residue_list + nonstand_resid_list

##      Carbohydrate:
carbohydrate_list = ['NAG']

##      Cofactors:
cofactor_list = residue_list + [ 'COA', 'HEM','NAP', 'NDP', 'NAD', 'SAM' ]
#COA 2CP 3CP 3HC 4CA 4CO ACO AMX BCA CA3 CA5 CAA CAO CIC CMC CMX CO8 COD COF COS COT CS8 DAK DCA DCC FAM FCX HAX HMG HXC LYX MCA MCD MDE MLC MYA NHM NMX SAM SCA SCD SCO HEM 1CP B12 BCB BCL BLA BLV BPB BPH CCH CL1 CL2 CLA CLN CNC COB COH CON COJ COY CP3 DDH DEU DHE F43 FEC HAS HDD HDM HE6 HEA HEB HEC HEG HEO HES HEV HIF HNI IMP MHM MMP MP1 PC3 PCU PNI POR PP9 SRM ZEM ZNH NAD ADJ CAN CND DND NAC NAE NAH NAI NAJ NAP NAQ NAX NBD NBP NDA NDC NDO NDP NHD NHO ODP PAD SND TAP ZID FAD 6FA FAA FAB FAE FAS FDA FMA FMN FNS MGD RFL AMP ADP ANP ATP CMP CDP CTP GMP GDP GNP GTP 2GP TMP TDP TTP UMP UDP UTP PSU GAR SF4 PLP #####NoNsTaNdArDrEsIdUeS CCS TYS APR

##      Ions:
ion_list = ['  K', ' AU', ' CA', ' CD', ' CL', ' CO', ' CP', ' CU', ' FE', ' HG', ' MG', ' MN', ' NA', ' NI', ' PT', ' YB', ' ZN']

##       other non ligands:
## detergents, stuf in bufers, ...
notligand_list = [ 'HOH', 'MPD', 'EDO']

def Is_protein_residue(resname):
#    print resname , (resname in residue_list)
    return (resname in residue_list or resname in nonstand_resid_list)

## if the resdiue has N Ca C O then it is likely a amino acid. 
def Has_backbone(residue):
    if (len(list(residue))>3):
        atom_list =  residue.get_unpacked_list()
        if (atom_list[0].get_name() == "N" and atom_list[1].get_name() == "CA" and atom_list[1].get_name() == "C" and atom_list[3].get_name() == "O" ):
            print residue.resname + " maybe a non-standard residue"
            return True
    return False


def Is_cofactor_residue(resname):
    return (resname in cofactor_list)

def Is_ion_residue(resname):
    return (resname in ion_list)


def Is_lig_residue(res):
    return not ( Is_protein_residue(res.resname) or Is_ion_residue(res.resname) or Has_backbone(res))

## this section definse sections of PDB for printing:
#
#class RECSelect(BP.Select):
#    def accept_residue(self, residue):
#        if Is_protein_residue(residue.get_resname()):
#            return 1
#        else:
#            return 0
#
#class LIGSelect(BP.Select):
#    def accept_residue(self, residue):
#        if Is_lig_residue(residue.get_resname()):
#            return 1
#        else:
#            return 0

# this function calcuclates the average occupancy a given residue
def calc_occupancy( residue ):
    occupancy = 0.0
    for atom in residue:
        occupancy = occupancy + atom.get_occupancy()
    occupancy = occupancy / len(list(residue))
    return occupancy

# this function calcuclates the average bfactor for a given residue
def calc_bfactor( residue ):
    bfactor = 0.0
    for atom in residue:
        bfactor = bfactor + atom.get_bfactor()
    bfactor = bfactor / len(list(residue))
    return bfactor

# This function will remove all waters 
# To write this function the following wiki was helpful:
# http://pelican.rsvs.ulaval.ca/mediawiki/index.php/Manipulating_PDB_files_using_BioPython
def get_substructure_remove_waters(structure_org):
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = []
        for chain in model:
            res_id_rm_list = [] # This list remembers wich residues to remove.
            for residue in chain:
                id = residue.id
                if id[0] == 'W':
                    res_id_rm_list.append(id)
            ## when I tryed to remove in the loop it skiped every other water.
            ## I think that this is some weird indexing issue.
            ## to surcomvent this I just loop over without removing anything, put the id on a list 
            ## then loop over that list to remove stuff.
            for id in res_id_rm_list:
                chain.detach_child(id)
            if len(chain) == 0:
                chain_id_rm_list.append(chain.id)
        ## this is the same logic as discriped above.
        ## loop over all chain, see which ones should be removed and then remove them.
        for id in chain_id_rm_list: 
            model.detach_child(id)
    return structure

def get_substructure_remove_list(structure_org, resname_list):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped.
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = [] ## remember which chains to delete
        for chain in model:
            res_id_rm_list = [] # remembers which residues to remove.
            for residue in chain:
                resname = residue.resname
                id = residue.id
                if resname in resname_list:
                    #chain.detach_child(id)
                    res_id_rm_list.append(id) # put on list to delete

            #loop over list of residue id's and remove them
            for id in res_id_rm_list:
                chain.detach_child(id)

            if len(list(chain)) == 0:
                #model.detach_child(chain.id)
                chain_id_rm_list.append(chain.id) # put on list to delete
        #loop over list of chain id's and remove them
        for id in chain_id_rm_list: 
            model.detach_child(id) 
    return structure

def get_substructure_of_list(structure_org, resname_list):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped. 
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = [] ## remember which chains to delete
        for chain in model:
            res_id_rm_list = [] # remembers which residues to remove.
            for residue in chain:
                resname = residue.resname
                id = residue.id
                if not (resname in resname_list):
                    #chain.detach_child(id)
                    res_id_rm_list.append(id) # put on list to delete

            #loop over list of residue id's and remove them
            for id in res_id_rm_list:
                chain.detach_child(id)

            if len(chain) == 0:
                #model.detach_child(chain.id)
                chain_id_rm_list.append(chain.id) # put on list to delete
        #loop over list of chain id's and remove them
        for id in chain_id_rm_list:
            model.detach_child(id)
    return structure

## 
def get_substructure_of_residue(structure_org, residue_id):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped. 
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = [] ## remember which chains to delete
        for chain in model:
            res_id_rm_list = [] # remembers which residues to remove.
            for residue in chain:
                resname = residue.resname
                id = residue.id
                if not (residue.id == residue_id):
                    #chain.detach_child(id)
                    res_id_rm_list.append(id) # put on list to delete

            #loop over list of residue id's and remove them
            for id in res_id_rm_list:
                chain.detach_child(id)

            if len(chain) == 0:
                #model.detach_child(chain.id)
                chain_id_rm_list.append(chain.id) # put on list to delete
        #loop over list of chain id's and remove them
        for id in chain_id_rm_list:
            model.detach_child(id)
    return structure

## wraper function
def get_substructure_of_chain(structure_org, chain_id):
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    chain_id_list = [ chain_id ] 
    get_substructure_of_chain_list(structure,chain_id_list)

def get_substructure_of_chain_list(structure_org, chain_id_list):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped. 
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = [] ## remember which chains to delete
        for chain in model:
            if not (chain.id in chain_id_list):
                #chain.detach_child(id)
                chain_id_rm_list.append(chain.id) # put on list to delete
            if len(chain) == 0:
                #model.detach_child(chain.id)
                chain_id_rm_list.append(chain.id) # put on list to delete
        #loop over list of chain id's and remove them
        for id in chain_id_rm_list:
            model.detach_child(id)
    return structure

def get_substructure_remove_chain_list(structure_org, chain_id_list):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped. 
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    for model in structure:
        chain_id_rm_list = [] ## remember which chains to delete
        for chain in model:
            if (chain.id in chain_id_list):
                #chain.detach_child(id)
                chain_id_rm_list.append(chain.id) # put on list to delete
            if len(chain) == 0:
                #model.detach_child(chain.id)
                chain_id_rm_list.append(chain.id) # put on list to delete
        #loop over list of chain id's and remove them
        for id in chain_id_rm_list:
            model.detach_child(id)
    return structure



def get_structure_one_model(structure_org):
    ## step one. loop over everything remember what we want to remove. Put the id in a list.
    ## then remove those structures
    ## When I tried doing this in one loop every other residue was skiped.
    structure = copy.deepcopy(structure_org) ## avoids pointer issues
    model_id_rm_list = []
    flag_first = True
    # delete all but the first model 
    # if there is only one then this should do nothing.
    for model in structure:
        if flag_first:
           flag_first = False
        else:
           model_id_rm_list.append(model.id)
           
        
    #loop over list of model id's and remove them
    for id in model_id_rm_list:
        structure.detach_child(id)
    return structure

## this return true if all residues are proteins
## and false other wise.
## Future: We might want to make sure that all residues are senquincal and conected.
def Is_all_protein(chain):
    for res in chain:
        if not Is_protein_residue(res):
           return False
    return True

## this function will return chain that have less than 30 amino acids.
## this will be treated as ligands
def get_peptides(structure):
    chain_list = []
    for model in structure.get_list():
        for chain in model.get_list():
            if len(list(chain)) < 20 and Is_all_protein(chain):
               chain_list.append(chain)

    structure_list = []
    for peptide in chain_list:
         struc_temp = copy.deepcopy(structure) ## avoids pointer issues
         struc_temp = get_substructure_of_chain(struc_temp, peptide.id)
         structure_list.append(struc_temp)
    return chain_list, structure_list

## This function will return a list of ligands.
def get_ligs(structure):
    het_res_list = []
    for model in structure.get_list():
        for chain in model.get_list():
            for res in chain:
                id = res.id
                if id[0] != ' ':
                     if Is_lig_residue(res) : 
                         het_res_list.append(res)
    ## make a list of structs This can be output using 
    ##
    structure_list = []
    for lig in het_res_list:
         struc_temp = copy.deepcopy(structure)
         struc_temp = get_substructure_of_residue(struc_temp, lig.id)
         structure_list.append(struc_temp)
    return het_res_list, structure_list

## This function will return a receptor compatable with ligands and peptides 
def get_receptor(structure_org, lig_list, pep_list,surface):
    ## lig_list is a list of residues
    ## pep_list is a list of chains
    ## Future: remove cofactors, ions, chains that are not close to ligs, pepides
    ## remove lig residues and peptide chains
    structure = copy.deepcopy(structure_org) ## make a copy
    #get_structure_stat(structure,surface)
    lig_name_list = []
    for lig in lig_list:
        name = lig.resname
        lig_name_list.append(name)
    structure = get_substructure_remove_list(structure, lig_name_list)
    #get_structure_stat(structure,surface)
    chain_id_list = []
    for pep in pep_list:
        chain_id_list.append(pep.id)
    structure = get_substructure_remove_chain_list(structure, chain_id_list)
    #get_structure_stat(structure,surface)
    
    return structure

## this function will return the shortest distance between to residues.
def residue_distance(res1,res2):
   min_dist = 1000.0
   for atom1 in res1:
       for atom2 in res2:
           dist = atom1-atom2
           if dist < min_dist : 
              min_dist = dist
   return min_dist

#def Is_resid_attaced():

def get_structure_stat(structure,surface):
  print "* " + structure.id
  print "  number of models:" + str(len(structure.get_list()))
  modelnum = 1
  for model in structure.get_list():
        print "  Model " + str(modelnum)
        print "    number of chains:" + str(len(model.get_list()))
        #print list(model)
        for chain in model.get_list():
            print "    chain " + chain.id 
            print "      number of residues                   : " + str(len(chain.child_list))
            count_W = 0
            count_H = 0
            text_H  = ''
            for res in chain:
                id = res.id
                if id[0] == 'W':
                    count_W = count_W + 1
                elif id[0] != ' ':
                    #print id
                    #residue_depth(res, surface)
                    resname = res.resname
                    type = '?'
                    #print resname
                    if (Is_cofactor_residue(resname)):
                        type = 'cofactor'
                    if (Is_protein_residue(resname)):
                        type = 'protein'
                    if (Is_ion_residue(resname)):
                        type = 'ion'
                    rd = residue_depth(res, surface)
                    o  =  calc_occupancy(res)
                    b  =  calc_bfactor(res)
                    text_H = text_H + "        " + id[0] +" "+ str(id[1]) + " (barial = "+ str(rd) +";"
                    text_H = text_H + " occupancy = "+ str(o) +";"
                    text_H = text_H + " bfactor = "+ str(b) +";"+resname+"=="+type
                    text_H = text_H + ")"+ '\n'
                    count_H = count_H + 1
            print "      number that are water residues       : " + str(count_W)
            print "      number that are other hetro-residues : " + str(count_H)
            print text_H
            #print "    number of atoms: " + 
        modelnum = modelnum+1

def write_list(name_prefix,start,struc_list,io):
    count = start
    for struc in struc_list:
        io.set_structure(struc)
        io.save(name_prefix+'.'+str(count)+'.pdb')
        count = count+1


## input pdb
#pdbcode = '3T4G'
pdbcode = sys.argv[1]
#file = '/raid9/tbalius/Projects/ProteomicDOCKing/plversion1/'+pdbcode+'/'+pdbcode+'/'+pdbcode+'.pdb.ori'
file = '/raid9/tbalius/Projects/ProteomicDOCKing/plversion1/'+pdbcode+'/'+pdbcode+'/'+pdbcode+'.pdb'

if (not os.path.exists(file) or os.path.getsize(file) == 0):
   print file + " is empty or does not exist "
   exit()

parser=BP.PDBParser()
struc=parser.get_structure(pdbcode, file)

io=BP.PDBIO()
io.set_structure(struc)
io.save("everything.pdb")

surf = BP.get_surface(file)

get_structure_stat(struc,surf)

## remove waters.
struc = get_substructure_remove_list(struc, ['HOH'])
#struc = get_substructure_remove_waters(struc)
io.save("nowaters.pdb")

get_structure_stat(struc,surf)

## if multiple models choose the first model.
struc = get_structure_one_model(struc)
get_structure_stat(struc,surf)

## idenify ligands
lig_list, lig_struc_list = get_ligs(struc)
get_structure_stat(struc,surf)

## write out ligands:
write_list('lig',1,lig_struc_list,io)

#print len(het_list)

## idenify small peptides
peptides_list, peptides_struc_list = get_peptides(struc)
## write out peptides
write_list('pep',1,peptides_struc_list,io)

## idenify a recptor compatable with the ligands/peptides
receptor_struc = get_receptor(struc,lig_list,peptides_list,surf)
io.set_structure(receptor_struc)
io.save("rec.pdb")

## output structures (all ligands, proteins and ligands.
#io=BP.PDBIO()
#io.set_structure(struc)

