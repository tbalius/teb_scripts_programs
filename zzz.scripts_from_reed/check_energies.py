import os, sys
import numpy as np
import math
import mol2


def read_in_dx_file(file):

  fileh = open(file,'r')

  flag_read_dx = False

  count = 0

  values = []
  for line in fileh:
      splitline = line.split()

      #print splitline
      #if len(splitline) < 2:
      if len(splitline) == 0:
          #print line
          continue

      ## this should be line 1
      if (splitline[0] == "object" and splitline[1] == "1"):
         print "count = ", count, " line = ", line
         xn = int(splitline[5])
         yn = int(splitline[6])
         zn = int(splitline[7])

      ## this should be line 2       
      if (splitline[0] == "origin"):
         #print line
         print "count = ", count, " line = ", line
         origin = [float(splitline[1]), float(splitline[2]), float(splitline[3])]

      ## this should be lines 3-5
      if (splitline[0] == "delta"):
         #print line
         print "count = ", count, " line = ", line
         if (float(splitline[2]) == 0 and  float(splitline[3]) ==0):
            dx = float(splitline[1])
         elif (float(splitline[1]) == 0 and  float(splitline[3]) ==0):
            dy = float(splitline[2])
         elif (float(splitline[1])== 0 and  float(splitline[2])==0):
            dz = float(splitline[3])
            print dx, dy, dz


      if (splitline[0] == "object" and splitline[1] == "2"):
         #print line
         print "count = ", count, " line = ", line
      if (splitline[0] == "object" and splitline[1] == "3"):
         #print line
         print "count = ", count, " line = ", line
         flag_read_dx = True
         continue # go to next line
      if (flag_read_dx):

         if (len(splitline) > 3):
            print "Error: dx formate problem. more than 3 colums"
            exit()

         for value in splitline:
             values.append(float(value))

      count = count + 1


  print len(values)
  fileh.close()
  return xn,yn,zn,dx,dy,dz,origin,values

def precompute_grids(xn, yn, zn, values):

        grid = []
        for i in range(xn):
            matrix = []
            for j in range(yn):
                row = []
                for k in range(zn):
                    row.append(0)
                matrix.append(row)
            grid.append(matrix)

        index = 0
        for i in range(xn):
            for j in range(yn):
                for k in range(zn):
                    grid[i][j][k] = values[index]
                    index = index + 1

        grid_precomp = []
        for i in range(xn):
            matrix = []
            for j in range(yn):
                row = []
                for k in range(zn):
                    a_array = [] # a1 through a8 for precomputing
                    for l in range(8):
                       a_array.append(0)
                    row.append(a_array)
                matrix.append(row)
            grid_precomp.append(matrix)

        for i in range(xn-1):
                for j in range(yn-1):
                        for k in range(zn-1):
                                a8 = grid[i][j][k]
                                a7 = grid[i][j][k+1] - a8
                                a6 = grid[i][j+1][k] - a8
                                a5 = grid[i+1][j][k] - a8
                                a4 = grid[i][j+1][k+1] - a7 - grid[i][j+1][k]
                                a3 = grid[i+1][j][k+1] - a7 - grid[i+1][j][k]
                                a2 = grid[i+1][j+1][k] - a6 - grid[i+1][j][k]
                                a1 = grid[i+1][j+1][k+1] - a4 - grid[i+1][j][k+1] + grid[i+1][j][k] - grid[i+1][j+1][k]

                                grid_precomp[i][j][k][0] = a1
                                grid_precomp[i][j][k][1] = a2
                                grid_precomp[i][j][k][2] = a3
                                grid_precomp[i][j][k][3] = a4
                                grid_precomp[i][j][k][4] = a5
                                grid_precomp[i][j][k][5] = a6
                                grid_precomp[i][j][k][6] = a7
                                grid_precomp[i][j][k][7] = a8

        return(grid_precomp)


def calc_score(mol, origin, gridscale, xn, yn, zn, grid_hydrogen_precomp, grid_heavy_precomp):

	hydr_value = 0
	heavy_value = 0
	electro = 0
	for atom_i,atom in enumerate(mol.atom_list):
	        x_int = (atom.X - origin[0]) / gridscale
	        y_int = (atom.Y - origin[1]) / gridscale
	        z_int = (atom.Z - origin[2]) / gridscale
	
	        nx = int(x_int)
	        ny = int(y_int)
	        nz = int(z_int)
	
	        xgr = x_int - float(nx)
	        ygr = y_int - float(ny)
	        zgr = z_int - float(nz)
	
	        if atom.name[0] == "H":
	                a8 = grid_hydrogen_precomp[nx][ny][nz][7]
	                a7 = grid_hydrogen_precomp[nx][ny][nz][6]
	                a6 = grid_hydrogen_precomp[nx][ny][nz][5]
	                a5 = grid_hydrogen_precomp[nx][ny][nz][4]
	                a4 = grid_hydrogen_precomp[nx][ny][nz][3]
	                a3 = grid_hydrogen_precomp[nx][ny][nz][2]
	                a2 = grid_hydrogen_precomp[nx][ny][nz][1]
	                a1 = grid_hydrogen_precomp[nx][ny][nz][0]
	
	                value = a1*xgr*ygr*zgr + a2*xgr*ygr + a3*xgr*zgr + a4*ygr*zgr + a5*xgr + a6*ygr + a7*zgr + a8
	
	                hyd_value = float(value * -1.0 * 0.125)
	                hydr_value += hyd_value
	                electro += hyd_value
	
	        else:
	                a8 = grid_heavy_precomp[nx][ny][nz][7]
	                a7 = grid_heavy_precomp[nx][ny][nz][6]
	                a6 = grid_heavy_precomp[nx][ny][nz][5]
	                a5 = grid_heavy_precomp[nx][ny][nz][4]
	                a4 = grid_heavy_precomp[nx][ny][nz][3]
	                a3 = grid_heavy_precomp[nx][ny][nz][2]
	                a2 = grid_heavy_precomp[nx][ny][nz][1]
	                a1 = grid_heavy_precomp[nx][ny][nz][0]
	
	                value = a1*xgr*ygr*zgr + a2*xgr*ygr + a3*xgr*zgr + a4*ygr*zgr + a5*xgr + a6*ygr + a7*zgr + a8
	
	                hvy_value = float(value * -1.0 * 0.125)
	                heavy_value += hvy_value
	                electro += hvy_value
	
	return(electro)


def collect_energies(mol2file):

	energy_dict = {}

	open_mol2 = open(mol2file, 'r')
        read_mol2 = open_mol2.readlines()
        open_mol2.close()

        comp_found = False
        for line in read_mol2:
                splitline = line.strip().split()
                if len(splitline) > 1:
                        if splitline[0] == "##########":
                                if splitline[1] == "Name:":
                                        comp_name = splitline[2]
					energy_dict[comp_name] = []
                                        comp_found = True

				if splitline[1] == "Electrostatic:":
					energy_dict[comp_name].append(float(splitline[2]))

				if splitline[1] == "Van":
					energy_dict[comp_name].append(float(splitline[4]))
					
				if splitline[1] == "Ligand" and splitline[2] == "Polar":
					energy_dict[comp_name].append(float(splitline[4]))
				
				if splitline[1] == "Ligand" and splitline[2] == "Apolar":
					energy_dict[comp_name].append(float(splitline[4]))

                                if comp_found == True and splitline[1] == "Receptor" and splitline[2] == "Desolvation:":
                                        energy_dict[comp_name].append(float(splitline[3]))
                                        comp_found = False

	return(energy_dict)

def sum_vals(energy_list):

	sum_val = 0
	for i in range(len(energy_list)):
		sum_val += energy_list[i]

	return(sum_val)


def main():


	pwd = os.getcwd()+"/"

	ori_dir = sys.argv[1]
	tbGIST_dir = sys.argv[2]

	#ori_mol2 = "/mnt/nfs/work/tbalius/Water_Project_DUDE/"+pdb+"/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#ori_mol2 = "/mnt/nfs/export/rstein/Ligand_Generation/"+pdb+"_testing/"+pdb+"_std_min/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#ori_mol2 = "/mnt/nfs/work/rstein/DUDE_MIN/"+pdb+"_min/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#ori_mol2 = "/mnt/nfs/work/rstein/ampc_preparation/11-16_2017_for_bGIST/1L2S_dist0pt5_size0pt6/ligands-decoys/ligands/allChunksCombined/poses.mol2"

	ori_mol2 = pwd+ori_dir+"/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	tbGIST_mol2 = pwd+tbGIST_dir+"/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#ori_mol2 = pwd+"1L2S_tart1_thin_spheres_5000_min/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#ori_mol2 = pwd+"1L2S_tart1_thin_spheres_min_top_10/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#tbGIST_mol2 = pwd+"1L2S_tart1_thin_spheres_tbGIST_min_top_10/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#tbGIST_mol2 = pwd+"1L2S_tart1_thin_spheres_tbGIST_5000_min/ligands-decoys/ligands/allChunksCombined/poses.mol2"

	#tbGIST_mol2 = "/mnt/nfs/work/rstein/Big_Blurry/"+pdb+"_truncate_blurry_spheres/"+pdb+"_sig_2_gist_rad_1pt8_1pt0_min/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#tbGIST_mol2 = "/mnt/nfs/work/rstein/ampc_preparation/11-16_2017_for_bGIST/1L2S_dist0pt5_size0pt6_tbGIST/ligands-decoys/ligands/allChunksCombined/poses.mol2"
	#tbGIST_mol2 = "/mnt/nfs/export/rstein/DUDE_Z/"+pdb+"_testing/"+pdb+"_tbGIST_std/ligands-decoys/ligands/allChunksCombined/poses.mol2"

	hydrogen_truncated_gist_grid = "/mnt/nfs/work/rstein/ampc_preparation/11-16_2017_for_bGIST/1L2S_dist0pt5_size0pt6_tbGIST/dockfiles/Sig_2_GIST_1pt0_gaussian.dx"
	heavy_truncated_gist_grid = "/mnt/nfs/work/rstein/ampc_preparation/11-16_2017_for_bGIST/1L2S_dist0pt5_size0pt6_tbGIST/dockfiles/Sig_2_GIST_1pt8_gaussian.dx"
	#hydrogen_truncated_gist_grid = "/mnt/nfs/export/rstein/Ligand_Generation/"+pdb+"_testing/"+pdb+"_tbGIST_std/dockfiles/Sig_2_GIST_1pt0_gaussian.dx"
	#heavy_truncated_gist_grid = "/mnt/nfs/export/rstein/Ligand_Generation/"+pdb+"_testing/"+pdb+"_tbGIST_std/dockfiles/Sig_2_GIST_1pt8_gaussian.dx"

	xn1,yn1,zn1,dx1,dy1,dz1,origin1,values1 = read_in_dx_file(hydrogen_truncated_gist_grid)
        xn2,yn2,zn2,dx2,dy2,dz2,origin2,values2 = read_in_dx_file(heavy_truncated_gist_grid)

        grid_hydrogen_precomp = precompute_grids(xn1, yn1, zn1, values1)
        grid_heavy_precomp = precompute_grids(xn2, yn2, zn2, values2)
        gridscale = dx1

	energy_dict1 = collect_energies(ori_mol2)
	energy_dict2 = collect_energies(tbGIST_mol2)

   	mols  = mol2.read_Mol2_file(ori_mol2)
   	#mols  = mol2.read_Mol2_file(tbGIST_mol2)

	count = 0
	diff_energy = []
	for mol in mols:
		mol_name = mol.name
		if (mol_name in energy_dict1) and (mol_name in energy_dict2):
			print(mol_name)
			gist_val = calc_score(mol, origin1, gridscale, xn1, yn1, zn1, grid_hydrogen_precomp, grid_heavy_precomp)
			ori_std_pose_energy = sum_vals(energy_dict1[mol_name])
			std_pose_energy = ori_std_pose_energy + gist_val
			gist_pose_energy = sum_vals(energy_dict2[mol_name])
			diff = gist_pose_energy - std_pose_energy
			if diff > 0.001:
				print(mol_name, ori_std_pose_energy, gist_val, std_pose_energy, gist_pose_energy, diff)	
				count += 1
				diff_energy.append(diff)
			#elif diff < -0.001:
			#	print("NEGATIVE DIFF")
			#	print(mol_name, ori_std_pose_energy, gist_val, std_pose_energy, gist_pose_energy, diff)	

	print(np.mean(diff_energy), np.std(diff_energy))
	print(count)
	




main()
