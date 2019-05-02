""" Receiver Operating Characteristic Curve
"""
from __future__ import print_function
import os,sys
import numpy as np
from scipy import interp
from scipy import stats

from argparse import ArgumentParser
from collections import defaultdict
from subprocess import call

import matplotlib  # must import first
matplotlib.use('Agg')  # allows you to not have an x-server running
import matplotlib.pyplot as plt
import pylab

parser = ArgumentParser(description='')

parser.add_argument('-l', '--ligand-file', dest='ligand_file', default='../ligands.name', 
	help='File containing ZINC IDs of ligands.')
parser.add_argument('-d', '--decoy-file',  dest='decoy_file',  default='../decoys.name', 
	help='File containing ZINC IDs of decoys.')

parser.add_argument('-s1', dest='ref',  
	help='reference score file. e.g., extract_all.sort.uniq.txt')
parser.add_argument('-s2', dest='new', nargs='+', 
	help='modified score file(s) from new method(s). e.g., score.*')

parser.add_argument('-p', dest='plot', choices=['single', 'compare'],
	help='choose to plot bootstrap AUC for one method or compare multiple methods to the reference')
parser.add_argument('-b', dest='bootstrap', choices=['standard', 'ratio'], default='ratio',
	help='choose how to do bootstrp: standard or keep the same ratio between ligands and decoys')


global num_bootstrap_replicate
num_bootstrap_replicate = 1000
print("Number of bootstrap replicate: %d" % num_bootstrap_replicate)

def main():
	opt = parser.parse_args()

	global lig_list, decoy_list 
	lig_list, decoy_list = [], []
	read_ligands_decoys(opt.ligand_file, opt.decoy_file)

	if opt.plot == 'single':
		if opt.ref:
			ref_scores = read_score(opt.ref)
			if opt.bootstrap == 'standard':
				auc, logauc = bootstrap(ref_scores)
			elif opt.bootstrap == 'ratio':
				auc, logauc = bootstrap_keep_ratio(ref_scores)
			boxplot_auc(opt.ref, auc, logauc)
		else:
			print("Provide one score file with -s1 to plot bootstrap AUC")
			sys.exit(-1)

	elif opt.plot == 'compare':
		if opt.ref and opt.new:
			ref_scores = read_score(opt.ref)

			num_methods = len(opt.new)
			print("Compare %d methods to reference" % num_methods)
			auc_list, logauc_list, p_auc_list, p_logauc_list = [], [], [], []
			for onefile in opt.new:
				print("Processing file: %s" % onefile)
				new_scores = read_score(onefile)
				if opt.bootstrap == 'standard':
					auc, logauc = bootstrap_2methods(ref_scores, new_scores)
				elif opt.bootstrap == 'ratio':
					p_auc, p_logauc, auc, logauc = bootstrap_2methods_keep_ratio(ref_scores, new_scores)
				auc_list.append(auc)
				logauc_list.append(logauc)
				p_auc_list.append(p_auc)
				p_logauc_list.append(p_logauc)
			names = []
			for i in opt.new:
				names.append(i.split(".")[-1])
			boxplot_2methods(names, auc_list, logauc_list, p_auc_list, p_logauc_list)

		else:
			print("Provide reference score file with -s1\n")
			print("        score file(s) in comparison with -s2\n")
			sys.exit(-1)

def bootstrap_keep_ratio(scores):
	auc_list, logauc_list = [], []
	lig_scores = [i for i in scores if i[2] in lig_list]
	decoy_scores = [i for i in scores if i[2] in decoy_list]

	for i in range(num_bootstrap_replicate):
		bootstrap_lig_indeces = [ np.random.randint(0, len(lig_scores)) for _ in lig_scores ]
		bootstrap_decoy_indeces = [ np.random.randint(0, len(decoy_scores)) for _ in decoy_scores ]

		new_lig_scores = [ lig_scores[i] for i in bootstrap_lig_indeces]
		new_decoy_scores = [ decoy_scores[i] for i in bootstrap_decoy_indeces]
		new_scores = new_lig_scores + new_decoy_scores

		new_scores.sort(key=lambda x: float(x[-1]))
		points = do_roc(new_scores)
		points = interpolate_curve(points)
		auc = AUC(points)*100
		logauc = logAUC(points)*100
		#print(auc, logauc)
		#plot_ROC(i, points, auc, logauc)
		auc_list.append(auc)
		logauc_list.append(logauc)
	return auc_list, logauc_list

def bootstrap_2methods_keep_ratio(scores1, scores2):

	list_auc1, list_auc2, list_logauc1, list_logauc2 = [],[],[],[]
	dict_scores1 = {}
	for i in scores1:
		dict_scores1[i[2]] = i
	lig_scores = [i for i in scores2 if i[2] in lig_list]
	decoy_scores = [i for i in scores2 if i[2] in decoy_list]

	# always bootstrap from score2 and find matched zincID in score1
	auc_diff, logauc_diff = [], []
	for i in range(num_bootstrap_replicate):
		bootstrap_lig_indeces = [ np.random.randint(0, len(lig_scores)) for _ in lig_scores ]
		bootstrap_decoy_indeces = [ np.random.randint(0, len(decoy_scores)) for _ in decoy_scores ]

		new_lig_scores = [ lig_scores[i] for i in bootstrap_lig_indeces]
		new_decoy_scores = [ decoy_scores[i] for i in bootstrap_decoy_indeces]
		new_scores2 = new_lig_scores + new_decoy_scores

		mol_names = [ i[2] for i in new_scores2 ]
		new_scores1 = [ dict_scores1[mol] for mol in mol_names ]

		new_scores1.sort(key=lambda x: float(x[-1]))
		new_scores2.sort(key=lambda x: float(x[-1]))

		points = do_roc(new_scores1)
		points = interpolate_curve(points)
		auc1 = AUC(points)*100
		logauc1 = logAUC(points)*100

		points = do_roc(new_scores2)
		points = interpolate_curve(points)
		auc2 = AUC(points)*100
		logauc2 = logAUC(points)*100

		list_auc1.append(auc1)
		list_auc2.append(auc2)
		list_logauc1.append(logauc1)
		list_logauc2.append(logauc2)

		auc_diff.append(auc2-auc1)
		logauc_diff.append(logauc2-logauc1)

	t_auc, p_auc = stats.ttest_ind(list_auc1,list_auc2)
	print(t_auc, p_auc)
	t_logauc, p_logauc = stats.ttest_ind(list_logauc1,list_logauc2)
	print(t_logauc, p_logauc)

	return p_auc, p_logauc, auc_diff, logauc_diff

def bootstrap_2methods(scores1, scores2):

	dict_scores1 = {}
	for i in scores1:
		dict_scores1[i[2]] = i

	# always bootstrap from score2 and find matched zincID in score1
	auc_diff, logauc_diff = [], []
	num = len(scores2)
	for i in range(num_bootstrap_replicate):
		bootstrap_indeces = [ np.random.randint(0, num) for _ in scores2 ]

		new_scores2 = [ scores2[i] for i in bootstrap_indeces]
		mol_names = [ i[2] for i in new_scores2 ]
		new_scores1 = [ dict_scores1[mol] for mol in mol_names ]

		new_scores1.sort(key=lambda x: float(x[-1]))
		new_scores2.sort(key=lambda x: float(x[-1]))

		points = do_roc(new_scores1)
		points = interpolate_curve(points)
		auc1 = AUC(points)*100
		logauc1 = logAUC(points)*100

		points = do_roc(new_scores2)
		points = interpolate_curve(points)
		auc2 = AUC(points)*100
		logauc2 = logAUC(points)*100

		auc_diff.append(auc2-auc1)
		logauc_diff.append(logauc2-logauc1)

	return auc_diff, logauc_diff

def bootstrap(scores):
	auc_list, logauc_list = [], []
	num = len(scores)
	for i in range(num_bootstrap_replicate):
		bootstrap_indeces = [ np.random.randint(0, num) for _ in scores ]
		new_scores = [ scores[i] for i in bootstrap_indeces]
		new_scores.sort(key=lambda x: float(x[-1]))
		#print(new_scores)
		points = do_roc(new_scores)
		points = interpolate_curve(points)
		auc = AUC(points)*100
		logauc = logAUC(points)*100
		#print(auc, logauc)
		auc_list.append(auc)
		logauc_list.append(logauc)
	return auc_list, logauc_list

def boxplot_2methods(names, data1, data2, p1, p2):

	medians_auc = []
	medians_logauc = []
	for data in data1:
		medians_auc.append(np.median( np.array(data) ) )
	print(medians_auc)
	for data in data2:
		medians_logauc.append(np.median( np.array(data) ) )

	min_auc, top_auc = np.min(np.array(data1)), np.max(np.array(data1))
	min_logauc, top_logauc = np.min(np.array(data2)), np.max(np.array(data2))
	pos = np.arange(len(data1)) + 1

	fig = plt.figure(figsize=(3*len(names), 5), dpi=120, facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace=0.4, wspace=0.4)
	props = dict(patch_artist=True, medianprops=dict(color="gold"))

	ax1 = fig.add_subplot(1, 2, 1)
	bp1 = ax1.boxplot(data1, **props)
	ax1.set_title("AUC")
	ax1.set_ylabel(r"$\Delta$ AUC")
	ax1.set_ylim([min_auc-1, top_auc+2])
	ax1.set_xticklabels(names)
	plt.grid(linestyle='dotted')
	upperLabels = []
	for i in range(len(medians_auc)):
		upperLabels.append( "%.2f\np=%.2E" % (medians_auc[i], p1[i]) )
	#upperLabels = [str(np.round(s, 2)) for s in medians_auc]
	for tick, label in zip(range(len(data1)), ax1.get_xticklabels()):
		ax1.text(pos[tick], top_auc+1, upperLabels[tick], horizontalalignment='center', size='medium')

	ax2 = fig.add_subplot(1, 2, 2)
	bp2 = ax2.boxplot(data2, **props)
	ax2.set_title("logAUC")
	ax2.set_ylabel(r"$\Delta$ logAUC")
	ax2.set_ylim([min_logauc-1, top_logauc+2])
	ax2.set_xticklabels(names)
	plt.grid(linestyle='dotted')
	upperLabels = []
	for i in range(len(medians_logauc)):
		upperLabels.append( "%.2f\np=%.2E" % (medians_logauc[i], p2[i]) )
	#upperLabels = [str(np.round(s, 2)) for s in medians_logauc]
	for tick, label in zip(range(len(data2)), ax2.get_xticklabels()):
		ax2.text(pos[tick], top_logauc+1, upperLabels[tick], horizontalalignment='center', size='medium')


	colors = ['tab:blue','tab:red','tab:green','violet']

	if len(names) > 4:
		colors = ['lightsalmon','palegreen','plum','paleturquoise',\
				  'rosybrown','lightgreen','violet','lightblue']
	for bplot in (bp1, bp2):
		for bp, color in zip(bplot['boxes'], colors):
			bp.set_facecolor(color)


	#fig.suptitle("Changes in AUC and logAUC")
	fig.tight_layout()
	fig.savefig("fig_compare_methods.png")

def boxplot_auc(title, auc_list, logauc_list):
	fig = plt.figure(figsize=(5, 5), dpi=120, facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace=0.4, wspace=0.4)
	props = dict(patch_artist=True, medianprops=dict(color="gold"))

	ax1 = fig.add_subplot(2, 1, 1)
	color = 'tab:red'
	ax1.set_ylabel('logAUC', color=color)
	bp1 = ax1.boxplot(logauc_list, positions=[0], **props)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()
	color = 'tab:blue'
	ax2.set_ylabel('AUC', color=color)
	bp2 = ax2.boxplot(auc_list, positions=[1], **props)
	ax2.tick_params(axis='y', labelcolor=color)

	ax1.set_xlim(-0.5,1.5)
	ax1.set_xticks(range(2))
	ax1.set_xticklabels(["bootstrap logAUC","bootstrap AUC"])

	colors = ['tab:red','tab:blue']
	for bp, color in zip(bp1['boxes']+bp2['boxes'], colors):
		bp.set_facecolor(color)

	ax3 = fig.add_subplot(2, 1, 2)
	num_bins = 50
	ax3.hist(auc_list, num_bins, density=1, color='tab:blue')
	ax4 = ax3.twinx()
	ax4.hist(logauc_list, num_bins, density=1, color='tab:red')

	fig.suptitle(title)
	fig.savefig("fig_bootstrapAUC_"+title+".png")
	plt.clf()

def plot_ROC(name, points, auc, logauc):
	x, y = zip(*points)

	fig = plt.figure(figsize=(15, 8), dpi=120, facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace=0.4, wspace=0.4)
	ax1 = fig.add_subplot(1, 2, 1)
	ax1.plot(x, y, linewidth=2, label='AUC: %.2f' % auc)
	ax2 = fig.add_subplot(1, 2, 2)
	ax2.semilogx(x, y, linewidth=2, label='logAUC: %.2f' % logauc)
	x = np.arange(0,100,0.1)
	ax1.plot(x, x, 'k--')
	#ax1.axis([0, 100, 0, 100])
	ax2.semilogx(x, x, 'k--')
	ax2.axis([0.1, 100, 0, 100])

	ax1.set_xlabel(" Decoys Found %")
	ax1.set_ylabel(" Ligands Found %")
	ax2.set_xlabel("Decoys Found % ")
	ax2.set_ylabel("Ligands Found %")
	
	fig.savefig("%s.png" % name)
	plt.clf()

def do_roc(scores):

	num_data = len(scores)
	binsize = 1
	num_lig = len(lig_list)
	num_dec = len(decoy_list)

	found_ligand = 0
	results = []
	for i in xrange(num_data):
		results.append([i-found_ligand, found_ligand])
		if scores[i][2].split('.')[0] in lig_list: 
			found_ligand += 1
	results.append([num_data - found_ligand, found_ligand])
	results.append([num_dec, num_lig])

	points = []
	for x in results:
		fpr = x[0]*100.0/num_dec
		tpr = x[1]*100.0/num_lig
		points.append([fpr, tpr])
	return points

def interpolate_curve(points):
	i = 0
	while i < len(points) and points[i][0] < 0.1:
		i += 1
	slope = (points[i][1] - points[i-1][1])/(points[i][0] - points[i-1][0])
	intercept = points[i][1] - slope * points[i][0]
	point_one =  [0.100001, (slope * 0.100001 + intercept)]
	npoints = [x for x in points]
	npoints.insert(i, point_one)
	return npoints

def AUC(points):
	"""Calulate the area under the curve using trapezoid rule."""
	auc = 0.0
	for point2, point1 in zip(points[1:], points[:-1]):
		#print(point2, point1)
		base = (point2[0] - point1[0]) / 100.0
		height = ( (point2[1] - point1[1])/2.0 + point1[1] ) / 100.0
		auc += (base*height)
	return auc

def logAUC(points):
	"""Compute semilog x AUC minus the perfectly random semilog AUC."""
	# assumes we have previously interpolated to get y-value at x = 0.1% 
	# generate new points array clamped between 0.1% and 100%

	# constants
	## if you modify also change in plots.py        
	LOGAUC_MAX = 1.0   ## this should not change
	LOGAUC_MIN = 0.001 ## this you may want to change if you database is large and you have strong early enrichment. 
	RANDOM_LOGAUC = (LOGAUC_MAX-LOGAUC_MIN)/np.log(10)/np.log10(LOGAUC_MAX/LOGAUC_MIN)

	npoints = []
	for x in points:
		if (x[0] >= LOGAUC_MIN*100) and (x[0] <= LOGAUC_MAX*100):
			npoints.append( [x[0]/100 , x[1]/100] )

	area = 0.0
	for point2, point1 in zip(npoints[1:], npoints[:-1]):
		if point2[0] - point1[0] < 0.000001:
			continue
		# segment area computed as integral of log transformed equation
		dx = point2[0]-point1[0]
		dy = point2[1]-point1[1]
		intercept = point2[1] - (dy)/(dx) * point2[0]
		area += dy/np.log(10) + intercept*(np.log10(point2[0])-np.log10(point1[0]))

	return area/np.log10(LOGAUC_MAX/LOGAUC_MIN) - RANDOM_LOGAUC

def read_ligands_decoys(lig_file, decoy_file):
	with open(lig_file, "r") as f:
		for oneline in f:
			lig_list.append(oneline.strip())
	with open(decoy_file, "r") as f:
		for oneline in f:
			decoy_list.append(oneline.strip())
	print("%d ligands and %d decoys read in." % (len(lig_list), len(decoy_list)) )
	return len(lig_list)+len(decoy_list)

def read_score(infile):
	outList = []
	with open(infile, "r") as f:
		for oneline in f:
			ele = oneline.split()
			outList.append(ele)
	return outList


if __name__ == "__main__":
	main()



"""
#======= test standard ROC curve & bootstrap AUC ========#

	# test auc logauc calculation
	points = do_roc(ref_scores)
	points = interpolate_curve(points)
	auc = AUC(points)*100
	logauc = logAUC(points)*100
	print(auc, logauc)
	plot_ROC(points, auc, logauc)

	# test bootstrap for one method
	auc, logauc = bootstrap(ref_scores)
	boxplot_auc(auc, logauc)

#======= test scikit-learn ========#
from sklearn.metrics import roc_curve, roc_auc_score, auc, mean_squared_error

	exp, pred  = get_data(ref_scores)
	fpr, tpr, thresholds = roc_curve(exp, pred)
	print(fpr, tpr, thresholds)
	print( roc_auc_score(exp, pred) )
	print( auc(fpr, tpr) )

	plt.figure()
	lw = 2
	plt.plot(fpr, tpr, color='darkorange',
	         lw=lw, label='ROC curve (area = %0.2f)' % auc(fpr, tpr))
	plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic example')
	plt.legend(loc="lower right")
	plt.show()

	#for onefile in opt.new:
	#	new_scores = read_score(opt.onefile)

def get_data(scores):
	exp, pred = [], []
	ndata = len(scores)
	for i in xrange(ndata):
		if scores[i][2] in lig_list:
			exp.append(1)
		else:
			exp.append(0)
		pred.append(0-float(scores[i][21]))
	print(exp, pred)
	return exp, pred
"""
