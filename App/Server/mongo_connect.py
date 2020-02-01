from flask import Flask, jsonify, request, redirect, session, render_template
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_cas import login_required, CAS, login, logout
from flask_cors import CORS
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
import utilities
import numpy as np
from urllib.parse import quote_plus
from pymongo.errors import ConnectionFailure
from flask import Flask, jsonify, request, redirect, session, render_template
from toposort import toposort, toposort_flatten
import random


mongo = pymongo.MongoClient('mongodb+srv://paulo892:hello@cluster0-farth.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'idioma')
users = pymongo.collection.Collection(db, 'users')
documents = pymongo.collection.Collection(db, 'documents')

app = Flask(__name__, static_folder='../build/static', template_folder='../build/')
app.config.from_object(__name__)
CORS(app)

top_dict = {
    1:{0},
    2:{0},
    3:{0},
    4:{3},
    5:{0},
    6:{5},
    7:{4,6},
    8:{7},
    9:{0},
    10:{0},
    11:{1},
    12:{11},
    13:{10, 4},
    14:{1},
    15:{14},
    16:{15},
    17:{14},
    18:{17},
    19:{0},
    20:{0},
    21:{0},
    22:{0}
}

# TODO - function that automatically creates this unrolled dependency tree 
dep_tree = {
    0:None,
    1:{0},
    2:{0},
    3:{0},
    4:{0,3},
    5:{0},
    6:{0,5},
    7:{0,3,4,5,6},
    8:{0,3,4,5,6,7},
    9:{0},
    10:{0},
    11:{0,1},
    12:{0,1,11},
    13:{0,3,4,10},
    14:{0,1},
    15:{0,1,14},
    16:{0,1,14,15},
    17:{0,1,14},
    18:{0,1,14,17},
    19:{0},
    20:{0},
    21:{0},
    22:{0}
}

indices_to_topics = {
    0:"Presente Indicativo (Regular)",
    1:"Presente Indicativo (Irregular)",
    2:"Ser vs. Estar",
    3:"Pretérito Indicativo (Regular)",
    4:"Pretérito Indicativo (Irregular)",
    5:"Imperfeito (Regular)",
    6:"Imperfeito (Irregular)",
    7:"Passado Subjuntivo (Regular)",
    8:"Passado Subjuntivo (Irregular)",
    9:"Presente Gerúndio",
    10:"Presente Perfeito",
    11:"Presente Subjuntivo (Regular)",
    12:"Presente Indicativo (Irregular)",
    13:"Pretérito Perfeito",
    14:"Futúro Indicativo (Regular)",
    15:"Futúro Indicativo (Irregular)",
    16:"Futúro Perfeito",
    17:"Condicional (Regular)",
    18:"Condicional (Irregular)",
    19:"Interrogativos",
    20:"Superlativos",
    21:"Preposiciões",
    22:"Números"
}

NUMBER_OF_FEATURES = len(indices_to_topics)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


@app.route('/api/getUserExperience', methods=['GET'])
def get_user_experience():

    # takes in user email
    email = request.args['email']

    # returns the user information
    userquery = {"email": email}
    cursor = users.find(userquery)

    if (cursor.count() > 1):
        print('ERROR: More than one user with same email.')

    usr = cursor[0]

    # extracts the number of times user has seen each feature
    usr_exp = usr['features_seen']

    return jsonify(usr_exp)

@app.route('/api/getArticleId', methods=['GET','POST'])
def get_article_by_input_and_prefs():

    # takes in user input and user email from request
    attributes = request.args.getlist('attributes[]')
    email = request.args['email']

    # determines what level user is at -> simple or difficult
    userquery = {"email": email}
    cursor1 = users.find(userquery)

    if (cursor1.count() > 1):
        print('ERROR: More than one user with same email.')

    usr = cursor1[0]

    usr_level = usr['level']

    # performs query to retrieve all documents of user's level
    levelquery = {"diff": usr_level}
    cursor2 = documents.find(levelquery)

    documents_right_level = []
    for doc in cursor2:
        documents_right_level.append(doc)

    # filters out all documents already seen by user
    usr_docs_seen = usr['documents_seen']
    documents_unseen = []
    for doc in documents_right_level:
        if doc['_id'] not in usr_docs_seen:
            documents_unseen.append(doc)

    ## performs matching algorithm to narrow down documents further

    # calculates topological sort over nodes -> TODO - maybe move this out of thsi function call
    top_sort = utilities.top_sort_topics(top_dict)

    # TODO - ensure that this array is always of the length of the number of features in consideration in mongo
    usr_feats_seen = usr['features_seen']

    feature_relevance={}

    # for each topic node...
    for topic in top_sort:
        print('Topic:', indices_to_topics[topic])
        print('Number of times seen(roughly):', usr_feats_seen[topic])
        deps = dep_tree[topic]
        prev_seen = []

        # always marks "Presente Indicativo (Regular)" as relevant
        if deps is None:
            feature_relevance[topic] = 1

        # for all other topics...
        else:
            # gets list of degree of familiarity with topics on which dependent
            for dep in deps:
                prev_seen.append(usr_feats_seen[dep])

            # calculates proportions of 0s, 1s, and 2s in previous topic familiarities
            prev_len = len(prev_seen)
            zero_count = prev_seen.count(0)
            one_count = prev_seen.count(1)
            two_count = prev_seen.count(2)
            zero_prop = zero_count / prev_len
            one_prop = one_count / prev_len
            two_prop = two_count / prev_len

            # if user has seen every previous topic...
            if 0 not in prev_seen:
                # and seen this topic many (10+) times, neutral relevance
                if usr_feats_seen[topic] == 2:
                    print(1)
                    feature_relevance[topic] = 0
                # and not seen this topic many times, relevant
                else:
                    feature_relevance[topic] = 1
                    print(2)

            # if user has not seen any of the previous topics, irrelevant
            elif 1 not in prev_seen and 2 not in prev_seen:
                feature_relevance[topic] = -1
                print(3)

            # TODO - flesh this out
            # if user has seen > 2/3 of previous topics and has not seen many of this one, relevant
            elif (one_prop + two_prop > 2/3) and (usr_feats_seen[topic] != 2):
                feature_relevance[topic] = 1
                print(4)

            # else, neutral
            else:
                feature_relevance[topic] = -1
                print(5)
        print('Result', feature_relevance[topic])

    # TODO - finalize threshold a document should meet to be considered appropriate

    # sample 100 documents
    sample_size = 100 if len(documents_unseen) >= 100 else len(documents_unseen)
    sampled_docs = random.sample(documents_unseen, sample_size)

    app_docs = {}

    # for each sampled doc...
    for doc in sampled_docs:
        # for each feature, nurmalizes its prevalence in text, multiplies it by relevance, and adds them together
        # divides sum by number of feature
        # range: [-1,1]
        feature_prev = doc['features']
        feature_prev_normalized = [0 if x==0 else 0.5 if x==1 else 1 for x in feature_prev]

        relevance_list = []
        for key in sorted(feature_relevance.keys()):
            relevance_list.append(feature_relevance[key])

        print(feature_prev_normalized)
        print(relevance_list)
        print(NUMBER_OF_FEATURES)

        temp = [a*b for a,b in zip(feature_prev_normalized, relevance_list)]
        print(temp)
        app = np.sum(temp) / NUMBER_OF_FEATURES
        print('app', app)

        #if app >= 0.5:
            #app_docs[doc['_id']] = app

        app_docs[doc['_id']] = app

    best_doc = max(app_docs, key=app_docs.get)

    return str(best_doc)

@app.route('/api/getArticleData', methods=['GET','POST'])
def get_article_data():
    # takes in user input and user email from request
    articleId = request.args['articleId']

    print(articleId)

    # determines what level user is at -> simple or difficult
    docquery = {"_id": ObjectId(articleId)}
    cursor1 = documents.find(docquery)

    doc = cursor1[0]
    encoded_doc = JSONEncoder().encode(doc)
    return encoded_doc

# TODO - API function called when user leaves document page that updates user object!

if __name__ == '__main__':

    app.run(debug=True)