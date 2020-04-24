import re
import json
import numpy as np
import syllables
import textstat
import math
import spacy
import pickle
import sklearn
import operator
from sklearn.ensemble import RandomForestClassifier

CLASSFEAT_TO_INDEX = {
    'sentences': 0,
    'words': 1,
    'syllables': 2,
    'letters': 3,
    'unique': 4,
    'ttr': 5,
    'flesch-adap': 6,
    'coleman': 7,
    'flesch-grade level': 8,
    'ari': 9,
    'awl': 10,
    'awlstd': 11
}

def syllables(word):
    # Count the syllables in the word.
    syllables = 0
    for i in range(len(word)):

       # If the first letter in the word is a vowel then it is a syllable.
       if i == 0 and word[i] in "aeiouy" :
          syllables = syllables + 1

       # Else if the previous letter is not a vowel.
       elif word[i - 1] not in "aeiouy" :

          # If it is no the last letter in the word and it is a vowel.
          if i < len(word) - 1 and word[i] in "aeiouy" :
             syllables = syllables + 1

          # Else if it is the last letter and it is a vowel that is not e.
          elif i == len(word) - 1 and word[i] in "aiouy" :
             syllables = syllables + 1

    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0 :
       syllables == 0
       syllables = 1

    return syllables

# extracts features for selection algorithm
def featurize_sel(text):

    # loads spacy model and tags text
    nlp = spacy.load('pt_core_news_sm')
    text = text
    doc = nlp(text)
    tagged_text = [(w.text, w.tag_, w.pos_, w.lemma_, w.idx) for w in doc]

    # list of irregular verbs for consideration in featurization
    irregulars = ['ser', 'estar', 'poder', 'trazer', 'vir', 'fazer', 'dar', 'ir', 'ter', 'ouvir', 'ler', 'dizer', 'ver', 'querer']

    # number of times each feature appears in the text (see mongo_connect.py script in "Server" directory for mapping)
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

# extracts features for classification
def featurize_class(text):

    features = []

    # removes repeated periods from text
    textA = re.sub('\.\.+', '', text)

    # calculates number of sentences by splitting on periods and taking tokens with at least one character
    sentences = re.split('\.', textA)
    sentencesA = []
    for sen in sentences:
        if re.search('\s\w+\s', sen):
            sentencesA.append(sen)
    num_sentences = len(sentencesA)
    features.append(('sentences', num_sentences))

    # if no sentences, returns (empty document)
    if num_sentences == 0:
        return features

    # calculates number of words by splitting on whitecase, trimming, and removing non-alphanumerics
    words = []
    num_words = 0
    for sen in sentencesA:
        words.extend(re.split('\s+', sen))

    wordsA = []
    for word in words:
        word = word.strip()
        if re.search('\w+', word):
            wordsA.append(re.sub(r'\W+', '', word))
    words = wordsA
    num_words = len(words)
    features.append(('words', num_words))

    # calculates number of syllables
    num_syllables = 0
    for word in words:
        num_syllables += syllables(word)
    features.append(('syllables', num_syllables))

    # calculates number of letters
    num_letters = 0
    for word in words:
        num_letters += len(word)
    features.append(('letters', num_letters))

    # calculates number of unique words
    words_upper = [x.upper() for x in words]
    words_set = set(words_upper)
    num_unique_words = len(words_set)
    features.append(('unique', num_unique_words))

    # calculates type-token ratio
    ttr = num_unique_words / num_words
    features.append(('ttr', ttr))

    # calculates flesch reading ease index and fernandez huerta metric
    # FH -> 206.84 - (0.6 * P) - (102 * F)
    f_huerta = 206.84 - (60) * (num_syllables/num_words) - (1.02) * (num_sentences/num_words)
    flesch = 206.835 - (84.6) * (num_syllables/num_words) - (1.015) * (num_words/num_sentences)
    features.append(('flesh-adap', flesch))
    features.append(('fern-huerta', f_huerta))

    # calculates Coleman Liau (adjusted)
    coleman_liau = 5.730 * num_letters / num_words - 171.365 * num_sentences / num_words - 6.662
    features.append(('coleman', coleman_liau))

    # calculates Flesch Kincaid (adjusted)
    flesch_kincaid = 0.883 * num_words / num_sentences + 17.347 * num_syllables / num_words - 41.239
    features.append(('flesch-grade', flesch_kincaid))

    # calculates Automated Readability Index (adjusted)
    ari = 4.71 * num_letters / num_words + 0.5 * num_words / num_sentences - 21.43
    features.append(('ari', ari))

    # calculates average number of letters per word
    avg_letters_per_word = num_letters / num_words
    features.append(('awl', avg_letters_per_word))

    # calculates SD of number of letters per word
    sum = 0
    for word in words:
        letters = len(word)
        temp = letters - avg_letters_per_word
        temp_sq = temp * temp
        sum += temp_sq

    div = sum / num_words
    sd_letters_per_word = math.sqrt(div)
    features.append(('awlstd', sd_letters_per_word))

    # returns dummy dictionary
    return features

# applies the modeling scheme to the featurized data
def model_documents(syntactic_feats):

    # loads the models
    model1 = pickle.load(open('../Models/saved_models/forest.sav', 'rb'))
    model2 = pickle.load(open('../Models/saved_models/mlp.sav', 'rb'))
    model3 = pickle.load(open('../Models/saved_models/bagging.sav', 'rb'))

    # opens the file containing the features used to train each document
    f = open('model_features.json', 'r+')
    contents = json.load(f)
    f.close()

    res_dict = {}

    # if sentence count 0, returns
    sentences = syntactic_feats[0]
    if sentences[1] == 0:
        return 'n/a'

    # predicts the label using the three models
    pred1 = model1.predict(np.asarray([syntactic_feats[CLASSFEAT_TO_INDEX[x]][1] for x in contents['forest']]).reshape(1, -1))
    pred2 = model2.predict(np.asarray([syntactic_feats[CLASSFEAT_TO_INDEX[x]][1] for x in contents['mlp']]).reshape(1, -1))
    pred3 = model3.predict(np.asarray([syntactic_feats[CLASSFEAT_TO_INDEX[x]][1] for x in contents['bagging']]).reshape(1, -1))
    preds = [pred1, pred2, pred3]

    # takes the maximum of the three outputs
    d = 0
    s = 0
    for pred in preds:
        if pred == 'd':
            d += 1
        elif pred == 's':
            s += 1
        else:
            print('ERROR: Invalid classification.')

    # returns the predicted label in new document
    if d > s:
        return 'd'
    elif s > d:
        return 's'

if __name__ == '__main__':

    # takes in name of file
    #filename = input("Enter the name of the file to featurize: ")

    # opens file to be featurized
    #file = open(filename, "r+")
    #contents = json.load(file)

    #featurized_docs = []

    # for each document in file...
    #for i, doc in enumerate(contents):
    #    doc_id = doc['link']
    #    formatted = doc['text']

        #if i % 10 == 0:
        #    print('HERE')

        # calculates features for classification
        #class_features = featurize_class(formatted)

        # uses classification features to classify document difficulty
        #diff = model_documents(class_features)

        # if 'n/a' returned, does not include document
        #if diff == 'n/a':
         #   continue

        # calculates features for document selection
        #el_features = featurize_sel(formatted)

        # adds classification and selection features to document
        #doc['features'] = sel_features
        #doc['diff'] = diff
        #featurized_docs.append(doc)

    # writes feature sets to a document
    #file = filename.split('/')
    #f = open('./Data/featurized_' + file[-1], 'w+')
    #f.write(json.dumps(featurized_docs))
    #f.close()

    ## creates list of the 100 most common tags in the DB

    # opens correct file
    f = open('../Data/featurized_diario_noticias_50iter.json', 'r')
    contents = json.load(f)
    f.close()

    tag_counts = {}

    # for each document...
    for doc in contents:
        tags = doc['tags']

        # for each tag...
        for tag in tags:
            # updates its count in the dict
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1

    # sorts the dict
    sorted_tags = sorted(tag_counts.items(), key=operator.itemgetter(1),reverse=True)

    # saves the first 100 entries in the list
    top_100 = sorted_tags[0:100]

    # writes the result to a file
    f = open('../Data/top_100_tags.json', 'w+')
    f.write(json.dumps(top_100))
    f.close()

