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


def top_sort_topics(top_dict):

    top_sort = toposort_flatten(top_dict)

    return top_sort

def featurize_text(text):
    # TOWRITE - talk about the process of elimination you had to do against the github repo for the tagger
    # passado subjuntivo is actually preterito imperfeito
    # TODO - straighten out list of topics later (https://www.soportugues.com.br/secoes/morf/morf62.php)

    # loads spacy model and tags text
    nlp = spacy.load('pt_core_news_sm')
    text = text
    doc = nlp(text)

    tagged_text = [(w.text, w.tag_, w.pos_, w.lemma_, w.idx) for w in doc]
    print(tagged_text)
    irregulars = ['ser', 'estar', 'poder', 'trazer', 'vir', 'fazer', 'dar', 'ir', 'ter', 'ouvir', 'ler', 'dizer', 'ver', 'querer']

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

    # get counts for most features in the text
    for i, token in enumerate(tagged_text):

        word = token[0]
        desc = token[1]
        lemma = token[3]

        # TODO - build dictionaries to reference against in determining whether regulars or irregulars

        # presente indicativo (regular e irregular)
        if 'PR' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[1] = feature_counts[1] + 1
            else:
                feature_counts[0] = feature_counts[0] + 1

        # pretérito indicativo (regular e irregular)
        elif 'PS' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[4] = feature_counts[4] + 1
            else:
                feature_counts[3] = feature_counts[3] + 1

        # imperfeito indicativo (regular e irregular)
        elif 'IMPF' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[6] = feature_counts[6] + 1
            else:
                feature_counts[5] = feature_counts[5] + 1

        # imperfeito subjuntivo
        elif 'IMPF' in desc and 'SUBJ' in desc:
            if lemma in irregulars:
                feature_counts[8] = feature_counts[8] + 1
            else:
                feature_counts[7] = feature_counts[7] + 1

        # gerúndio
        elif 'GER' in desc:
            feature_counts[9] = feature_counts[9] + 1

        # presente subjuntivo (regular e irregular)
        elif 'PR' in desc and 'SUBJ' in desc:
            if lemma in irregulars:
                feature_counts[12] = feature_counts[12] + 1
            else:
                feature_counts[11] = feature_counts[11] + 1

        # futúro indicativo (regular e irregular)
        elif 'FUT' in desc and 'IND' in desc:
            if lemma in irregulars:
                feature_counts[15] = feature_counts[15] + 1
            else:
                feature_counts[14] = feature_counts[14] + 1

        # condicional (regular e irregular)
        elif 'COND' in desc:
            if lemma in irregulars:
                feature_counts[18] = feature_counts[18] + 1
            else:
                feature_counts[17] = feature_counts[17] + 1

        # número
        elif 'NUM' in desc:
            feature_counts[22] = feature_counts[22] + 1


        # perfeitos
        if 'PCP' in desc:

            # will not consider first token
            if i != 0:

                prev = tagged_text[i - 1][1].strip()

                # pretérito perfeito composto
                if prev in ['tenho', 'tem', 'temos', 'têm']:
                    feature_counts[10] = feature_counts[10] + 1

                # pretérito mais-que-perfeito composto
                elif prev in ['tinha', 'tinham', 'tínhamos']:
                    feature_counts[13] = feature_counts[13] + 1

                # futúro composto
                if prev in ['terei', 'terá', 'teremos', 'terão']:
                    feature_counts[16] = feature_counts[16] + 1

        # ser e estar
        if lemma == 'ser' or lemma == 'estar':
            feature_counts[2] = feature_counts[2] + 1

        # superlativo absoluto
        if word.find('íssimo') != -1:
            feature_counts[20] = feature_counts[20] + 1

        # TODO - deal with interrogativos e preposições

    # converts the dict to a list and returns
    feature_list = list(feature_counts.values())

    return feature_list

def featurize_documents(path):
    docs = open(path, 'r+')
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

def model_documents(path):
    docs = open(path, 'r+')
    data = json.load(docs)

    docs_featurized = open("../../Scrapers/DiarioNoticias/DiarioNoticias/featurized_diario_noticias_50iter.json", 'r+')
    data_featurized = json.load(docs_featurized)

    docs_modeled = []
    model = load('../../Models/forest.joblib') 

    # TODO - get data in the same format as the model application script, or figure out how to do it with json format
    # docid,sentences,words,syllables,letters,unique,ttr,flesch-adap,coleman,flesch-gradelevel,ari,awl,awlstd,psfl,zh,wiki,brescola
    #[('sentences', 17), ('words', 497), ('syllables', 998), ('letters', 2533), ('unique', 251), ('ttr', 0.5050301810865191), ('flesh-adap', 7.280291158717024), ('fern-huerta', 86.32221327967807), ('coleman', 16.679820925553326), ('flesch-grade', 19.40937838797491), ('ari', 17.192536394839628), ('awl', 5.096579476861167), ('awlstd', 3.1665264420926857)]

    res_dict = {}

    # for each document in json...
    for i, doc in enumerate(data):

        new_doc = doc

        if i % 100 == 0:
            print(i)

        # get document link
        link = doc['link']
        syntactic_feats = data_featurized[link]

        # if sentence count 0, continues
        sentences = syntactic_feats[0]
        if sentences[1] == 0:
            continue

        # appends each relevant doc feature to list (features in csv)
        doc_elements = []

        # docid [link]
        #doc_elements.append(link)
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
        # flesch-gradelevel
        doc_elements.append(syntactic_feats[9][1])
        # ari
        doc_elements.append(syntactic_feats[10][1])
        # awl
        doc_elements.append(syntactic_feats[11][1])
        # awlstd
        doc_elements.append(syntactic_feats[12][1])

        # TODO - Figure out how to implement feature selection here as well!
        #print(doc_elements)



        pred = model.predict(np.asarray(doc_elements).reshape(1, -1))
        new_doc['diff'] = pred[0]
        docs_modeled.append(new_doc)

    f = open('final_featurized_diario_noticias_50iter.json', 'w+')
    f.write(json.dumps(docs_modeled))
    f.close()

if __name__ == '__main__':

    featurize_text("Eu vou começar a jogar à bola.")
    #featurize_documents("../../Scrapers/DiarioNoticias/DiarioNoticias/diario_noticias_50iter.json")
    #model_documents("./docs_featurized_1.json")