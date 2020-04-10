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
import decision_tree
import nearest_neighbor
import sgd_classifier
import mlp_classifier
import gaussian_nb
import bagging
import random_forest
import svc
import kernel_ridge
import model
import sys

import matplotlib.pyplot as plt

# TODO - Assess whether it is reasonable for the data to be giving higher accuracy on test than on training data -> seems not, but maybe due to little data?
if __name__ == '__main__':

	# py.tools.set_credentials_file(username='paulo892', api_key='AiZ0NJ9htO9OVySZNYtE')

	print('Start!')

	# reads in the dataset
	test_data = pd.read_csv('../Annotations_Adjusted.csv')

	# if necessary, trains the models
	if (sys.argv[1:][0] == 'create'):
		dec_tree = model.train(test_data, 'dec_tree')
		sgd = model.train(test_data, 'sgd')
		mlp = model.train(test_data, 'mlp')
		gaussian_nb = model.train(test_data, 'gaussian_nb')
		bagging = model.train(test_data, 'bagging')
		forest = model.train(test_data, 'forest')
		svc = model.train(test_data, 'svc')
		kr = model.train(test_data, 'kr')
		nn = model.train(test_data, 'nn')
	
	
	# TODO - work out table, look at code for spring IW master.py
