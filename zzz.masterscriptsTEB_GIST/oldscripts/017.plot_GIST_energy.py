import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab
from pylab import *

def plot_hist(energy_file, system):

        energy_file = open(energy_file)
        energylines = energy_file.readlines()
        energy_file.close()
        ligand_energy_list = []
	decoy_energy_list = []

        for line in energylines:
                line = line.strip().split()
		if line[0][-8:] == "_ligands":
			lig_energy = float(line[2])
                	ligand_energy_list.append(lig_energy)
		elif line[0][-7:] == "_decoys":
			dec_energy = float(line[2])
			decoy_energy_list.append(dec_energy)

        #mu = np.mean(rmsd_list)
        #sigma = np.std(rmsd_list)
        #x = mu + sigma*np.random.randn(10000)
        num_bins = 20
        f, axarr = plt.subplots(4)
	#axarr[0, 0].plot(x, y)
	#axarr[0, 0].set_title('Axis [0,0]')
	#axarr[0, 1].scatter(x, y)
	#axarr[0, 1].set_title('Axis [0,1]')
	#axarr[1, 0].plot(x, y ** 2)
	#axarr[1, 0].set_title('Axis [1,0]')
	#axarr[1, 1].scatter(x, y ** 2)
	#axarr[1, 1].set_title('Axis [1,1]')
        n, bins, patches = axarr[0].hist(ligand_energy_list, num_bins)
        n2, bins2, patches2 = axarr[1].hist(decoy_energy_list, num_bins)
        mu = np.mean(decoy_energy_list)
        sigma = np.std(decoy_energy_list)
	y = mlab.normpdf(bins2, mu, sigma)
        r = np.random.uniform(-15,15,1000)
  #      print r
        n3, bins3, patches3 = axarr[2].hist(r, num_bins)
 #       print n,bins,patches
        s1 = sum(n)
        s2 = sum(n2)
        s3 = sum(n3)
        meanbins = []
        for i in range(1,len(bins)):
            meanbins.append((bins[i]+bins[i-1])/2.0)
        meanbins2 = []
        for i in range(1,len(bins2)):
            meanbins2.append((bins2[i]+bins2[i-1])/2.0)
        meanbins3 = []
        for i in range(1,len(bins3)):
            meanbins3.append((bins3[i]+bins3[i-1])/2.0)
	print(meanbins)
	print(meanbins2)
	print(meanbins3)
#	print len(n),len(bins),len(patches)
        axarr[3].plot(meanbins,n/s1,'r-',meanbins2,n2/s2,'g-',meanbins3,n3/s3,'y-',bins2,y,'k--')
        #plt.plot(bins, y, 'r--')
        #pylab.xlabel('GIST Energy')
        #pylab.ylabel('Count')
        #pylab.title(system)
        plt.subplots_adjust(left=0.15)
       	#plt.show()
        #plt.savefig(system+"energy_GISTogram.png",dpi=1000)
        os.system("pwd")
	plt.savefig(system+"_energy_GISTogram.png")
	plt.clf()	



def main():
        #pwd = "/mnt/nfs/work/rstein/RotationProjectDUDEGIST/"
        #pwd = "/mnt/nfs/work/fischer/ucsf/postdoc/hsp/1YESdocking/"
	pwd = "/mnt/nfs/work/fischer/ucsf/postdoc/tutorialEtc/tutorial_scripts/"

        #sys_dict = {"ampC":["1L2S_10-22_GIST"],"HSP90":["1UYG_12-4_GIST"],"NA":["1B9V_10-22_GIST"],"FA10":["3KL6_11-15_GIST"],"ACES":["1E66_10-22_GIST"],"HIVPR":["1XL2_aligned_10-22_GIST"],
        #"PUR2":["1NJS_10-22_GIST"],"EGFR":["2RGP_TKD_aligned_10-22_GIST"],"HMDH":["3CCW_10-22_GIST"],"TRYP":["2AYW_10-22_GIST"]}

	sys_dict = {"CcPgaApo":["docking/2runEnrich/4NVA_gist/"]}


        comp_type = ["ligands","decoys"]


        for sys in sys_dict:

		new_file = pwd+sys+"_GIST_energies"
        	output = open(new_file, "w")
        	output.write("%-25s%15s%15s"% ("SYSTEM","COMPOUND","GIST_ENERGY\n"))
                
		sys_len = len(sys_dict[sys]) # another for loop can be added if you want to calculate averages for GIST weightings/approximations
                docktype = sys_dict[sys][0]


                for subtype in comp_type:
                        path = pwd+docktype+subtype+"/allChunksCombined/" # go to path where extract all text file is located for ligands and decoys
                        os.chdir(path)
                        uniq_txt = open(path+"extract_all.sort.uniq.txt")
                        uniq_txt_read = uniq_txt.readlines()
                        uniq_txt.close()
                        
			ls = []
                        for line in uniq_txt_read:
                                line = line.strip().split()
                                ls.append([line[2],float(line[13])]) # append the GIST energy to the list

			for line in ls:
				output.write('%-25s%15s%15s\n'%(sys+"_"+subtype,line[0],line[1]))

		os.chdir(pwd)	
        	output.close()

		plot_hist(new_file, sys)
main()
