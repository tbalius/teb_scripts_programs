
#set clustertype = "complete_4.0_sieve10"
 set clustertype = "4.0_mod"
#set clustertype = "single_1.0_sieve10"

 set clusterdir = 009.clustering_${clustertype}
 set rmsddir    = 010.rmsd_${clustertype}/

 paste  ${clusterdir}/cnumvtime.dat ${rmsddir}/lig1.dat | awk '{print $2,$4}' > cnumvrmsd_${clustertype}.dat

 python 011.plot_cluster_rmsd.py cnumvrmsd_${clustertype}.dat cnumvrmsd_${clustertype} cnumvrmsd_${clustertype}  

