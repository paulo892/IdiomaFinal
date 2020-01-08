import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from sklearn.impute import SimpleImputer
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_regression
import numpy as np
import statistics
import math
import decision_tree
import plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def preprocess(data):

	test_data = data

	# removes the categorical variables from the dataset
	x = list(range(1,len(test_data.columns), 2))
	test_data = test_data.drop(test_data.columns[x], axis=1)

	# performs complete case analysis to remove instances that are missing the target feature level
	for index, row in test_data.iterrows():
		if math.isnan(row["IGRNT_A"]):
			test_data = test_data.drop(axis=0, index=index)

	# calculates proportion of missing values for each feature and imputes if <35% missing, deletes if not
	percMissing = []

	for column in test_data:
		total = len(test_data.index)
		sum = 0

		imp_mean = SimpleImputer(strategy='mean')

		for i in test_data[column]:
			if math.isnan(i):
				sum = sum + 1

		# imputation threshold
		if float(sum) / total < 0.35:
			imp_mean.fit(np.reshape(np.asarray(test_data[column]), (-1,1)))
			
			test_data[column] = imp_mean.transform(np.reshape(np.asarray(test_data[column]), (-1,1)))
		else:
			test_data = test_data.drop(columns=[column], axis=1)

	print(len(test_data.index))

	# swaps the target column and the final column
	target_index = test_data.columns.get_loc("IGRNT_A")
	num_cols = len(test_data.columns)

	cols = test_data.columns.tolist()
	cols = cols[:target_index] + cols[num_cols:(num_cols + 1)] + cols[(target_index + 1):num_cols] + cols[target_index:(target_index + 1)]
	test_data = test_data[cols]

	# plots a histogram of the target feature
	dat = test_data.iloc[:,(num_cols - 1)].values.tolist()

	print(max(dat))
	print(min(dat))

	ax = plt.hist(dat, bins='auto')
	
	plt.xlabel('IGRNT_A Value')
	plt.ylabel('Density')
	plt.title('Distribution of IGRNT_A')
	#plt.show(block=True)
	plt.savefig('IGRNT_A_histogram.png')
	plt.clf()

	# removes the LOAN_T and FLOAN_T columns
	test_data = test_data.drop(['LOAN_T', 'FLOAN_T'], axis=1)

	# performs feature selection by removing zero-variance features
	index = test_data.index.tolist()
	cols = test_data.columns.tolist()

	selector = VarianceThreshold()
	test_data = selector.fit_transform(test_data)

	test_data = pd.DataFrame(data=test_data, index=index, columns=[cols[i] for i in selector.get_support(True)])

	return test_data

def plot(figs):
	headerColor = 'grey'
	rowEvenColor = 'lightgrey'
	rowOddColor = 'white'

	trace0 = go.Table(
	  header = dict(
	    values = [['<b>Evaluation Metrics</b>'],
	                  ['<b>MAE</b>'],
	                  ['<b>RMSE</b>'],
	                  ['<b>R-Squared</b>'],
	                  ['<b>NRMSE</b>']],
	    line = dict(color = '#506784'),
	    fill = dict(color = headerColor),
	    align = ['left','center'],
	    font = dict(color = 'white', size = 12)
	  ),
	  cells = dict(
	    values = [
	      [['Linear Regression', 'Linear Regression [Poly Feat.]', 'Ridge Regression', 'Lasso Regression', 'Support Vector Regression', 'Random Forest Regression']],
	      #[figs[0]],
	      #[figs[1]],
	      #[figs[2]]],
	      [[round(figs[0][0], 2), round(figs[1][0], 2), round(figs[2][0], 2), round(figs[3][0], 2), round(figs[4][0], 2), round(figs[5][0], 2)]],
	      [[round(figs[0][1], 2), round(figs[1][1], 2), round(figs[2][1], 2), round(figs[3][1], 2), round(figs[4][1], 2), round(figs[5][1], 2)]],
	      [[round(figs[0][2], 2), round(figs[1][2], 2), round(figs[2][2], 2), round(figs[3][2], 2), round(figs[4][2], 2), round(figs[5][2], 2)]],
	      [[round(figs[0][3], 2), round(figs[1][3], 2), round(figs[2][3], 2), round(figs[3][3], 2), round(figs[4][3], 2), round(figs[5][3], 2)]]],
	    line = dict(color = '#506784'),
	    fill = dict(color = [rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]),
	    align = ['left', 'center'],
	    font = dict(color = '#506784', size = 11)
	    ))

	data = [trace0]

	py.plotly.plot(data, filename = "alternating row colors")

if __name__ == '__main__':

	# logs into table service
	# TODO - Figure out table service
	# py.tools.set_credentials_file(username='paulo892', api_key='AiZ0NJ9htO9OVySZNYtE')

	print('Start!')

	# reads in the dataset
	test_data = pd.read_csv('../Annotations_Adjusted.csv')

	# preprocesses the data
	# test_data = preprocess(test_data)

	# creates the models
	dec_tree = decision_tree.train(test_data)

	# plots the model results
	#plot([lin_reg, poly_reg, ridge_reg, lasso_reg, svm_reg, forest_reg])
