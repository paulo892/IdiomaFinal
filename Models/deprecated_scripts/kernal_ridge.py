from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectPercentile
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
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

	# ensures the lengths of the target data line up
	length = len(target_brescola)
	if length != len(target_zh) or length != len(target_wiki) or length != len(target_psfl):
		print("ERROR: Lengths of four targets are not all the same.")

	## aggregates the results into one column
	difficulties = []

	# for each observation...
	for i in range(length):
		results = [target_psfl.values[i], target_zh.values[i], target_wiki.values[i], target_brescola.values[i]]

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

		# TODO - Plot the differences here!
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

	# sets the target data according to user input
	print('Please select the corpora to use as ground truth: 0 - PSFL, 1 - ZH, 2 - Wiki, 3 - BrEscola, 4 - Weighted Average')
	temp = float(input())

	if (temp == 0):
		target = target_psfl.values.reshape(-1,).tolist()
	elif (temp == 1):
		target = target_zh.values.reshape(-1,).tolist()
	elif (temp == 2):
		target = target_wiki.values.reshape(-1,).tolist()
	elif (temp == 3):
		target = target_brescola.values.reshape(-1,).tolist()
	elif (temp == 4):
		target = difficulties

	# partitions data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

	# partitions the training set into a general set (for use in the model) and a tuning set (for use in refining other components)
	X_general, X_tuning, y_general, y_tuning = train_test_split(X_train, y_train, test_size=0.3)

	X_tuning_copy = X_tuning.copy()

	# Uses GridSearchCV to determine the right kernel 
	#, degree=[2, 3, 4]
	model = SVC()
	grid = GridSearchCV(estimator=model, param_grid=dict(kernel=['linear', 'poly', 'rbf', 'sigmoid'], degree=[1,2,3,4]))
	grid.fit(X_tuning, y_tuning)

	op_kernel = grid.best_estimator_.kernel
	op_degree = grid.best_estimator_.degree

	print('Optimal Params (SVC):', op_kernel, op_degree)

	## performs feature selection using other scikit libraries

	# TODO - Average all metrics out over many rounds for better selection
	# TODO - Select only a couple of metrics
	print('FEATURE SELECTION METRICS (SVC):')
	for j in range(20, 80, 5):
		index = X_tuning.index.tolist()
		cols = X_tuning.columns.tolist()

		# creates selector for given percentile of features
		selector = SelectPercentile(percentile=j)
		X_new = selector.fit_transform(X_tuning, y_tuning)

		temp = selector.get_support(True)

		X_tuning = pd.DataFrame(data=X_tuning, index=index, columns=[cols[i] for i in temp])

		# splits tuning set into training and testing data
		X_train_iter, X_test_iter, y_train_iter, y_test_iter = train_test_split(X_tuning, y_tuning, test_size=0.2)

		# fits a basic decision tree model on the data
		svc = SVC(kernal=op_kernel, degree=op_degree)
		fitted = svc.fit(X_train_iter, y_train_iter)

		# calculates the accuracy, precision, recall, and f1-measure
		y_pred = fitted.predict(X_test_iter).tolist()
		y_true = y_test_iter

		# NOTE - Order in lists is 'd','s'
		accuracy = accuracy_score(y_true, y_pred)
		precisions_by_label = [precision_score(y_true, y_pred, average='binary', pos_label='d'), precision_score(y_true, y_pred, average='binary', pos_label='s')]
		precision_global = precision_score(y_true, y_pred, average='micro')
		recalls_by_label = recall_score(y_true, y_pred, average=None)
		recall_global = recall_score(y_true, y_pred, average='micro')
		f1s_by_label = f1_score(y_true, y_pred, average=None) 
		f1_global = f1_score(y_true, y_pred, average='micro') 

		print(j / 100, 'acc:', round(accuracy, 2), 'precisions_by_label', [round(x, 2) for x in precisions_by_label], 'precision_global', round(precision_global, 2), 'recalls_by_label', [round(x, 2) for x in recalls_by_label], 'recall_global', round(recall_global, 2), 'f1s_by_label', [round(x, 2) for x in f1s_by_label], 'f1_global', round(f1_global, 2))

		X_tuning=X_tuning_copy

	# TODO - Plots for all of the metrics chosen - do it for just one model to give reader idea of the range in performance depending on selected features + how we visualized it
	#ax = plt.gca()
	#ax.plot(percs, [x[1] for x in nrmses])
	#plt.xlabel('percentage of features included')
	#plt.ylabel('NRMSE')
	#plt.title('NMRSE change over feature inclusion thresholds')
	#plt.axis('tight')
	#plt.show(block=False)
	#plt.savefig('linear_feature_threshold_nrmses.png')
	#plt.clf()

	print('Please input a reasonable decimal threshold for feature selection:')
	thresh = float(input())
	
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
	svc = SVC(kernal=op_kernel, degree=op_degree)
	fitted = svc.fit(X_general, y_general)

	# prints evaluation metrics
	y_pred = fitted.predict(X_test).tolist()
	y_true = y_test

	accuracy = accuracy_score(y_true, y_pred)
	precisions_by_label = [precision_score(y_true, y_pred, average='binary', pos_label='d'), precision_score(y_true, y_pred, average='binary', pos_label='s')]
	precision_global = precision_score(y_true, y_pred, average='micro')
	recalls_by_label = recall_score(y_true, y_pred, average=None)
	recall_global = recall_score(y_true, y_pred, average='micro')
	f1s_by_label = f1_score(y_true, y_pred, average=None) 
	f1_global = f1_score(y_true, y_pred, average='micro') 

	# TODO - Print metrics more intelligently
	print('SVC:', 'acc:', round(accuracy, 2), 'precisions_by_label', [round(x, 2) for x in precisions_by_label], 'precision_global', round(precision_global, 2), 'recalls_by_label', [round(x, 2) for x in recalls_by_label], 'recall_global', round(recall_global, 2), 'f1s_by_label', [round(x, 2) for x in f1s_by_label], 'f1_global', round(f1_global, 2))

	# TODO - Plot all evaluation metrics!
	# visualizes the residuals
	#plt.xlabel('Predicted Value')
	#plt.ylabel('Residual')
	#plt.title('Residuals (Linear Regression)')
	#plt.axis('tight')
	#plt.savefig('linear_residuals.png')
	#plt.show()
	#plt.clf()

	# saves the model to a file
	filename = 'svc.sav'
	pickle.dump(fitted, open(filename, 'wb'))

	# prints the mean accuracy
	#loaded_model = pickle.load(open(filename, 'rb'))
	#result = loaded_model.score(X_test, y_test)
	#print('Mean Accuracy: ', result)

	return fitted