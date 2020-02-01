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
import spacy

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

    tagged_text = [(w.text, w.tag_, w.pos_, w.lemma_) for w in doc]
    irregulars = ['ser', 'estar', 'poder', 'trazer', 'vir', 'fazer', 'dar', 'ir', 'ter', 'ouvir', 'ler', 'dizer', 'ver', 'querer']

    print(tagged_text)

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
    print(feature_list)

    return feature_list

def featurize_documents(path):
    print('here')

if __name__ == '__main__':

    featurize_text("eu esperava que você não ouvisse")