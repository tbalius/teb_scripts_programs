import sys, os


def make_sph_dirs(pwd, ori_pdb_dir, new_dir):

	ori_dockfiles = ori_pdb_dir+"/dockfiles/"

	os.chdir(new_dir)
	os.system("ln -s "+ori_pdb_dir+"/INDOCK .")
	os.chdir(new_dir+"/dockfiles/")
	os.system("ln -s "+ori_dockfiles+"ligand.desolv.heavy .")
	os.system("ln -s "+ori_dockfiles+"ligand.desolv.hydrogen .")
	os.system("cp "+ori_dockfiles+"matching_spheres.sph ori_matching_spheres.sph")
	os.system("ln -s "+ori_dockfiles+"trim.electrostatics.phi .")
	os.system("ln -s "+ori_dockfiles+"vdw.bmp .")
	os.system("ln -s "+ori_dockfiles+"vdw.parms.amb.mindock .")
	os.system("ln -s "+ori_dockfiles+"vdw.vdw .")
	
	os.chdir(pwd)



def main():

	if len(sys.argv) != 4:
		print "ERROR: Input directory path, number of sphere sets to generate, and sphere spacing"

	pdb_code = sys.argv[1]
	dir_num = int(sys.argv[2])
	spacing = float(sys.argv[3])

	pwd = os.popen("pwd")
        pwd_list = []

        for p in pwd:
                p = p.strip().split()[0]
                pwd_list.append(p)
        pwd = pwd_list[0]+"/"	

	ori_pdb_dir = pwd+pdb_code

	for num in range(dir_num):
		print(num)
		new_dir = pwd+pdb_code+"_rand_sph_"+str(num)
		new_dock_dir = new_dir+"/dockfiles/"
		os.system("mkdir "+new_dir)
		os.system("mkdir "+new_dock_dir)
		make_sph_dirs(pwd, ori_pdb_dir, new_dir)	
		os.system("python make_random_sph.py "+new_dock_dir+"/ori_matching_spheres.sph "+spacing+" "+new_dock_dir+"/matching_spheres.sph")	

main()
	
