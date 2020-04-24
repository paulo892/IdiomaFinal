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
import nearest_neighbor
import sgd_classifier
import mlp_classifier
import gaussian_nb
import bagging
import random_forest
import svc
import kernel_ridge
import plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pickle
from joblib import dump, load

if __name__ == '__main__':

	# loads saved model
	model = load('forest.joblib')

	# applies model to all test cases
	docs = open("../Scrapers/DiarioNoticias/DiarioNoticias/diario_noticias_50iter.json", 'r+')
    data = json.load(docs)
    docs_featurized = []

    for i, doc in enumerate(data):
        #if i > 10:
            #break
        features = featurize_text(doc['text'])
        doc['features'] = features
        docs_featurized.append(doc)

    with open('docs_featurized_1.json', 'w') as outfile:
        json.dump(docs_featurized, outfile)

    print(docs_featurized)
