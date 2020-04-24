from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectPercentile
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn import tree
import pandas as pd
import numpy as np
import pickle

def train(data):

	test_data = data

	## aggregates the predictions on classifiers over the four corpuses into one
	target_psfl = test_data.loc[:, test_data.columns == 'psfl']
	target_zh = test_data.loc[:, test_data.columns == 'zh']
	target_wiki = test_data.loc[:, test_data.columns == 'wiki']
	target_brescola = test_data.loc[:, test_data.columns == 'brescola']

	# TOWRITE
	# ensures the lengths of the target data line up
	# changed to remove BrEscola from running -> refer to Filho
	# documents tailored to kids and teens -> want a wider sweep
	# Explanation:
	# Removed BrEscola because it uses documents originally just tailored for kids and teens
	# Don't want to rely on just PSFL (despite it performing best) since it used documents just for kids and just for adults
	# Highest accuracy but likely because its classifications are too stark -> we also don't want that to be the threshold
	# Our "simple" and "difficult" should be from the perspective of the "average" learner!
	# Decide to go with majority of the 3 -> fair accuracy
	# SHOW BOTH THIS ONE'S STATS AND THE PSFL ONLY
	length = len(target_brescola)
	if length != len(target_zh) or length != len(target_wiki) or length != len(target_psfl):
		print("ERROR: Lengths of four targets are not all the same.")

	# aggregates the results into one column
	difficulties = []

	# for each observation...
	for i in range(length):
		results = [target_psfl.values[i], target_zh.values[i], target_wiki.values[i]]

		# takes the maximum occurrence, defaulting towards "difficult" in case of tie
		s = 0
		d = 0
		for res in results:
			if res == 'd':
				d += 1
			elif res == 's':
				s += 1
			else:
				print('ERROR: Target value not \'d\' nor \'s\'.')

		# TO-WRITE:
		# if using the weighted system, tiebreaking in favor of d brings down overall accuracy but balances between labels
		# doing the opposite brings up accuracy and f1 but heavily leans in favor of predicting for 's'
		# just using psfl brings up both scores -> DISCUSS THIS -> why might this be? maybe those docs are all from psfl???

		# takes the simple majority and appends to list
		if d >= s:
			difficulties.append('d')
		else:
			difficulties.append('s')

	## partitions data into features and target, dropping old target columns as well as docid column
	data = test_data.drop("psfl", axis=1)
	data = data.drop("zh", axis=1)
	data = data.drop("wiki", axis=1)
	data = data.drop("brescola", axis=1)
	data = data.drop("docid", axis=1)

	# sets the target data according to user input - option 4 selected by default
	print('Please select the corpora to use as ground truth: 0 - PSFL, 1 - ZH, 2 - Wiki, 3 - BrEscola, 4 - Majority of non-BrE')
	print('Option 4 selected automatically. This setting can be changed in the individual model script.')
	#temp = float(input())
	temp = 4

	if (temp == 0):
		target = target_psfl.values.reshape(-1,).tolist()
	elif (temp == 1):
		target = target_zh.values.reshape(-1,).tolist()
	elif (temp == 2):
		target = target_wiki.values.reshape(-1,).tolist()
	elif (temp == 3):
		print('BrEscola classifier not implemented. See code.')
		return
	elif (temp == 4):
		target = difficulties
	
	# TOWRITE - Note that they're fairly balanced and so not differentiating metrics by label should be fine
	print('\n')
	print('Number of difficult docs:' + str(target.count('d')))
	print('Number of simpler docs:' + str(target.count('s')))
	print('\n')

	# partitions data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

	# partitions the training set into a general set (for use in the model) and a tuning set (for use in refining other components)
	X_general, X_tuning, y_general, y_tuning = train_test_split(X_train, y_train, test_size=0.2)

	X_tuning_copy = X_tuning.copy()

	## performs feature selection using other scikit libraries

	print('FEATURE SELECTION METRICS (DECISION TREE):')
	accs = []
	precs = []
	recs = []
	fones = []
	rng = range(20, 80, 5)
	for j in rng:
		index = X_tuning.index.tolist()
		cols = X_tuning.columns.tolist()

		# creates selector for given percentile of features
		selector = SelectPercentile(percentile=j)
		X_new = selector.fit_transform(X_tuning, y_tuning)

		temp = selector.get_support(True)

		X_temp = pd.DataFrame(data=X_tuning, index=index, columns=[cols[i] for i in temp])

		# splits tuning set into training and testing data
		X_train_iter, X_test_iter, y_train_iter, y_test_iter = train_test_split(X_temp, y_tuning, test_size=0.2)

		# fits a basic decision tree model on the data
		dec_tree = tree.DecisionTreeClassifier()
		fitted = dec_tree.fit(X_train_iter, y_train_iter)

		# calculates the accuracy, precision, recall, and f1-measure
		y_pred = fitted.predict(X_test_iter).tolist()
		y_true = y_test_iter

		# NOTE - Order in lists is 'd','s'
		accuracy = accuracy_score(y_true, y_pred)
		precision_global = precision_score(y_true, y_pred, average='binary', pos_label='d')
		recall_global = recall_score(y_true, y_pred, average='binary', pos_label='d')
		f1_global = f1_score(y_true, y_pred, average='binary', pos_label='d') 

		print(j / 100, 'acc:', round(accuracy, 2),'precision_global', round(precision_global, 2),  'recall_global', round(recall_global, 2), 'f1_global', round(f1_global, 2))
		accs.append(accuracy)
		precs.append(precision_global)
		recs.append(recall_global)
		fones.append(f1_global)

		X_tuning=X_tuning_copy

	# TOWRITE - For metrics, 'd' considered positive class
	ax = plt.gca()
	ax.plot(rng, accs, label="Accuracies")
	ax.plot(rng, precs, label="Precisions")
	ax.plot(rng, recs, label="Recalls")
	ax.plot(rng, fones, label="F-measures")
	plt.xlabel('Percentage of features used')
	plt.ylabel('Magnitude of measure')
	plt.title("Magnitude of eval. metrics by % of features used.")
	plt.axis('tight')
	plt.legend()
	plt.show(block=True)
	plt.savefig('decision_tree_metrics_by_prop_features.png')
	plt.clf()

	print('Please input a reasonable decimal threshold for feature selection:')
	thresh = float(input())
	#thresh = 0.6
	
	# uses the percent threshold to perform feature selection, applying it to training and test sets
	index_test = X_test.index.tolist()
	index_train = X_general.index.tolist()
	cols = X_test.columns.tolist()

	selector = SelectPercentile(percentile=(thresh*100))
	X_new = selector.fit_transform(X_general, y_general)

	temp = selector.get_support(True)

	X_general = pd.DataFrame(data=X_general, index=index_train, columns=[cols[i] for i in temp])
	X_test = pd.DataFrame(data=X_test, index=index_test, columns=[cols[i] for i in temp])

	# fits a decision tree model to the testing data
	dec_tree = tree.DecisionTreeClassifier()
	fitted = dec_tree.fit(X_general, y_general)

	# prints evaluation metrics
	y_pred = fitted.predict(X_test).tolist()
	y_true = y_test

	accuracy = accuracy_score(y_true, y_pred)
	precision_global = precision_score(y_true, y_pred, average='binary', pos_label='d')
	recall_global = recall_score(y_true, y_pred, average='binary', pos_label='d')
	f1_global = f1_score(y_true, y_pred, average='binary', pos_label='d') 

	print('Final:', 'acc:', round(accuracy, 2),'precision_global', round(precision_global, 2),  'recall_global', round(recall_global, 2), 'f1_global', round(f1_global, 2))

	# saves the model to a file
	filename = 'decision_tree.sav'
	pickle.dump(fitted, open(filename, 'wb'))

	return [accuracy, precision_global, recall_global, f1_global]