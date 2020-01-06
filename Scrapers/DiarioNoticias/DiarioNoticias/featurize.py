import re
import json
import syllables

def format_brwac(text):
    
    # extracts document id from text
    start_idx = text.find('docid=') + 6
    end_idx = text.find(' title=')
    doc_id = text[start_idx: end_idx]

    ## populates the feature dictionary
    features = {}

    # partitions text into chunks by <p>, taking the last chunk as the text
    p_chunks = re.split('<p>', text)
    meta = p_chunks[0]
    p_chunks = p_chunks[1:]
    words = p_chunks[-1]

    # formats the text
    words = words.replace('</p>', '')
    words = words.replace('\n<g/>\n', '')
    words = words.replace('</s>\n<s>', '')
    words = words.replace('<s>', '')
    words = words.replace('</doc>', '')
    words = words.replace('\n', ' ')

    return [doc_id, words]

# TODO - develop function for eliciting features from text
def featurize(text):

    # adjust text in various ways
    textA = re.sub('\.\.+', '', text)

    # TODO - develop module for eliciting features from text
    # TODO (A) - make it efficient lol

    # elicits number of sentences
    sentences = re.split('\.', textA)
    num_sentences = len(sentences)
    print('Sentences:', num_sentences)

    ## elicits number of words
    words = []
    num_words = 0
    for sen in sentences:
        words.extend(re.split('\s+', sen))

    # trims each word and removes non-words
    wordsA = []
    for word in words:
        word = word.strip()
        if re.search('\w+', word):
            wordsA.append(word)
    words = wordsA
    num_words = len(words)
    print('Words:', num_words)

    # elicits number of syllables
    num_syllables = 0
    for word in words:
        num_syllables += syllables.estimate(word)
    print('Syllables:', num_syllables)

    

    # returns dummy dictionary
    return {'words': 2, 'length': 5}


if __name__ == '__main__':

    # takes in name of file
    filename = input("Enter the name of the file to featurize: ")

    # opens file
    file = open(filename, "r")
    contents = file.read()

    # determines kind of file
    filetype = input("What kind of file are you featurizing? [0 - BRWAC, 1 - Scrapy scraped]")

    features = {}

    # if brwac file, ...
    if filetype == '0':
        file = open(filename, "r")
        contents = file.read()

        docs = [x+'</doc>' for x in re.split('</doc>', contents)]

        # featurizes each text
        for i, doc in enumerate(docs):
            doc_id, formatted = format_brwac(doc)
            features[doc_id] = featurize(formatted)

    # if scrapy file, ...
    if filetype == '1':
        file = open(filename, "r")
        contents = json.load(file)

        # featurizes each text
        for i, doc in enumerate(contents):
            # TODO - save each document by smth other than link
            # might need to give them all ids ahead of time
            doc_id = doc['link']
            formatted = doc['text']
            features[doc_id] = featurize(formatted)

    # writes feature sets to a document
    f = open('featurized_' + filename, 'w+')
    f.write(str(features))
    f.close()
