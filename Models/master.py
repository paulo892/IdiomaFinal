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
from joblib import dump, load
import numpy as np
import statistics
import math
import plotly as py
import model
import sys
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def plot(figs):
	headerColor = 'grey'
	rowEvenColor = 'lightgrey'
	rowOddColor = 'white'

	fig = go.Figure(data=[go.Table(
		header=dict(values=['<b>Metrics and Statistics</b>',
	                  '<b>% Features Used</b>',
	                  '<b>Accuracy</b>',
	                  '<b>Precision</b>',
	                  '<b>Recall</b>',
					  '<b>F-measure</b>'],
					   line = dict(color = '#506784'),
	    			fill = dict(color = headerColor),
	    			align = ['left','center'],
	    			font = dict(color = 'white', size = 12)),
		cells=dict(values= [
	      ['Decision Tree', 'Stochastic Gradient Descent', 'Multi-Layer Perceptron', 'Gaussian (Naive Bayes)', 'Bagging', 'Random Forest', 'Support Vector Classifier', 'k-Nearest Neighbor Classifier'],
	      [round(figs[0][0], 2), round(figs[1][0], 2), round(figs[2][0], 2), round(figs[3][0], 2), round(figs[4][0], 2), round(figs[5][0], 2), round(figs[6][0], 2), round(figs[7][0], 2)],
	      [round(figs[0][1], 2), round(figs[1][1], 2), round(figs[2][1], 2), round(figs[3][1], 2), round(figs[4][1], 2), round(figs[5][1], 2), round(figs[6][1], 2), round(figs[7][1], 2)],
	      [round(figs[0][2], 2), round(figs[1][2], 2), round(figs[2][2], 2), round(figs[3][2], 2), round(figs[4][2], 2), round(figs[5][2], 2), round(figs[6][2], 2), round(figs[7][2], 2)],
	      [round(figs[0][3], 2), round(figs[1][3], 2), round(figs[2][3], 2), round(figs[3][3], 2), round(figs[4][3], 2), round(figs[5][3], 2), round(figs[6][3], 2), round(figs[7][3], 2)],
		  [round(figs[0][4], 2), round(figs[1][4], 2), round(figs[2][4], 2), round(figs[3][4], 2), round(figs[4][4], 2), round(figs[5][4], 2), round(figs[6][4], 2), round(figs[7][4], 2)]],
		  line = dict(color = '#506784'),
	    fill = dict(color = [rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]),
	    align = ['left', 'center'],
	    font = dict(color = '#506784', size = 11))
	)])
	fig.show()

if __name__ == '__main__':

	print('Start!')

	# reads in the dataset
	test_data = pd.read_csv('../Data/Annotations_Adjusted.csv')

	# trains and tests the models
	bagging = model.train(test_data, 'bagging')
	dec_tree = model.train(test_data, 'dec_tree')
	forest = model.train(test_data, 'forest')
	mlp = model.train(test_data, 'mlp')
	sgd = model.train(test_data, 'sgd')
	gaussian_nb = model.train(test_data, 'gaussian_nb')
	nn = model.train(test_data, 'nn')
	svc = model.train(test_data, 'svc')

	# plots the results
	plot([dec_tree, sgd, mlp, gaussian_nb, bagging, forest, svc, nn])
