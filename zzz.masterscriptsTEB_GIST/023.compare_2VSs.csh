
#source /nfs/soft/python/envs/complete/latest/env.csh

#csh 023.compare_2VSs.csh
#/nfs/soft/python/envs/complete/python-2.7.7/lib/python2.7/site-packages/matplotlib/collections.py:548: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
#  if self._edgecolors == 'face':

source /nfs/home/tbalius/zzz.virtualenvs/virtualenv-1.9.1/myVEonGimel/bin/activate.csh


set mountdir = `pwd`

set vs1    = vs_gist
set vs2    = vs_nogist
set label1 = gist
set label2 = nogist
set tval   = 0.5 # portion of histogram shown in inset


set workdir = $mountdir/023.comparision_${vs1}_${vs2}

if (-e $workdir) then
   echo "$workdir exists" 
   exit
endif

mkdir -p $workdir
cd $workdir



#if !( -e ${vs1}/extract_all.sort.uniq.txt.ori ) then
#   echo moving ${vs1}/extract_all.sort.uniq.txt
#   mv ${vs1}/extract_all.sort.uniq.txt ${vs1}/extract_all.sort.uniq.txt.ori
#   python process.extract.include.list.py noO-C=O.${vs1}.txt ${vs1}/extract_all.sort.uniq.txt.ori ${vs1}/extract_all.sort.uniq.txt
#else 
#   echo "${vs1}/extract_all.sort.uniq.txt.ori exists"
#endif
#
#if !( -e ${vs2}/extract_all.sort.uniq.txt.ori ) then
#   echo moving ${vs2}/extract_all.sort.uniq.txt
#   mv ${vs2}/extract_all.sort.uniq.txt ${vs2}/extract_all.sort.uniq.txt.ori
#   python process.extract.include.list.py noO-C=O.${vs1}.txt ${vs2}/extract_all.sort.uniq.txt.ori ${vs2}/extract_all.sort.uniq.txt
#else 
#   echo "${vs2}/extract_all.sort.uniq.txt.ori exists"
#endif

python ${mountdir}/for023.plot_rank_energy_compare.py ${mountdir}/${vs1}/extract_all.sort.uniq.txt ${mountdir}/${vs2}/extract_all.sort.uniq.txt >! ${label1}_${label2}_1.log

python ${mountdir}/for023.plot_rank_energy_compare2.py ${mountdir}/${vs1}/extract_all.sort.uniq.txt ${mountdir}/${vs2}/extract_all.sort.uniq.txt ${label1} ${label2} ${tval} >! ${label1}_${label2}_2.log

python ${mountdir}/for023.get_list_log10rankchange.py ${mountdir}/${vs1}/extract_all.sort.uniq.txt ${mountdir}/${vs2}/extract_all.sort.uniq.txt ${tval}

#mv rankchangebeter1.txt ${run1}_${run2}_rankchangebeter1.txt
#mv rankchangebeter2.txt ${run1}_${run2}_rankchangebeter2.txt
#mv rankonly1.txt        ${run1}_${run2}_rankonly1.txt
#mv rankonly2.txt        ${run1}_${run2}_rankonly2.txt

awk -F, '{print $1}' rankchangebetter1.txt >! rankchangebetter1_list.txt
awk -F, '{print $1}' rankchangebetter2.txt >! rankchangebetter2_list.txt

foreach run ($vs1 $vs2)

cd ${mountdir}/${run}
python ${mountdir}/for023.remove_zincid_from_extract_all.py extract_all.sort.uniq.txt $workdir/rankchangebetter1_list.txt
mv extract_all.sort.uniq_new.txt ${label2}_compounds_from-${run}-with_LogRankDiff.txt

python ${mountdir}/for023.remove_zincid_from_extract_all.py extract_all.sort.uniq.txt $workdir/rankchangebetter2_list.txt
mv extract_all.sort.uniq_new.txt ${label1}_compounds_from-${run}-with_LogRankDiff.txt

wc -l $workdir/rankchangebetter1_list.txt
wc -l $workdir/rankchangebetter2_list.txt

$DOCKBASE/analysis/getposes.py -l 5000 -x 1 -f ${label2}_compounds_from-${run}-with_LogRankDiff.txt -o ${label2}_compounds_from-${run}-with_LogRankDiff.mol2
$DOCKBASE/analysis/getposes.py -l 5000 -x 1 -f ${label1}_compounds_from-${run}-with_LogRankDiff.txt -o ${label1}_compounds_from-${run}-with_LogRankDiff.mol2

mv ${label2}_compounds_from-${run}-with_LogRankDiff.txt ${label2}_compounds_from-${run}-with_LogRankDiff.mol2 ${label1}_compounds_from-${run}-with_LogRankDiff.txt ${label1}_compounds_from-${run}-with_LogRankDiff.mol2 $workdir/.

end


