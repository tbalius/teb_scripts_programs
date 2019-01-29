#! /usr/bin/python2.6

#######################################################################
#  Written by Trent E Balius 
#  B. Shoichet Lab at UCSF, and now at University of Toronto.
#  This python program takes as input a four letter code 
#  and will give You back a receptor and a ligand in two 
#  diferent pdb files. 
#  
#  This is a replacement for the be_blasti.csh written by fcolizzi 
#  in the Brian Shoichet Group at UCSF in June 2008. 
#######################################################################

#######################################################################
#  Requierments:
#  This program requiers Bio python.  
#  Also it requiers the program msms:
#######################################################################
#  installing MSMS
#  wget http://mgltools.scripps.edu/downloads/tars/releases/MSMSRELEASE/REL2.6.1/msms_i86_64Linux2_2.6.1.tar.gz
#  tar -xzvf msms_i86_64Linux2_2.6.1.tar.gz
#  ln -s /nfs/home/tbalius/zzz.programs/msms/msms.x86_64Linux2.2.6.1.staticgcc /nfs/home/tbalius/zzz.programs/msms/msms
#  ln -s `which awk` nawk 
#######################################################################

# Add in a function to replace MSE with MET. Trent Balius 2013/11/13



import Bio.PDB as BP
from Bio.PDB.ResidueDepth import residue_depth
import sys, os, copy
import urllib

## define globle variable. 

##     Standard residdues:
residue_list = ['ALA','ARG','ASN','ASP','CYS','CYX','GLN','GLU','GLY','HIS', 'HIE', 'HID', 'HIP' ,'ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL' ]

##     non-standared:
nonstand_resid_list = ['MSE', 'ORN','PTR', '4BF', 'TYS', 'TPO', 'SEP', 'CCS', 'CSW','KCX'] #,'ACE' ]
# MSE -- Se-MET
# TPO -- PHOSPHOTHREONINE; TPO is found in 450 entries : in  2I0E
# SEP -- PHOSPHOSERINE; SEP is found in 544 entries : in 2I0E
# PTR -- O-PHOSPHOTYROSINE; PTR is found in 372 entries : in 3LPB 
# ACE (ACETYL GROUP) may be a capping group on peptid
# KCX -- LYSINE NZ-CARBOXYLIC ACID
#        

##      Carbohydrate:
carbohydrate_list = ['NAG', 'MAN','BMA', 'FUC',  'NDG' ]
## carbohydrates may be linked.  examples: 2OYU, 2V3F 
## NAG -- N-ACETYL-D-GLUCOSAMINE; NAG is found in 3648 entries 
## MAN -- ALPHA-D-MANNOSE; MAN is found in 1205 entries 
## BMA -- BETA-D-MANNOSE; BMA is found in 1023 entries 
## FUC -- ALPHA-L-FUCOSE; FUC is found in 566 entries 
## NDG -- 2-(ACETYLAMINO)-2-DEOXY-A-D-GLUCOPYRANOSE; NDG is found in 433 entries 

##      Cofactors:
cofactor_list = [ 'COA', 'FAD', 'HEM','NAP', 'NDP', 'NAD','PLP', 'SAM', 'UMP' 'TIP', 'WAT', 'SPC', 'UKK' ]
#COA 2CP 3CP 3HC 4CA 4CO ACO AMX BCA CA3 CA5 CAA CAO CIC CMC CMX CO8 COD COF COS COT CS8 DAK DCA DCC FAM FCX HAX HMG HXC LYX MCA MCD MDE MLC MYA NHM NMX SAM SCA SCD SCO HEM 1CP B12 BCB BCL BLA BLV BPB BPH CCH CL1 CL2 CLA CLN CNC COB COH CON COJ COY CP3 DDH DEU DHE F43 FEC HAS HDD HDM HE6 HEA HEB HEC HEG HEO HES HEV HIF HNI IMP MHM MMP MP1 PC3 PCU PNI POR PP9 SRM ZEM ZNH NAD ADJ CAN CND DND NAC NAE NAH NAI NAJ NAP NAQ NAX NBD NBP NDA NDC NDO NDP NHD NHO ODP PAD SND TAP ZID FAD 6FA FAA FAB FAE FAS FDA FMA FMN FNS MGD RFL AMP ADP ANP ATP CMP CDP CTP GMP GDP GNP GTP 2GP TMP TDP TTP UMP UDP UTP PSU GAR SF4 PLP #####NoNsTaNdArDrEsIdUeS CCS TYS APR

# PLP = Pyridoxal-phosphate (PLP, pyridoxal-5'-phosphate, P5P); Found in 657 entries in pdb on 2013/06/13; 1C8K 
# UMP = 2'-DEOXYURIDINE 5'-MONOPHOSPHATE; UMP is found in 138 entries; 1SYN -- Thymidylate synthase 
### UMP may not be as common enough of a co-factor. 
# 'TIP', TIP3P WATER 
# 'WAT', TIP3P WATER 
# 'SPC', SPC   WATER 
# 'UKK', Genaric cofactor for people who want to trick the script. 

##      Ions:
ion_list = ['  K', ' AU', ' CA', ' CD', ' CL', ' CO', ' CP', ' CU', ' FE', ' HG', ' MG', ' MN', ' NA', ' NI', ' PT', ' YB', ' ZN']

##       other non ligands:
## detergents, stuf in bufers, ...
notligand_list = [ 'HOH', 'MPD', 'DMS', 'EDO', 'GOL','FMT', 'ACY', 'SO4', 'PO4']
# FMT = FORMIC ACID; FMT is found in 603 entries 
# ACT = ACETATE ION ; ACT is found in 2473 entries : in 2OWB
# ACY = ACETIC ACID ; ACY is found in 607 entries  : in 3NF7 
# DMS = DIMETHYL SULFOXIDE; DMS is found in 603 entries : in 3NXU 


## this file will brake up that PDB file on "Alternate location indicator" Column.
## this allows multiple conformations of molecules in the same structure.
## this will also remove ctrl M from the pdb file
def Preprocess_PDB(file):
   fileh1 = open(file,'r') 
   fileprifix = process_filename_for_pdb(file)
   #fileprifix = file.split('.')[0] ## Here I am assuming that the file is file  = fileprifix.pdb
   #if (len(file.split('.')) > 2):
   #    print "file must be named : fileprifix.pdb "
   #    print "and fileprifix must not contain the dot character '.' "
   #    exit()
   #if (file.split('.')[1] != 'pdb'):
   #    print "This must be a pdb file with the file name as follows:"
   #    print "     fileprifix.pdb"
   #    exit()

   ALI = {} ## define a dictionary of "Alternate location indicator" 
   # loop over the file and remember how meny ALI there are and 
   # what they are.
   atominfo_ALI = {} ## dictionary the contain ALI or each residue [resdinfo=resname,reschain,resid].

   lines = fileh1.readlines() 
   fileh1.close()
   #os.system('mv ' + file +' '+ fileprifix + '_downloaded.pdb') # move to new file
   os.system('mv ' + file +' '+ fileprifix + '_ori.pdb') # move to new file

   # remove ctrl M
   for i in range(0,len(lines)):
       lines[i] = lines[i].replace('\r','')

   multiple_Modelflag = False

   #for line in fileh1:
   for line in lines:
       tempREMARK = line[0:10]
       tempATOM   = line[0:6]
       if tempREMARK == 'REMARK 470':
       ## This remark has to do with missing atoms for 'ATOM  '
       ## FOR RIGHT NOW I AM JUST REPORTING
       ## IN FUTURE I WOULD LIKE TO DO SOMETHING WITH 
       ## THIS INFO
          print line
          continue
       elif tempREMARK == 'REMARK 610':
       ## This remark has to do with missing atoms for 'HETATM' 
       ## FOR RIGHT NOW I AM JUST REPORTING
       ## IN FUTURE I WOULD LIKE TO DO SOMETHING WITH 
       ## THIS INFO
          print line
          continue
       ##if tempATOM == 'MODEL ': File with multiple Models will not me processed corectly by this script. 
       ## the plan is to handel this better.  maybe write out a pdb file for each model.
       if tempATOM == 'MODEL ':
          if (multiple_Modelflag): # frist time will be false second time will be true and will break the loop.
                                   # only the first model will be processed in
             print "this has multiple models."
             print "only the frist is read in"
             break
          multiple_Modelflag = True
          
       if tempATOM == 'ATOM  ' or tempATOM == 'HETATM':
          atomname = line[13:16]
          resname  = line[17:20]
          reschain = line[21]
          resid    = line[23:26]
          tempatominfo = atomname+','+resname+','+reschain+','+resid
          #print tempatominfo 
          #tempresinfo = resname+','+reschain+','+resid
          #print tempresinfo 
          tempALI = line[16]
          if not (tempALI in ALI.keys() or tempALI == ' '):
               ALI[tempALI] = 1

          ## remember which atom have which conformations
          if not (tempatominfo in atominfo_ALI.keys()):
               atominfo_ALI[tempatominfo] = [tempALI]
          elif not (tempALI in atominfo_ALI[tempatominfo]): # if the not in list asoiated with residue then add to list
               atominfo_ALI[tempatominfo].append(tempALI)
 
   #for atominfo in atominfo_ALI.keys():
   #    print atominfo, ":::" ,atominfo_ALI[atominfo] 


   if len(ALI.keys()) == 0:
       # write lines to original filename
       # note that the ctrl M character was removed
       fileh2 = open(file,'w')
       multiple_Modelflag = False
       for line in lines:
          tempATOM = line[0:6]
          ##if tempATOM == 'MODEL ': File with multiple Models will not me processed corectly by this script.
          ## the plan is to handel this better.  maybe write out a pdb file for each model.
          if tempATOM == 'MODEL ':
             if (multiple_Modelflag): # frist time will be false second time will be true and will break the loop.
                                      # only the first model will be processed in
                print "this has multiple models."
                print "only the frist is read in"
                break
             multiple_Modelflag = True

          if tempATOM == 'ATOM  ' or tempATOM == 'HETATM':
             if MSE_replace(line,fileh2):
                continue
             fileh2.write(line)
       fileh2.close()
       return
   # for each ALI right out a file containing all common atoms and 
   # the unique atoms flag by the ALI
   # if atom does not have a ALI = ' ' or curent ALI then uses A. 
   for ALIval in ALI.keys():
       fileh2 = open(fileprifix+'_'+ALIval+'.pdb','w')
       #for line in fileh1:
       for line in lines:
          tempATOM = line[0:6]
          if tempATOM == 'ATOM  ' or tempATOM == 'HETATM':
             atomname = line[13:16]
             resname  = line[17:20]
             reschain = line[21]
             resid    = line[23:26]
             tempatominfo = atomname+','+resname+','+reschain+','+resid
             if line[16] == ' ' or line[16] == ALIval:
                 N = len(line)
                 ## relace MSE with MET
                 if MSE_replace(line,fileh2):
                    continue
                 fileh2.write(line[0:16]+' '+line[17:N])
             ## if the atom does not have the current ALI or ' ' ALI then print atom from the 'A' state
             elif not (' ' in atominfo_ALI[tempatominfo] ) and not (ALIval in atominfo_ALI[tempatominfo] ) and line[16] == 'A':
                 N = len(line)
                 ## relace MSE with MET
                 if MSE_replace(line,fileh2):
                    continue
                 fileh2.write(line[0:16]+' '+line[17:N])

       fileh2.close()

   os.system('cp ' + fileprifix+'_'+ALI.keys()[0]+'.pdb' +' '+ file) # make the frist ALI be used 

   return

def MSE_replace(line,fileh2):
    #print line[17:20]
    N = len(line)
    if (line[17:20] == 'MSE'):
        print line[17:20]
        print line[12:16]
        fileh2.write('ATOM  ')
        if (line[12:15] == 'SE '):
           fileh2.write(line[6:12]+' SD  MET'+line[20:N-5]+' S  \n')
        else:
           fileh2.write(line[6:16]+' MET'+line[20:N])
        return True
    return False

   
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

def Is_carbohydrate_residue(resname):
    return (resname in carbohydrate_list)

def Is_ion_residue(resname):
    return (resname in ion_list)

def Is_not_lig_residue(res):
    resname = res.resname
    if len(list(res)) < 8:
       print resname + ' may be Nonligand: ligand is small'
    return (resname in notligand_list)

def Is_lig_residue(res):
    return not ( Is_protein_residue(res.resname) or Is_ion_residue(res.resname) or Is_cofactor_residue(res.resname) or Has_backbone(res) or Is_not_lig_residue(res))

## this section definse sections of PDB for printing:
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
            ## then loop over that list to remove stuff as a following step.
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

## This function gets a substructure that consists of the residues names in the list. 
## there may be more than one residue with the same name. 
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

## This function gets a substructure that consists of the residues ids in the list. 
## the residue id is unique 
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

## This is a smarter way of doing get_substructure_of_residue. 
## this will only copy what is needed. 
## using deep_copy everything is duplicated and then 
## what is not wanted is removed: This is inefictant. 
## beter is to only copy what is wanted.
## THIS FUNCTION IS NOT COMPLETED.
def get_substructure_of_residue_manual_copy(structure_org, residue_id):
    # initializing structure.
    structurebuild = BP.StructureBuilder.StructureBuilder() 
    structurebuild.init_structure("new")
    structure = structurebuild.get_structure()
    # loop over 
    # ENTITY.get_list() makes a copy of childeren. 
    # ENTITY.add() will add the copy to the new structure.
    return structure 

## wraper function
#def get_substructure_of_chain(structure_org, chain_id):
#    structure = copy.deepcopy(structure_org) ## avoids pointer issues
def get_substructure_of_chain(structure, chain_id):
    print "chain_id=" + str(chain_id)
    chain_id_list = [ chain_id ] 
    return get_substructure_of_chain_list(structure,chain_id_list)

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
            if len(list(chain)) == 0:
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
            #if len(list(chain)) < 20 and Is_all_protein(chain):
            if len(list(chain)) < 20 :
               chain_list.append(chain)

    structure_list = []
    for peptide in chain_list:
         struc_temp = copy.deepcopy(structure) ## avoids pointer issues
         struc_temp = get_substructure_of_chain(struc_temp, peptide.id)
         structure_list.append(struc_temp)
    
    return chain_list, structure_list

def On_res_list(resname, res_list):
    for res in res_list:
        if res.resname == resname: 
           return True
    return False

## This function will return a list of ligands.
def get_ligs(structure):
    structure_list = []
    het_res_list = []
    for model in structure.get_list():
        for chain in model.get_list():
            chain_het_res_list = []
            for res in chain:
                id = res.id
                if id[0] != ' ':
                     #if Is_lig_residue(res) and not On_res_list(res.resname,chain_het_res_list): 
                     #if Is_lig_residue(res) and not On_res_list(res.resname,het_res_list): 
                     if Is_lig_residue(res): 
                     #if Is_lig_residue(res): 
                         chain_het_res_list.append(res)
                         het_res_list.append(res)
            ## make a list of structs This can be output using 
            ## Do this seperately for each chain
            #struc_temp = copy.deepcopy(structure)
            struc_temp = get_substructure_of_chain(structure, chain.id)
            for lig in chain_het_res_list:
                 struc_temp2 = get_substructure_of_residue(struc_temp, lig.id)
                 struc_temp3 = get_substructure_of_residue_manual_copy(struc_temp, lig.id)
                 structure_list.append(struc_temp2)
            #het_res_list = het_res_list + chain_het_res_list
            
    print len(het_res_list)
    print het_res_list
    print len(structure_list)
    return het_res_list, structure_list

## This function will return a receptor compatable with ligands and peptides 
def get_receptor(structure_org, lig_list, pep_list,lig_num):
    ## lig_list is a list of residues
    ## pep_list is a list of chains
    ## Future: remove cofactors, ions, chains that are not close to ligs, pepides
    ## remove lig residues and peptide chains
    structure = copy.deepcopy(structure_org) ## make a copy
    lig_name_list = []
    for lig in lig_list:
        name = lig.resname
        lig_name_list.append(name)
    structure = get_substructure_remove_list(structure, lig_name_list)
    chain_id_list = []
    for pep in pep_list:
        chain_id_list.append(pep.id)
    structure = get_substructure_remove_chain_list(structure, chain_id_list)
 
    # this will see which ligands are bound or clashing with the receptor
    are_ligands_close_to_receptor(lig_list,structure)

    print "lig_num = ", lig_num   # this is the index for the ligand 
    if lig_num >= 0: #
        print "get close chains list to ligand"
        close_chains_list = close_chains_rec_lig(structure,lig_list[lig_num])
        structure = get_substructure_of_chain_list(structure, close_chains_list)
    return structure


def distance_chain_res(chain1,res2):
    min_d = 10000
    for res1 in chain1.get_list():
        d = residue_distance(res1,res2)
        if d < min_d:
           min_d = d
    return min_d
    
## struc1 = rec ,res2=lig
# This funsction will return a list of the chain.ids for close chains to ligand or struc 2
def close_chains_rec_lig(struc1, res2):
    list_chain = []
    min_dist = 1000.0 ##  
    
    for model in struc1.get_list():
        for chain in model.get_list():
             dist = distance_chain_res(chain,res2)
             if dist < min_dist:
                min_dist = dist
                min_dist_chain = chain.id
             if dist < 7.0:
                list_chain.append(chain.id)

    if len(list_chain) == 0: ## this is in case there are not chains with in the distance cutoff. 
                             ## we will keep the chain closest to the ligand. 
       list_chain.append(min_dist_chain)

    return list_chain

## this function will return the shortest distance between to residues.
def residue_distance(res1,res2):
   #print "I AM HERE", res1.id,res2.id
   min_dist = 1000.0
   for atom1 in res1:
       for atom2 in res2:
           dist = atom1-atom2
           if dist < min_dist: 
              min_dist = dist
   if min_dist < 0.5:
      print "distance = "+ str(min_dist) + "this is likely clash: " + str(res1.id) + " -- " + str(res2.id)
   if min_dist < 2.0 and min_dist > 0.5:
      print "distance = "+ str(min_dist) + "; this is likely a bound: " + str(res1.id) + " -- " + str(res2.id)
   return min_dist

#def Is_resid_attaced():
# this function prints if a ligand is clashing or is attached to another ligand
# IN FUTURE::: we will want to do something with the knowelage.
#              we should link ligands bound to one another into a group. 
#              we might consider using a dictionary.
#              when bond is detected, label both residues with Group name
def are_ligands_close(res_list):
    for i in range(0,len(res_list)):
        for j in range(i+1,len(res_list)):
            #print "I AM HERE"
            dist = residue_distance(res_list[i],res_list[j])
    
def are_ligands_close_to_receptor(lig_list,rec):
    #print "I AM HERE"
    for model in rec.get_list():
        for chain in model.get_list():
            for res in chain:
                for lig in lig_list:
                    dist = residue_distance(lig,res) 


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
                    if (Is_carbohydrate_residue(resname)):
                        type = ' carbohydrate '
                    if (Is_cofactor_residue(resname)):
                        type = ' cofactor '
                    if (Is_protein_residue(resname)):
                        type = ' protein '
                    if (Is_ion_residue(resname)):
                        type = ' ion '
                    if Is_not_lig_residue(res):
                        type = ' notLig '
                    if Has_backbone(res):
                        type = type + ' has backbone: amino_acid??'
                    if Is_lig_residue(res):
                        type = type + ' maybe Lig? '

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

## this function will calculate  N (number of heavy atoms) in a residue and return a score:
##                    /   -1  if N < 16  
## function. score = {    -N / 500  if N > 500  
##                    \    0 otherwize
## We can modify the function defenition, for example use a bellshape function.  
def eval_size(structure):
   print " start eval_size "
   N = 0
   sizeval = 500 # this is the maxum size be for penlizing the molcule
   for model in structure.get_list():
        for chain in model.get_list():
            for res in chain:
                #print res.get_fullname()
                #print res.resname
                #print res.segid
                #print res.disordered
                for atom in res:
                    name = atom.get_name()
                    if name[0] == 'H':
                       #print name
                       continue
                    #print atom.get_fullname()
                    N = N + 1
   ## calculate score
   score = 0
   if N < 16: 
      score = -10
   elif N > sizeval:
      score = -N / sizeval
   print " finish eval_size : N = " + str(N) + "; score = " + str(score)
   return score 

## this is the function that evaluates the ligands. 
## 
def get_structure_eval(structure,surface):
    size_score = eval_size(structure)
    rd = 0
    o  = 0
    b  = 0
    for model in structure.get_list():
        for chain in model.get_list():
            rd = 0
            o  = 0
            b  = 0
            for res in chain:
                rd = rd + residue_depth(res, surface)
                o  = o  + calc_occupancy(res)
                b  = b  + calc_bfactor(res)

    # we should also consider penlizing the ligand if not all atoms are reprenented in pdb
    #eval = rd + o - 0.5 * b + size_score
    eval = rd + size_score
    return rd, o, b, eval


def write_list(name_prefix,start,struc_list,surf,io):
    print "Trying to Writing " + name_prefix + "pdb"
    count = start
    struc_count = 0
    best_struc_num = 0
    max_eval = -100000
    if len(struc_list) == 0:
       print "Warning something weird is hapening"
       return -1

    for struc in struc_list:
        io.set_structure(struc)
        io.save(name_prefix+'.'+str(count)+'.pdb')
        rd, o, b, eval = get_structure_eval(struc,surf)
        print "eval = " + str(eval)

        if eval > max_eval: 
           max_eval = eval
           best_struc_num = struc_count

        count = count+1
        struc_count = struc_count+1
    ## write out best ligand
    print len(struc_list), best_struc_num
    io.set_structure(struc_list[best_struc_num])
    io.save(name_prefix+'.pdb')
    return best_struc_num

# this function will renumber each chain starting at one.     
# One reason to do this is to get ride of code for insertion of residues.
def renumber_residues(structure):
   for model in structure.get_list():
      for chain in model.get_list():
         print "Renumbering chain "+ str(chain.id)
         i = 1
         for residue in chain:
            residue.id = (' ', i, ' ')
            i += 1

# this function will process a filename returning the fileprefix
# this function assumes that the filename obases this formate:
# /path/pdbcode.pdb 
def process_filename_for_pdb(file):
       splitfile = file.split('/')
       splitfile2 = splitfile[len(splitfile)-1].split('.')
       if (len(splitfile2)!=2):
           print "file name is not is not right."
           print "expected filename format: /path/pdbcode.pdb"
           exit()
       elif (splitfile2[1] != 'pdb'):
           print "file name is not is not right."
           print "expected filename format: /path/pdbcode.pdb"
           exit()
       pdbcode = splitfile2[0]
       return pdbcode

def main():
     if len(sys.argv) != 5: # if no input
         print "ERORR: not the right number of arguments"
         print "syntax: ~/zzz.scripts/be_blasti.py [ --pdbcode pdbcodename | --pdbfile pdbfilename ] [ carbohydrate| nocarbohydrate ] [renumber | orginal_numbers]"
         return
 
     ## input pdb
     #pdbcode = '3T4G'

     flag = sys.argv[1]

     if flag == '--pdbcode':
       ## if a pdbcode is spesified then we will download it from the pdb.
       pdbcode = sys.argv[2]
       #file = '/raid9/tbalius/Projects/ProteomicDOCKing/plversion1/'+pdbcode+'/'+pdbcode+'/'+pdbcode+'.pdb.ori'
       #file = '/raid9/tbalius/Projects/ProteomicDOCKing/plversion1/'+pdbcode+'/'+pdbcode+'/'+pdbcode+'.pdb'
       #url = 'ftp://ftp.wwpdb.org/pub/pdb/data/biounit/coordinates/all/' + pdbcode + '.pdb1.gz'
       url = 'http://www.rcsb.org/pdb/files/'+pdbcode+'.pdb'
       print "downloading with urllib"
       urllib.urlretrieve(url, pdbcode + ".pdb")
       file = pdbcode + ".pdb"
     elif flag == '--pdbfile':
       # if a filename is spesified then we will
       # process the file name
       # the filename should have the following formate:
       #    /path/pdbcode.pdb 
       file = sys.argv[2]
       pdbcode = process_filename_for_pdb(file)
     else:
       print "flag is needed."
       print "options: --pdbcode (download from pdb) or --pdbfile (spesify the file locations)"
       exit()
        
     print "pdbcode = " + pdbcode
     print "file = " + file

     if (sys.argv[3] == 'carbohydrate' ):
         flag_carbohydrate = True
     elif(sys.argv[3] == 'nocarbohydrate'):
         flag_carbohydrate = False
     else:
         print "ERORR: the second parameter can be carbohydrate or nocarbohydrate"
     if (sys.argv[4] == 'renumber' ):
         flag_renumber = True
     elif(sys.argv[4] == 'orginal_numbers'):
         flag_renumber = False
     else:
         print "ERORR: the third parameter can be renumber (renumber residues or orginal_numbers (use the curent numbering)"
         print "       the renumber is recomended.  get ride of code for insertion of residues."
         
     
     # this function will split up "Alternate location indicator" 
     # ALI is not stored in BIO PDB.
     # At this step we may want to do other processing
     # This will create 3 files: (1) the original files downloaded, (2) everything incomon + the ALI mark A, and (3) everything incomon + the ALI mark B. 
     # the file (2) will be used for additional steps and is copied to pdbcode.pdb 
     Preprocess_PDB(file)
     #exit() 
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
     #struc = get_substructure_remove_list(struc, ['HOH'])
     ## remove waters and other small molecules (Hetatms) that are not posible ligand.
     struc = get_substructure_remove_list(struc, notligand_list)
     #struc = get_substructure_remove_waters(struc)

     ## remove carbohydrates
     if not (flag_carbohydrate): 
        struc = get_substructure_remove_list(struc, carbohydrate_list)
     
     io.save("nowaters.pdb")
     
     #get_structure_stat(struc,surf)
     
     ## if multiple models choose the first model.
     struc = get_structure_one_model(struc)
     #get_structure_stat(struc,surf)
     
     
     ## idenify small peptides
     print "idenifying small peptides"
     peptides_list, peptides_struc_list = get_peptides(struc)
     ## write out peptides
     pepnum = write_list('pep',1,peptides_struc_list,surf,io)
     #remove peptides
     struc = get_receptor(struc,[],peptides_list,-1)
     
     ## idenify ligands
     print "idenifying ligands"
     lig_list, lig_struc_list = get_ligs(struc)
     ## write out ligands:
     # lignum is the index of the best ligand.
     # if the list is empty then return -1. 
     lignum = write_list('lig',1,lig_struc_list,surf,io)
     
     ## check if Attached to neighbor
     ## check if Attached to or clash?
     are_ligands_close(lig_list) 
     
     ## Idenify a recptor compatable with the ligands/peptides
     ## we  only include chains close to a ligand/peptide as 
     ## part of protein. 
     ## evaluate chains by seeing how close the ligand is to chain.
     ## get_receptor will keep chains with in a certein distance (7 
     ## Angstroms) from the ligand or the the chain closest to the ligand. 
     receptor_struc = get_receptor(struc,lig_list,[],lignum)
     # renumber all chains.  Each chain will start at one. 
     if (flag_renumber):
        renumber_residues(receptor_struc) 
     
     io.set_structure(receptor_struc)
     io.save("rec.pdb")
     
     ## output structures (all ligands, proteins and ligands.
     #io=BP.PDBIO()
     #io.set_structure(struc)

main()     
