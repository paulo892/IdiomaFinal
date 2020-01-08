import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from sklearn.impute import SimpleImputer
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from scipy import stats
from math import sqrt
import numpy as np
import statistics
import math
from sklearn import tree
import pickle

def train(data):

	test_data = data

	# aggregates the predictions on classifiers over the four corpuses into one
	target_psfl = test_data.loc[:, test_data.columns == 'psfl']
	target_zh = test_data.loc[:, test_data.columns == 'zh']
	target_wiki = test_data.loc[:, test_data.columns == 'wiki']
	target_brescola = test_data.loc[:, test_data.columns == 'brescola']

	length = len(target_brescola)
	print(len(target_brescola), len(target_zh), len(target_wiki), len(target_psfl))

	if length != len(target_zh) or length != len(target_wiki) or length != len(target_psfl):
		print("WHAT")

	difficulties = []
	for i in range(length):
		# gets results
		results = [target_psfl.values[i], target_zh.values[i], target_wiki.values[i], target_brescola.values[i]]

		# takes the maximum, defaulting towards "difficult" in case of tie
		s = 0
		d = 0

		for res in results:
			if res == 'd':
				d += 1
			elif res == 's':
				s += 1
			else:
				print('HUH')

		if d >= s:
			difficulties.append('d')
		else:
			difficulties.append('s')

	# partitions data into features and target
	data = test_data.drop("psfl", axis=1)
	data = data.drop("zh", axis=1)
	data = data.drop("wiki", axis=1)
	data = data.drop("brescola", axis=1)
	data = data.drop("docid", axis=1)
	print(data)
	target = difficulties

	if len(target) != len(target_brescola):
		print('ISSUE')

	# partitions data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

	print(np.sum(np.isnan(X_test)))
	print(y_test)
	print(len(y_test))

	# partitions the training set into a general set (for use in the model) and a tuning set (for use in refining other components)
	X_general, X_tuning, y_general, y_tuning = train_test_split(X_train, y_train, test_size=0.2)

	X_tuning_copy = X_tuning.copy()

	# performs feature selection using other scikit libraries
	rmse_sum = 0
	nrmse_sum = 0
	rmse_count = 0
	nrmses = []
	percs = range (20, 80, 5)

	for j in range(20, 80, 5):
		for k in range(200):

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
			dec_tree = tree.DecisionTreeClassifier()
			fitted = dec_tree.fit(X_train_iter, y_train_iter)

			# TODO - evaluate the effectiveness of the model somehow
			#y_pred = fitted.predict(X_test_iter).tolist()
			#y_actual = y_test

			#sum = 0
			#for i in range(len(y_pred)):
			#	sum += (y_pred[i] - y_actual[i]) ** 2

			#rmse = sqrt(sum / len(y_pred))
			#rmse_sum += rmse

			#max_y = max(y_actual)
			#min_y = min(y_actual)
			#range_y = max_y - min_y

			#nrmse = rmse / range_y

			
			#nrmse_sum += nrmse
			#rmse_count += 1

			X_tuning=X_tuning_copy
		#rmse_avg = rmse_sum / rmse_count
		#nrmse_avg = nrmse_sum / rmse_count
		#nrmses.append([j, nrmse_avg])
		# print 'Avg NRMSE (retained feature perc = ' + str(j) + '): ' + str(rmse_avg) + '\n' 

	# displays the NMRSES to determine a reasonable feature selection percentage threshold
	#ax = plt.gca()
	#ax.plot(percs, [x[1] for x in nrmses])
	#plt.xlabel('percentage of features included')
	#plt.ylabel('NRMSE')
	#plt.title('NMRSE change over feature inclusion thresholds')
	#plt.axis('tight')
	#plt.show(block=False)
	#plt.savefig('linear_feature_threshold_nrmses.png')
	#plt.clf()

	#print('Please input a reasonable percent threshold for feature selection:')
	#thresh = float(input())
	thresh = 0.6
	
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

	# TODO - evaluate the effectiveness of the model somehow
	# y_pred = fitted.predict(X_test).tolist()
	# y_actual = y_test.values

	# sum = 0
	# for i in range(len(y_pred)):
	#	sum += (y_pred[i] - y_actual[i]) ** 2

	# mae = mean_absolute_error(y_actual, y_pred)

	#rmse = sqrt(sum / len(y_pred))

	#max_y = max(y_actual)
	#min_y = min(y_actual)
	#range_y = max_y - min_y

	#nrmse = float(rmse / range_y)

	#r2 = r2_score(y_actual, y_pred)

	# visualizes the residuals
	#plt.xlabel('Predicted Value')
	#plt.ylabel('Residual')
	#plt.title('Residuals (Linear Regression)')
	#plt.axis('tight')
	#plt.savefig('linear_residuals.png')
	#plt.show()
	#plt.clf()

	#print('MAE of Linear Regression applied to training data: ' + str(mae))
	#print('RMSE of Linear Regression applied to training data: ' + str(rmse))
	#print('R-Squared Score of Linear Regression applied to training data: ' + str(r2))
	#print('NMRSE of Linear Regression applied to training data: ' + str(nrmse))

	# saves the model to a file
	filename = 'decision_tree.sav'
	pickle.dump(fitted, open(filename, 'wb'))

	# prints the mean accuracy
	loaded_model = pickle.load(open(filename, 'rb'))
	result = loaded_model.score(X_test, y_test)
	print('Mean Accuracy: ', result)

	return fitted

	#return [mae, rmse, r2, nrmse]