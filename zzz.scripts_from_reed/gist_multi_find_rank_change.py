from __future__ import print_function, absolute_import

import os, sys
import numpy as np
from scipy import stats
import math
from rdkit import Chem as C
from rdkit.Chem import Descriptors as D
from rdkit.Chem import rdMolDescriptors as CD


def get_stuff(smiles):

        mol = C.MolFromSmiles(smiles)
	hac = D.HeavyAtomCount(mol)
        logp = C.Crippen.MolLogP(mol)
	rotB = D.NumRotatableBonds(mol)

        return(logp, hac, rotB)


def create_temp_dict(lig_dict, dec_dict):

	temp_lig_dict = {}
	temp_dec_dict = {}
	
	for lig in lig_dict:
		smiles = lig_dict[lig][0]
		temp_lig_dict[lig] = []

	for dec in dec_dict:
		smiles = dec_dict[dec][0]
		temp_dec_dict[dec] = []

	return(temp_lig_dict, temp_dec_dict)


def refill_comp_dict(temp_dict, final_dict, dock_identifier):

	for lig in temp_dict:
		if len(temp_dict[lig]) > 1:
			rank1 = temp_dict[lig][0]
			es1 = temp_dict[lig][1]
                        pol1 = temp_dict[lig][2]
                        apol1 = temp_dict[lig][3]
                        vdw1 = temp_dict[lig][4]
			gist1 = temp_dict[lig][5]

                        rank2 = temp_dict[lig][6]
                        es2 = temp_dict[lig][7]
                        pol2 = temp_dict[lig][8]
                        apol2 = temp_dict[lig][9]
                        vdw2 = temp_dict[lig][10]
			gist2 = temp_dict[lig][11]

			if lig in final_dict:
				final_dict[lig].append([dock_identifier, rank1, es1, pol1, apol1, vdw1, gist1, rank2, es2, pol2, apol2, vdw2, gist2])
			else:
				final_dict[lig] = [dock_identifier, rank1, es1, pol1, apol1, vdw1, gist1, rank2, es2, pol2, apol2, vdw2, gist2]

	return(final_dict)
	 

def collect_energies(uniq_txt_file_std, uniq_txt_file_rew, lig_dict, dec_dict, dock_identifier):

	txt_open_std = open(uniq_txt_file_std,'r')
	txt_read_std = txt_open_std.readlines()
	txt_open_std.close()

	txt_open_rew = open(uniq_txt_file_rew,'r')
	txt_read_rew = txt_open_rew.readlines()
	txt_open_rew.close()

	temp_lig_dict, temp_dec_dict = create_temp_dict(lig_dict, dec_dict)

	for i in range(len(txt_read_std)):
		line1 = txt_read_std[i].strip().split()
		lig_ID = line1[2]
		es = float(line1[12])
		gist = float(line1[13])
                vdw = float(line1[14])
                pol = float(line1[15])
                apol = float(line1[16])

		if lig_ID in temp_lig_dict:
			temp_lig_dict[lig_ID].append(i+1)
			temp_lig_dict[lig_ID].append(es)
                        temp_lig_dict[lig_ID].append(pol)
                        temp_lig_dict[lig_ID].append(apol)
                        temp_lig_dict[lig_ID].append(vdw)
                        temp_lig_dict[lig_ID].append(gist)

		elif lig_ID in temp_dec_dict:
			temp_dec_dict[lig_ID].append(i+1)
			temp_dec_dict[lig_ID].append(es)
                        temp_dec_dict[lig_ID].append(pol)
                        temp_dec_dict[lig_ID].append(apol)
                        temp_dec_dict[lig_ID].append(vdw)
                        temp_dec_dict[lig_ID].append(gist)

	for i in range(len(txt_read_rew)):
		line1 = txt_read_rew[i].strip().split()
		lig_ID = line1[2]

		es = float(line1[12])
		gist = float(line1[13])
                vdw = float(line1[14])
                pol = float(line1[15])
                apol = float(line1[16])

		if lig_ID in temp_lig_dict:
			temp_lig_dict[lig_ID].append(i+1)
			temp_lig_dict[lig_ID].append(es)
                        temp_lig_dict[lig_ID].append(pol)
                        temp_lig_dict[lig_ID].append(apol)
                        temp_lig_dict[lig_ID].append(vdw)
                        temp_lig_dict[lig_ID].append(gist)

		elif lig_ID in temp_dec_dict:
			temp_dec_dict[lig_ID].append(i+1)
			temp_dec_dict[lig_ID].append(es)
                        temp_dec_dict[lig_ID].append(pol)
                        temp_dec_dict[lig_ID].append(apol)
                        temp_dec_dict[lig_ID].append(vdw)
                        temp_dec_dict[lig_ID].append(gist)

	lig_dict = refill_comp_dict(temp_lig_dict, lig_dict, dock_identifier)
	dec_dict = refill_comp_dict(temp_dec_dict, dec_dict, dock_identifier)

	return(lig_dict, dec_dict)

def fill_lig_dec_dicts(system):

	ligand_file = "/mnt/nfs/db/users/adler/AutoDude_LigandDB2_NachTeaguesFixAnDerWebseite/autodude.docking.org/dude_e_db2/"+system+"_DOCKINGAutoDudeData_Adler/lig-decoy-db/ligands.smi"
        decoy_file = "/mnt/nfs/db/users/adler/AutoDude_LigandDB2_NachTeaguesFixAnDerWebseite/autodude.docking.org/dude_e_db2/"+system+"_DOCKINGAutoDudeData_Adler/lig-decoy-db/decoys.smi"

        lig_dict = {}
        dec_dict = {}

        open_lig = open(ligand_file,'r')
        read_lig = open_lig.readlines()
        open_lig.close()

        open_dec = open(decoy_file, 'r')
        read_dec = open_dec.readlines()
        open_dec.close()

        for line in read_lig:
                splitline = line.strip().split()
                lig_ID = splitline[-1]
                smiles = splitline[0]
                lig_dict[lig_ID] = [[smiles]]

        for line in read_dec:
                splitline = line.strip().split()
                dec_ID = splitline[-1]
                smiles = splitline[0]
                dec_dict[dec_ID] = [[smiles]]

	return(lig_dict, dec_dict)


def calc_mag(es1, pol1, apol1, vdw1, gist1, es2, pol2, apol2, vdw2, gist2):
	
	denom1 = (abs(es1) + abs(pol1) + abs(apol1) + abs(vdw1) + abs(gist1))
	denom2 = (abs(es2) + abs(pol2) + abs(apol2) + abs(vdw2) + abs(gist2))


	es_perc1 = abs(es1) / denom1 * 100.
	es_perc1 = round(es_perc1, 2)
	es_perc2 = abs(es2) / denom2 * 100.
	es_perc2 = round(es_perc2, 2)

	ld_perc1 = (abs(pol1) + abs(apol1)) / denom1 * 100.
	ld_perc1 = round(ld_perc1, 2)
	ld_perc2 = (abs(pol2) + abs(apol2)) / denom2 * 100.
	ld_perc2 = round(ld_perc2, 2)

	vdw_perc1 = abs(vdw1) / denom1 * 100.
	vdw_perc1 = round(vdw_perc1, 2)
	vdw_perc2 = abs(vdw2) / denom2 * 100.
	vdw_perc2 = round(vdw_perc2, 2)

	gist_perc1 = abs(gist1) / denom1 * 100.
	gist_perc1 = round(gist_perc1, 2)
	gist_perc2 = abs(gist2) / denom2 * 100.
	gist_perc2 = round(gist_perc2, 2)

	return (es_perc1, es_perc2, ld_perc1, ld_perc2, vdw_perc1, vdw_perc2, gist_perc1, gist_perc2)


def process_dict(comp_dict, comptype):

	log_diff_list = []
	comp_count = 0	
	for lig in comp_dict:
		lig_rank_list = []
		for i in range(len(comp_dict[lig])):
			if i == 0:
				smiles = comp_dict[lig][i][0]
			else:
				rank1 = comp_dict[lig][i][1]
                        	es1 = comp_dict[lig][i][2]
                        	pol1 = comp_dict[lig][i][3]
                        	apol1 = comp_dict[lig][i][4]
                        	vdw1 = comp_dict[lig][i][5]
                        	gist1 = comp_dict[lig][i][6]

                        	rank2 = comp_dict[lig][i][7]
                        	es2 = comp_dict[lig][i][8]
                        	pol2 = comp_dict[lig][i][9]
                        	apol2 = comp_dict[lig][i][10]
                        	vdw2 = comp_dict[lig][i][11]
                        	gist2 = comp_dict[lig][i][12]
			
				if comptype[0] == "l":
					log_diff = math.log(rank2) - math.log(rank1)
				else:
					log_diff = math.log(rank1) - math.log(rank2)

				if comptype[0] == "l":
					diff = rank2 - rank1
				else:
					diff = rank1 - rank2

				if diff > 0:
					es_perc1, es_perc2, ld_perc1, ld_perc2, vdw_perc1, vdw_perc2, gist_perc1, gist_perc2 = calc_mag(es1, pol1, apol1, vdw1, gist1, es2, pol2, apol2, vdw2, gist2)	
					lig_rank_list.append([rank1, rank2])
					log_diff_list.append([diff, smiles, rank1, es_perc1, ld_perc1, vdw_perc1, rank2, es_perc2, ld_perc2, vdw_perc2, gist_perc1, gist_perc2, lig])


	log_P_list = []
	HAC_list = []
	rotB_list = []
	es_perc1_list = []
	es_perc2_list = []
	ld_perc1_list = []
	ld_perc2_list = []
	vdw_perc1_list = []
	vdw_perc2_list = []
	gist_perc1_list = []
	gist_perc2_list = []
	rank_list = []

	for lig in sorted(log_diff_list, reverse=True):
		diff = lig[0]
		smiles = lig[1]
		logp, hac, rotB = get_stuff(smiles)
		std_rank = lig[2]
		es_perc1 = lig[3]
		ld_perc1 = lig[4]
		vdw_perc1 = lig[5]

		es_perc1_list.append(es_perc1)
		ld_perc1_list.append(ld_perc1)
		vdw_perc1_list.append(vdw_perc1)
		
		gist_rank = lig[6]
		es_perc2 = lig[7]
		ld_perc2 = lig[8]
		vdw_perc2 = lig[9]

		gist_perc1 = lig[10]
		gist_perc2 = lig[11]

		gist_perc1_list.append(gist_perc1)
		gist_perc2_list.append(gist_perc2)

		es_perc2_list.append(es_perc2)
		ld_perc2_list.append(ld_perc2)
		vdw_perc2_list.append(vdw_perc2)

		lig_ID = lig[12]	
		
		HAC_list.append(hac)
		log_P_list.append(logp)
		rotB_list.append(rotB)
		rank_list.append([lig_ID, diff, std_rank, es_perc1, ld_perc1, vdw_perc1, gist_perc1, gist_rank, es_perc2, ld_perc2, vdw_perc2, gist_perc2,])
		#print(lig_ID, diff, std_rank, es_perc1, ld_perc1, vdw_perc1, gist_rank, es_perc2, ld_perc2, vdw_perc2)

	print("LogP Top 10")
	print(np.mean(log_P_list[:10]))
	print(np.std(log_P_list[:10]))

	#print("LogP Top 25")
	#print(np.mean(log_P_list[:25]))
	#print(np.std(log_P_list[:25]))

	#print("HAC Top 10")
	#print(np.mean(HAC_list[:10]))
	#print(np.std(HAC_list[:10]))

	#print("HAC Top 10")
	#print(np.mean(HAC_list[:25]))
	#print(np.std(HAC_list[:25]))

	#print("RotB Top 10")
	#print(np.mean(rotB_list[:10]))
	#print(np.std(rotB_list[:10]))

	#print("RotB Top 25")
	#print(np.mean(rotB_list[:25]))
	#print(np.std(rotB_list[:25]))

	if comptype[0] == "l": 
		print ("# Ligands that move down the rank list (get worse) is", len(log_diff_list))
	else:
		print ("# Decoys that move up the rank list (get better) is", len(log_diff_list))

	print ("Mean/STD of Top 10 STD ES_Perc:", np.mean(es_perc1_list[:10]), np.std(es_perc1_list[:10]))

	print ("Mean/STD of Top 10 STD LD_Perc:", np.mean(ld_perc1_list[:10]), np.std(ld_perc1_list[:10]))

	print ("Mean/STD of Top 10 STD vdW_Perc:", np.mean(vdw_perc1_list[:10]), np.std(vdw_perc1_list[:10]))

	print ("Mean/STD of Top 10 STD GIST_Perc:", np.mean(gist_perc1_list[:10]), np.std(gist_perc1_list[:10]))
	print (" ")

	print ("Mean/STD of Top 10 GIST ES_Perc:", np.mean(es_perc2_list[:10]), np.std(es_perc2_list[:10]))

	print ("Mean/STD of Top 10 GIST LD_Perc:", np.mean(ld_perc2_list[:10]), np.std(ld_perc2_list[:10]))

	print ("Mean/STD of Top 10 GIST vdW_Perc:", np.mean(vdw_perc2_list[:10]), np.std(vdw_perc2_list[:10]))

	print ("Mean/STD of Top 10 GIST GIST_Perc:", np.mean(gist_perc2_list[:10]), np.std(gist_perc2_list[:10]))

	for rank in rank_list[:10]:
		print(rank)
	#print ("Rank Changes:", rank_list[:10])

def main():

	pwd = os.getcwd()+"/"

	pdb = sys.argv[1]
	system = sys.argv[2]
	lig_or_decoy = sys.argv[3]

	new_pdbs = ['3M2W', '2OJG', '1LRU', '2AM9', '3G6Z', '3F07', '1J4H', '2ZEC', '3KRJ', '1SQT', '3HL5', '3C4F', '2ETR', '2HZI']

	lig_dict, dec_dict = fill_lig_dec_dicts(system)

	if pdb in new_pdbs:
		uniq_txt1 = "/mnt/nfs/work/rstein/RotationProjectDUDEGIST/"+pdb+"/ROC_ligdecoy/extract_all.sort.uniq.txt"
	else:
		#uniq_txt1 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"/ROC_ligdecoy/extract_all.sort.uniq.txt"
		uniq_txt1 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"/ROC_ligdecoy/extract_all.sort.uniq.txt"

	#weight_list = ["_es1pt0_v1pt0_ld0pt3", "_es1pt0_v1pt0_ld0pt5", "_es1pt0_v1pt0_ld0pt7"]

	#uniq_txt2 = pwd+pdb+"_full_parameter_scan/"+pdb+"_es1pt0_v1pt0_ld0pt5/ROC_ligdecoy/extract_all.sort.uniq.txt"		
	#uniq_txt2 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"_GIST/ROC_ligdecoy/extract_all.sort.uniq.txt"
	uniq_txt2 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"_GIST_0p5/ROC_ligdecoy/extract_all.sort.uniq.txt"
	#uniq_txt2 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"_GIST_0p5_truncate_3p0/ROC_ligdecoy/extract_all.sort.uniq.txt"
	lig_dict, dec_dict = collect_energies(uniq_txt1, uniq_txt2, lig_dict, dec_dict, "GIST")

	if lig_or_decoy[0] == "l":
		process_dict(lig_dict, "ligands")
	else:
		process_dict(dec_dict, "decoys")
			
main()
