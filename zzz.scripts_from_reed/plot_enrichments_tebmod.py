import os
import os.path
import mol2
import sys
import pylab
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


def assign_color(gist_col,gist_val, std_val):
	diff = float(gist_val) - float(std_val)
        if diff > 1:
        	gist_col += 'g'
        elif diff <= 1 and diff > 0:
        	gist_col += 'y'
        elif diff < 0 and diff > -1:
        	gist_col += 'DarkOrange'
        elif diff < -1 and diff >= -3:
        	gist_col += 'r'
	elif diff <= -3:
		gist_col += 'm'
	return(gist_col)


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


def main():

#	sys_dict = {["ampC"]:['10.9','9.08','11.76','10.94','10.21','9.89','9.44'],["HSP90"]:['10.7','17.84','15.87','20.42','21.55','20.94','19.69'],["NA"]:['11.5','20.28','5.65','14.67','17.63','18.73','19.71']}
	#sys_dict = {"ampC":['10.9','9.08','9.02','10.94','10.21','9.89','9.44']}
	
	#pwd = "/mnt/nfs/work/rstein/RotationProjectDUDEGIST/"
	pwd = "/nfs/home/tbalius/work/Water_Project_all_in_the_same_frame_ph4/workingdir/align_"

	#sys_dict = {"ampC":['1L2S_10-22','1L2S_10-22_GIST','1L2S_10-22_GIST_0.5','1L2S_10-22_GIST_0.3','1L2S_10-22_GIST_0.2','1L2S_10-22_GIST_0.1'], 
	#"NA":['1B9V_10-22','1B9V_10-22_GIST','1B9V_10-22_GIST_0.5','1B9V_10-22_GIST_0.3','1B9V_10-22_GIST_0.2','1B9V_10-22_GIST_0.1'],
	#"HSP90":['1UYG_12-4','1UYG_12-4_GIST','1UYG_12-4_GIST_0.5','1UYG_12-4_GIST_0.3','1UYG_12-4_GIST_0.2','1UYG_12-4_GIST_0.1'],
	#"PUR2":['1NJS_10-22','1NJS_10-22_GIST','1NJS_10-22_GIST_0.5','1NJS_10-22_GIST_0.3','1NJS_10-22_GIST_0.2','1NJS_10-22_GIST_0.1'],
	#"HIVPR":['1XL2_aligned_10-22','1XL2_aligned_10-22_GIST','1XL2_aligned_10-22_GIST_0.5','1XL2_aligned_10-22_GIST_0.3','1XL2_aligned_10-22_GIST_0.2','1XL2_aligned_10-22_GIST_0.1'],
	#"TRYP":['2AYW_10-22','2AYW_10-22_GIST','2AYW_10-22_GIST_0.5','2AYW_10-22_GIST_0.3','2AYW_10-22_GIST_0.2','2AYW_10-22_GIST_0.1'],
	#"EGFR":['2RGP_TKD_aligned_10-22','2RGP_TKD_aligned_10-22_GIST','2RGP_TKD_aligned_10-22_GIST_0.5','2RGP_TKD_aligned_10-22_GIST_0.3','2RGP_TKD_aligned_10-22_GIST_0.2','2RGP_TKD_aligned_10-22_GIST_0.1'],
	#"HMDH":['3CCW_10-22','3CCW_10-22_GIST','3CCW_10-22_GIST_0.5','3CCW_10-22_GIST_0.3','3CCW_10-22_GIST_0.2','3CCW_10-22_GIST_0.1'],
	#"KITH":['2B8T_12-4','2B8T_12-4_GIST','2B8T_12-4_GIST_0.5','2B8T_12-4_GIST_0.3','2B8T_12-4_GIST_0.2','2B8T_12-4_GIST_0.1'],
	#"FA10":['3KL6_11-15','3KL6_11-15_GIST','3KL6_11-15_GIST_0.5','3KL6_11-15_GIST_0.3','3KL6_11-15_GIST_0.2','3KL6_11-15_GIST_0.1'],
	#"AA2AR":['3EML_aligned_10-22','3EML_aligned_10-22_GIST','3EML_aligned_10-22_GIST_0.5','3EML_aligned_10-22_GIST_0.3','3EML_aligned_10-22_GIST_0.2','3EML_aligned_10-22_GIST_0.1'],
	#"ACES":['1E66_10-22','1E66_10-22_GIST','1E66_10-22_GIST_0.5','1E66_10-22_GIST_0.3','1E66_10-22_GIST_0.2','1E66_10-22_GIST_0.1'], 
	#"THRB":['1YPE_12-4','1YPE_12-4_GIST','1YPE_12-4_GIST_0.5','1YPE_12-4_GIST_0.3','1YPE_12-4_GIST_0.2','1YPE_12-4_GIST_0.1'],
	#"ADA":['2E1W_12-12','2E1W_12-12_GIST','2E1W_12-12_GIST_0.5','2E1W_12-12_GIST_0.3','2E1W_12-12_GIST_0.2','2E1W_12-12_GIST_0.1']}
	
	sys_dict = { 
        "CcP_A":['DOCKING_standard','DOCKING_gist-EswPlusEww_ref2','DOCKING_gist-EswPlusEww_ref2_scale-0.5','DOCKING_gist-EswPlusEww_ref2_scale-0.3','DOCKING_gist-EswPlusEww_ref2_scale-0.2','DOCKING_gist-EswPlusEww_ref2_scale-0.1'],
        "CcP_B":['DOCKING_standard','DOCKING_gist-EswPlusEww_ref2','DOCKING_gist-EswPlusEww_ref2_scale-0.5','DOCKING_gist-EswPlusEww_ref2_scale-0.3','DOCKING_gist-EswPlusEww_ref2_scale-0.2','DOCKING_gist-EswPlusEww_ref2_scale-0.1'],
        "CcP_C":['DOCKING_standard','DOCKING_gist-EswPlusEww_ref2','DOCKING_gist-EswPlusEww_ref2_scale-0.5','DOCKING_gist-EswPlusEww_ref2_scale-0.3','DOCKING_gist-EswPlusEww_ref2_scale-0.2','DOCKING_gist-EswPlusEww_ref2_scale-0.1'],
        "CcP_D":['DOCKING_standard','DOCKING_gist-EswPlusEww_ref2','DOCKING_gist-EswPlusEww_ref2_scale-0.5','DOCKING_gist-EswPlusEww_ref2_scale-0.3','DOCKING_gist-EswPlusEww_ref2_scale-0.2','DOCKING_gist-EswPlusEww_ref2_scale-0.1']
        }

	#val_dict = {"ampC":[10.9]}
	val_dict = {
        "CcP_A":[0.0],
        "CcP_B":[0.0],
        "CcP_C":[0.0],
        "CcP_D":[0.0]
        }
	
	decoytype = "decoys"
	#decoytype = "known-non-binders"
	for key in sys_dict:
		key_len = len(sys_dict[key])
		docktype = sys_dict[key]
		for subtype in docktype:
			new_dir = pwd+key+'/'+subtype+"/ROC_lig-ligands_dec-"+decoytype+"/"
			open_file = open(new_dir+"roc_own.txt")
			read_file = open_file.readlines()
			open_file.close()
			
			for line in read_file:
				line = line.strip().split()
				if line[0] == '#AUC':
					val_dict[key].append(float(line[3]))

	print(val_dict)
			
		
	#gist_dict = {"2":['GIST','gist_col'],"3":['GIST_0.5','gist_05_col'],"4":['GIST_0.3','gist_03_col'],"5":['GIST_0.2','gist_02_col'],"6":['GIST_0.1','gist_01_col']}

	for key in val_dict.keys():
		enrich_list = []
		labels = []
		cole_list = []
		std_list = []
		gist_list = []
		gist_col = ''
        	gist_05_list = []
		gist_05_col = ''
        	gist_03_list = []
		gist_03_col = ''
        	gist_02_list = []
		gist_02_col = ''
        	gist_01_list = []
		gist_01_col = ''
        	std_enrich = []
		print key
                print val_dict[key]
		for i,val in enumerate(val_dict[key]):
                        print i,val
			enrich_list.append(float(val))	
			if i == 0:
				cole_list.append(float(val))
				labels.append("Coleman")
			elif i == 1:
				std_list.append(float(val))
				labels.append("Standard")
				std_enrich.append(float(val))
			
			#for ind in gist_dict:
			#	if i == ind:
			#		print(str(i))
			#		print(int(i))
			#		print(ind)
			#		gist_val = float(val)
			#		print(gist_dict[ind][0])
			#		label = gist_dict[ind][0]
			#		gist_col = gist_dict[ind][1]
			#		print(gist_col)
			#		labels.append(label)
			#		gist_dict[ind][1] = assign_color(gist_col,gist_val,std_enrich[0])
			#		stuff.append(0.15+float(i)*0.15, gist_list, 0.15)
			#ax.bar(
			elif i == 2:
				gist_list.append(float(val))
				labels.append("GIST")
				gist_val = float(val)
				gist_col = assign_color(gist_col,gist_val,std_enrich[0])			
			elif i == 3:
				gist_05_list.append(float(val))
				labels.append("GIST_0.5")
				gist_val = float(val)
		  		gist_05_col = assign_color(gist_05_col,gist_val,std_enrich[0])
			elif i == 4:
				gist_03_list.append(float(val))
				labels.append("GIST_0.3")
				gist_val = float(val)
				gist_03_col = assign_color(gist_03_col,gist_val,std_enrich[0])
			elif i == 5:
				gist_02_list.append(float(val))
				labels.append("GIST_0.2")
				gist_val = float(val)
				gist_02_col = assign_color(gist_02_col,gist_val,std_enrich[0])
			elif i == 6:
				gist_01_list.append(float(val))
				labels.append("GIST_0.1")
				gist_val = float(val)
				gist_01_col = assign_color(gist_01_col,gist_val,std_enrich[0])	
			else:
				print("something is wronG!!!!!")
				return	

		print gist_list
		fig = plt.figure(figsize=(8,8))
		fig.subplots_adjust(bottom=0.2)
		ax = fig.add_subplot(111)
		#matplotlib.rcParams['xtick.labelsize'] = 20
		pylab.xlabel("Docking Type")
		pylab.ylabel("Log AUC")
		pylab.title(key+" "+decoytype+" Enrichments")
		#x = range(len(enrich_list))
		width = 0.15
		xticks = [(width+0.5*width),2*width+0.5*width,3*width+0.5*width,4*width+0.5*width,5*width+0.5*width,6*width+0.5*width,7*width+0.5*width]
	#	matplotlib.rc('xtick', labelsize=20)
		plt.xticks(xticks, labels, rotation='vertical',fontsize=20)
		rects0 = ax.bar(width, cole_list, width, color="LightGray")
		rects1 = ax.bar(2*width, std_list, width, color="w")
		rects2 = ax.bar(width+2*width, gist_list, width, color=gist_col)
		rects3 = ax.bar(width+3*width, gist_05_list, width, color=gist_05_col)
		rects4 = ax.bar(width+4*width, gist_03_list, width, color=gist_03_col)
		rects5 = ax.bar(width+5*width, gist_02_list, width, color=gist_02_col)
		rects6 = ax.bar(width+6*width, gist_01_list, width, color=gist_01_col)
		#rects = [rects0, rects1, rects2, rects3, rects4, rects5, rects6]
		
		rects = ax.patches
	
		for rect in rects:
   			height = rect.get_height()
    			ax.text(rect.get_x() + rect.get_width()/2, height/2, str(height), ha='center', va='bottom',fontsize=20)	
	


		#plt.bar(x, enrich_list, width, color=color, align='center')
		pylab.savefig(key+"_"+decoytype+"_enrichments.png", dpi=1000)
		#plt.show()

main()
