
open working/rec.crg.pdb 
open working/xtal-lig.pdb 

display #0 & #1 z < 3.5
~ribbon

represent wire #0
linewidth 5 #0

represent wire #1 
#viewdock vs_frags-now-marvin/top.1000.mol2
viewdock vs_leads-now-marvin/top.1000.mol2
#viewdock vs_natural-products/top.1000.mol2
findhbond intermodel true spec #0,2
