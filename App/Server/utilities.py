from flask import Flask, jsonify, request, redirect, session, render_template
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_cas import login_required, CAS, login, logout
from flask_cors import CORS
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import pymongo
from bson.json_util import dumps
import json
from urllib.parse import quote_plus
from pymongo.errors import ConnectionFailure
from flask import Flask, jsonify, request, redirect, session, render_template
from toposort import toposort, toposort_flatten
from joblib import load
import numpy as np
import spacy
import sklearn

# topologically sorts argument dictionary
def top_sort_topics(top_dict):
    return toposort_flatten(top_dict)

# featurizes the text
def featurize_text(text):

    # loads spacy model and tags text
    nlp = spacy.load('pt_core_news_sm')
    text = text
    doc = nlp(text)
    tagged_text = [(w.text, w.tag_, w.pos_, w.lemma_, w.idx) for w in doc]

    # list of irregular verbs for consideration in featurization
    irregulars = ['ser', 'estar', 'poder', 'trazer', 'vir', 'fazer', 'dar', 'ir', 'ter', 'ouvir', 'ler', 'dizer', 'ver', 'querer']

    # number of times each feature appears in the text (see mongo_connect.py for mapping)
    feature_counts = {
        0:0,
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0,
        11:0,
        12:0,
        13:0,
        14:0,
        15:0,
        16:0,
        17:0,
        18:0,
        19:0,
        20:0,
        21:0,
        22:0
    }

    # for each token in the text...
    for i, token in enumerate(tagged_text):

        # saves the word, description, and lemma
        word = token[0]
        desc = token[1]
        lemma = token[3]

        # checks if present tense, regular or irregular
        if 'PR' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[1] = feature_counts[1] + 1
            else:
                feature_counts[0] = feature_counts[0] + 1

        # checks if preterite tense, regular or irregular
        elif 'PS' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[4] = feature_counts[4] + 1
            else:
                feature_counts[3] = feature_counts[3] + 1

        # checks if imperfect tense, regular or irregular
        elif 'IMPF' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[6] = feature_counts[6] + 1
            else:
                feature_counts[5] = feature_counts[5] + 1

        # checks if imperfect subjunctive tense, regular or irregular
        elif 'IMPF' in desc and 'SUBJ' in desc:
            if lemma in irregulars:
                feature_counts[8] = feature_counts[8] + 1
            else:
                feature_counts[7] = feature_counts[7] + 1

        # checks if gerund
        elif 'GER' in desc:
            feature_counts[9] = feature_counts[9] + 1

        # checks if present subjunctive tense, regular or irregular
        elif 'PR' in desc and 'SUBJ' in desc:
            if lemma in irregulars:
                feature_counts[12] = feature_counts[12] + 1
            else:
                feature_counts[11] = feature_counts[11] + 1

        # checks if future indicative, regular or irregular
        elif 'FUT' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[15] = feature_counts[15] + 1
            else:
                feature_counts[14] = feature_counts[14] + 1

        # checks if conditional tense, regular or irregular
        elif 'COND' in desc:
            if lemma in irregulars:
                feature_counts[18] = feature_counts[18] + 1
            else:
                feature_counts[17] = feature_counts[17] + 1

        # checks if number
        elif 'NUM' in desc:
            feature_counts[22] = feature_counts[22] + 1

        # if token is a perfect tense...
        if 'PCP' in desc:

            # skips the first term
            if i != 0:
                # looks back at the first term to determine type of perfect tense
                prev = tagged_text[i - 1][1].strip()

                # checks if preterite perfect composite tense
                if prev in ['tenho', 'tem', 'temos', 'têm']:
                    feature_counts[10] = feature_counts[10] + 1

                # checks if preterite more-than-perfect composite tense
                elif prev in ['tinha', 'tinham', 'tínhamos']:
                    feature_counts[13] = feature_counts[13] + 1

                # checks if future perfect composite tense
                if prev in ['terei', 'terá', 'teremos', 'terão']:
                    feature_counts[16] = feature_counts[16] + 1

        # checks for 'ser' or 'estar'
        if lemma == 'ser' or lemma == 'estar':
            feature_counts[2] = feature_counts[2] + 1

        # checks for superlatives
        if word.find('íssimo') != -1:
            feature_counts[20] = feature_counts[20] + 1

    # converts the dict to a list and returns
    feature_list = list(feature_counts.values())
    return feature_list

# featurizes all of the documents in the path directory, 
# dumping the results in docs_featurized_1.json
def featurize_documents(path):
    docs = open(path, 'r+')
    data = json.load(docs)
    docs_featurized = []

    for i, doc in enumerate(data):
        features = featurize_text(doc['text'])
        doc['features'] = features
        docs_featurized.append(doc)

    with open('docs_featurized_1.json', 'w') as outfile:
        json.dump(docs_featurized, outfile)

# applies the modeling scheme to the featurized data
def model_documents(path):
    # opens the documents, as well as their featurized version
    docs = open(path, 'r+')
    data = json.load(docs)
    docs_featurized = open("../../Scrapers/DiarioNoticias/DiarioNoticias/featurized_diario_noticias_50iter.json", 'r+')
    data_featurized = json.load(docs_featurized)

    docs_modeled = []

    # loads the models
    # TODO - change this
    model = load('../../Models/forest.joblib') 

    res_dict = {}

    # for each document in json...
    for i, doc in enumerate(data):

        # copies the document
        new_doc = doc

        # gets the document link
        link = doc['link']
        syntactic_feats = data_featurized[link]

        # if sentence count 0, continues
        sentences = syntactic_feats[0]
        if sentences[1] == 0:
            continue

        # appends each relevant doc feature to list (features in csv)
        doc_elements = []

        # sentences
        doc_elements.append(syntactic_feats[0][1])
        # words
        doc_elements.append(syntactic_feats[1][1])
        # syllables
        doc_elements.append(syntactic_feats[2][1])
        # letters
        doc_elements.append(syntactic_feats[3][1])
        # unique
        doc_elements.append(syntactic_feats[4][1])
        # ttr
        doc_elements.append(syntactic_feats[5][1])
        # flesch-adap
        doc_elements.append(syntactic_feats[6][1])
        # coleman
        doc_elements.append(syntactic_feats[8][1])
        # flesch-grade level
        doc_elements.append(syntactic_feats[9][1])
        # ari
        doc_elements.append(syntactic_feats[10][1])
        # awl
        doc_elements.append(syntactic_feats[11][1])
        # awlstd
        doc_elements.append(syntactic_feats[12][1])

        # predicts using the model
        pred = model.predict(np.asarray(doc_elements).reshape(1, -1))

        # saves the predicted label in new document
        new_doc['diff'] = pred[0]
        docs_modeled.append(new_doc)

    # writes the result to a file
    f = open('final_featurized_diario_noticias_50iter.json', 'w+')
    f.write(json.dumps(docs_modeled))
    f.close()

if __name__ == '__main__':

    # testing calls
    featurize_text("Eu vou começar a jogar à bola.")
    featurize_documents("../../Scrapers/DiarioNoticias/DiarioNoticias/diario_noticias_50iter.json")
    model_documents("./docs_featurized_1.json")