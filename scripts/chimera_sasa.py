from chimera import openModels, Molecule, runCommand
import sys

# This script will calculate the SASA (Solvent Accesible Surface Area) using the program Chimera.
# It calculates SASA for Receptor, ligand, and complex and retruns the change(delta) in SASA. 
# Writen by Trent E Balius, Shoichet Lab, 2013
# modified from http://plato.cgl.ucsf.edu/pipermail/chimera-users/2011-January/005954.html


def cal_SASA(input_pdb,output_prefix):

  print "pdb inputs    = " + input_pdb 
  print "output prefix = " + output_prefix
  
  model = openModels.open(input_pdb) 
  runCommand("surf :all")
  out = open(output_prefix + "sasa.txt", "w")
  x = '---------------------------------------------------------------------------------\n'
  print "list " + str(list(model))
  for m in openModels.list(modelTypes=[Molecule]):
    msas = 0
    for r in m.residues:
      try:
          sas = r.areaSAS
      except AttributeError:
          continue
      msas = msas + sas
      out.write('%s,%f\n' % (r, sas))
    out.write(x)
    out.write('%s,%f\n' % (m, msas))
    out.write('\n')
  out.close()
  runCommand("del")
  print msas
  return msas


def main():
  print sys.argv
  if len(sys.argv) != 5: # if no input
     print "ERROR: Wrong number of inputs"
     print "syntax: chimera --nogui --script chimera_sasa.py rec.pdb lig.pdb com.pdb output_prefix"
     print len(sys.argv)
     return

  #models = openModels.list(modelTypes=[chimera.Molecule])

  input_rec_pdb = sys.argv[1]
  input_lig_pdb = sys.argv[2]
  input_com_pdb = sys.argv[3]
  output_prefix = sys.argv[4]

  print "pdb inputs = " + input_rec_pdb +","+ input_lig_pdb +","+ input_com_pdb
  print "output prefix = " + output_prefix

  r_sasa = cal_SASA(input_rec_pdb,output_prefix+'.rec')
  l_sasa = cal_SASA(input_lig_pdb,output_prefix+'.lig')
  c_sasa = cal_SASA(input_com_pdb,output_prefix+'.com')
  d_sasa = c_sasa - (r_sasa + l_sasa) 

  print (" rec SASA   = %f\n lig SASA   = %f\n comp SASA  = %f\n delta SASA = %f\n " % (r_sasa, l_sasa, c_sasa, d_sasa))

main()
