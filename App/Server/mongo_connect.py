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
import string
import utilities
import numpy as np
from urllib.parse import quote_plus
from pymongo.errors import ConnectionFailure
from flask import Flask, jsonify, request, redirect, session, render_template
from toposort import toposort, toposort_flatten
import random
import ast

# performs integrations with MongoDB Atlas DB
mongo = pymongo.MongoClient('mongodb+srv://paulo892:hello@cluster0-farth.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'idioma')
users = pymongo.collection.Collection(db, 'users')
achievements = pymongo.collection.Collection(db, 'achievements')
documents = pymongo.collection.Collection(db, 'featurized_diario_noticias_50iter')

# necessary Flask configurations
app = Flask(__name__, static_folder='../build/static', template_folder='../build/')
app.config.from_object(__name__)
CORS(app)

# dictionary of direct dependencies for use in top. sort
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

# dictionary of unrolled dependencies for use in matching alg.
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

# mapping of indices to grammatical topics
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
    12:"Presente Subjuntivo (Irregular)",
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

# mapping of grammatical topics to indices
topics_to_indices = {
    "Presente Indicativo (Regular)":0,
    "Presente Indicativo (Irregular)":1,
    "Ser vs. Estar":2,
    "Pretérito Indicativo (Regular)":3,
    "Pretérito Indicativo (Irregular)":4,
    "Imperfeito (Regular)":5,
    "Imperfeito (Irregular)":6,
    "Passado Subjuntivo (Regular)":7,
    "Passado Subjuntivo (Irregular)":8,
    "Presente Gerúndio":9,
    "Presente Perfeito":10,
    "Presente Subjuntivo (Regular)":11,
    "Presente Indicativo (Irregular)":12,
    "Pretérito Perfeito":13,
    "Futúro Indicativo (Regular)":14,
    "Futúro Indicativo (Irregular)":15,
    "Futúro Perfeito":16,
    "Condicional (Regular)":17,
    "Condicional (Irregular)":18,
    "Interrogativos":19,
    "Superlativos":20,
    "Preposiciões":21,
    "Números":22
}

# total number of features in script
NUMBER_OF_FEATURES = len(indices_to_topics)

# thresholds for determining user familiarity with features and for feature prevalence in doc
THRESHOLDS_FAM = [0, 10, 50, 100]
THRESHOLDS_PREV = [0, 5, 10, 20]

# number of thematical subjects to offer user
SUBS = 25

# score bonus for requested tag appearing in article
BONUS = 0.1

# mapping of achievements to ObjectIDs
ACHS_TO_IDS = {
    'first_session': '5dd603c61c9d4400004cadd8',
    'second_session': '5dd604231c9d4400004cadda',
    'first_doc': '5e655fb81c9d440000df11a1'
}

# helper class for writing to JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# retrieves the features a user has seen by their email
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

# retrieves the top 100 most common tags in data
@app.route('/api/getCommonTags', methods=['GET'])
def get_tags():
    # opens the corresponding file
    f = open('../../Data/top_100_tags.json', 'r')
    contents = json.load(f)
    f.close()

    # converts list to dict to appease Axios return types
    content_dict = {}
    for i, con in enumerate(contents):
        if i >= SUBS:
            break
        tag = con[0]
        tag = string.capwords(tag)
        content_dict[i] = tag

    return content_dict

# increments the number of user sessions
@app.route('/api/updateUserSessions', methods=['GET', 'POST'])
def update_user_sessions():
    # takes in user email from request
    email = request.args['email']

    # retrieves user object
    userquery = {"email": email}
    cursor1 = users.find(userquery)

    if (cursor1.count() > 1):
        print('ERROR: More than one user with same email.')

    usr = cursor1[0]

    # retrieves user's session count and increments it
    sessions = usr['sessions_completed']
    sessions += 1

    # gets list of user achievements
    ach = usr['achievements']

    ach_gained = None

    # if user now at one session completed...
    if sessions == 1:
        # adds achievement to list
        if ObjectId(ACHS_TO_IDS['first_session']) not in ach:
            ach.append(ObjectId(ACHS_TO_IDS['first_session']))

        # retrieves achievement object and extracts its name
        achquery = {"_id": ObjectId(ACHS_TO_IDS['first_session'])}
        cursor = achievements.find(achquery)
        achievement = cursor[0]
        ach_gained = achievement['name']

    # else if user now at two sessions completed...
    elif sessions == 2:
        # adds achievement to list
        if ObjectId(ACHS_TO_IDS['second_session']) not in ach:
            ach.append(ObjectId(ACHS_TO_IDS['second_session']))

        # retrieves achievement object and extracts its name
        achquery = {"_id": ObjectId(ACHS_TO_IDS['second_session'])}
        cursor = achievements.find(achquery)
        achievement = cursor[0]
        ach_gained = achievement['name']

    # updates user object
    newvalues = { "$set": { "sessions_completed": sessions, "achievements": ach}}
    users.update_one(userquery, newvalues)

    # if achievement gained...
    if ach_gained != None:
        return str(ach_gained)
    else:
        return 'NOACH'

# retrieves an appropriate article by user input and preferences
@app.route('/api/getArticleId', methods=['GET','POST'])
def get_article_by_input_and_prefs():

    # takes in user input and user email from request
    attributes = request.args.getlist('attributes[]')
    email = request.args['email']

    # determines the user level -> simple or difficult
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

    # calculates topological sort over nodes
    top_sort = utilities.top_sort_topics(top_dict)

    usr_feats_seen = usr['features_seen']

    feature_relevance={}

    # for each grammatical topic...
    for topic in top_sort:
        # retrieves its dependencies
        deps = dep_tree[topic]
        prev_seen = []

        # calculates its relevance
        # (-1, 0, 1) -> (irrelevant, neutral, relevant)
        
        # always marks "Present Indicative" as relevant
        if deps is None:
            feature_relevance[topic] = 1

        # if the user requested the topic, marks it as relevant
        elif indices_to_topics[topic] in attributes:
            feature_relevance[topic] = 1

        # for all other topics...
        else:
            # creates list of user's familiarity with topics on which this topic is dependent
            for dep in deps:
                occ = usr_feats_seen[dep]
                if occ < THRESHOLDS_FAM[0]:
                    print('ERROR: User cannot have seen feature less than 0 times.')
                # if user has seen feature b/w 0 and 10 times, unfamiliar -> 0
                elif occ < THRESHOLDS_FAM[1]:
                    lvl = 0
                # if user has seen feature b/w 10 and 50 times, familiar -> 1
                elif occ < THRESHOLDS_FAM[2]:
                    lvl = 1
                # if user has seen feature over 50 times, very familiar -> 2
                else:
                    lvl = 2

                prev_seen.append(lvl)

            # calculates proportions of 0s, 1s, and 2s in previous topic familiarities
            prev_len = len(prev_seen)
            zero_count = prev_seen.count(0)
            one_count = prev_seen.count(1)
            two_count = prev_seen.count(2)
            zero_prop = zero_count / prev_len
            one_prop = one_count / prev_len
            two_prop = two_count / prev_len

            ## calculates the relevance of the topic

            # if user has seen every topic on which this topic depends...
            if 0 not in prev_seen:
                # and seen this topic many times -> neutral
                if usr_feats_seen[topic] == 2:
                    feature_relevance[topic] = 0
                # and not seen this topic many times -> relevant
                else:
                    feature_relevance[topic] = 1
                    #print(2)

            # if user has not seen any topics on which this topic depends -> irrelevant
            elif 1 not in prev_seen and 2 not in prev_seen:
                feature_relevance[topic] = -1

            # if user has seen > 2/3 of topics on which this topic depends 
            # and has not seen many of this one -> relevant
            elif (one_prop + two_prop > 2/3) and (usr_feats_seen[topic] != 2):
                feature_relevance[topic] = 1

            # else -> neutral
            else:
                feature_relevance[topic] = -1

    # samples 100 documents from the pool of documents not yet read
    sample_size = 100 if len(documents_unseen) >= 100 else len(documents_unseen)
    sampled_docs = random.sample(documents_unseen, sample_size)

    doc_apps = {}

    # for each sampled doc...
    for doc in sampled_docs:

        # retrieves the number of appearances of all topics in text
        feature_prev = doc['features']

        # retrieves the document's tags
        tags = doc['tags']

        # normalizes the appearance count, according to system similar to one above
        feature_prev_normalized = [0 if x < THRESHOLDS_PREV[1] else 0.5 if x < THRESHOLDS_PREV[2] else 1 for x in feature_prev]

        # collates the relevances of each topic
        relevance_list = []
        for key in sorted(feature_relevance.keys()):
            relevance_list.append(feature_relevance[key])

        # multiplies the relevance and the prevalence (within the text) of each topic together
        temp = [a*b for a,b in zip(feature_prev_normalized, relevance_list)]
        # adds the above products together, and divides by the number of topics
        app = np.sum(temp) / NUMBER_OF_FEATURES

        # if any of the requested tags are in the article, adds the BONUS modifier to appropriateness
        for attr in attributes:
            if attr in tags:
                app += BONUS
                print(attr)
                break

        doc_apps[doc['_id']] = app

        ## this process produces a number in the range [-1,1 + BONUS]
    
    # selects the most appropriate document among those sampled
    best_doc = max(doc_apps, key=doc_apps.get)

    return str(best_doc)

# retrieves an article by its ID
@app.route('/api/getArticleData', methods=['GET','POST'])
def get_article_data():
    # takes in article ID from request
    articleId = request.args['articleId']

    # finds matching article and returns it
    docquery = {"_id": ObjectId(articleId)}
    cursor1 = documents.find(docquery)

    doc = cursor1[0]
    encoded_doc = JSONEncoder().encode(doc)
    return encoded_doc

# retrieves the document objects for documents seen by users
@app.route('/api/getUserDocuments', methods=['GET', 'POST'])
def get_user_documents():
    # takes in user email and search term from request
    email = request.args['email']
    search = request.args['search']

    # returns the user information
    userquery = {"email": email}
    cursor = users.find(userquery)

    if (cursor.count() > 1):
        print('ERROR: More than one user with same email.')
    
    usr = cursor[0]

    # extracts the documents seen by user
    docs_seen = usr['documents_seen']
    print(docs_seen)

    docs = {}

    # for each document already seen...
    for doc in docs_seen:
        # creates and runs query to find its data
        docquery = {"_id": ObjectId(doc), 'title': {'$regex': '.*' + search + '.*'}}
        cursor = documents.find(docquery)

        # if cursor empty, continues
        if cursor.count() == 0:
            continue

        # gets the document data and appends to list
        document = cursor[0]
        docs[str(document['_id'])] = JSONEncoder().encode(document)
    
    return jsonify(docs)

# retrieves the achievements unlocked by the user
@app.route('/api/getUserAchievements', methods=['GET','POST'])
def get_user_achievements():
    # takes in user email from request
    email = request.args['email']

    # returns the user information
    userquery = {"email": email}
    cursor = users.find(userquery)

    if (cursor.count() > 1):
        print('ERROR: More than one user with same email.')

    usr = cursor[0]

    # extracts the user achievements
    achieves = usr['achievements']

    achs = {}
    # for each achievement...
    for ach in achieves:
        # creates and runs query to find its data
        achquery = {"_id": ObjectId(ach)}
        cursor = achievements.find(achquery)

        # gets the achievement data and appends to list
        achievement = cursor[0]
        achs[str(achievement['_id'])] = JSONEncoder().encode(achievement)

    return jsonify(achs)

# retrieves all possible achievements
@app.route('/api/getAllAchievements', methods=['GET','POST'])
def get_all_achievements():

    # creates and executes achievement query
    achquery = {}
    cursor = achievements.find(achquery)

    achs = {}
    # for each achievement...
    for ach in cursor:
        # appends its data to a list
        achs[str(ach['_id'])] = JSONEncoder().encode(ach)

    return jsonify(achs)

# updates the documents and topics seen by the user 
@app.route('/api/updateUser', methods=['POST'])
def update_user():

    # takes in article ID, article features, and email from request
    data = ast.literal_eval(request.data.decode('utf-8'))
    article_id = data['articleViewed']
    article_feats = data['articleFeatures']
    email = data['email']

    # gets user info using email
    userquery = {"email": email}
    cursor = users.find(userquery)

    if (cursor.count() > 1):
        print('ERROR: More than one user with same email.')

    usr = cursor[0]

    # changes user's documents seen dictionary to include most recent document
    usr['documents_seen'].append(ObjectId(article_id))

    features_seen = usr['features_seen']
    if (len(features_seen) != len(article_feats)):
        print('ERROR: Two lists not the same length')

    # updates the topics that the user has seen
    new_features_seen = [sum(x) for x in zip(features_seen, article_feats)]

    # updates the number of documents the user has read
    docs_read = usr['documents_read']
    docs_read += 1

    # gets list of user achievements
    ach = usr['achievements']
    ach_gained = None

    # if number of documents read is now 1...
    if docs_read == 1:
        # adds achievement to list
        if ObjectId(ACHS_TO_IDS['first_doc']) not in ach:
            ach.append(ObjectId(ACHS_TO_IDS['first_doc']))

        # retrieves achievement object and extracts its name
        achquery = {"_id": ObjectId(ACHS_TO_IDS['first_doc'])}
        cursor = achievements.find(achquery)
        achievement = cursor[0]
        ach_gained = achievement['name']

    # updates user object in database
    newvalues = { "$set": { "documents_seen": usr['documents_seen'], "features_seen": new_features_seen, "achievements": ach, "documents_read": docs_read} }
    users.update_one(userquery, newvalues)

    # if achievement gained...
    if ach_gained != None:
        return str(ach_gained)
    else:
        return 'NOACH'

if __name__ == '__main__':

    app.run(debug=True)