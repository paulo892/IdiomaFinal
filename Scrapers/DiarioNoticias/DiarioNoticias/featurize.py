import re
import json
import syllables
import textstat
import math

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

    # for lack of a better adjustment, subtracts some margin from score
    #syllables -= 0.5

    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0 :
       syllables == 0
       syllables = 1

    return syllables

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

    features = []

    # adjust text in various ways
    textA = re.sub('\.\.+', '', text)

    # TODO - develop module for eliciting features from text
    # TODO (A) - make it efficient lol

    # elicits number of sentences
    sentences = re.split('\.', textA)
    sentencesA = []
    for sen in sentences:
        if re.search('\s\w+\s', sen):
            sentencesA.append(sen)
    num_sentences = len(sentencesA)
    #print('Sentences:', num_sentences)
    features.append(('sentences', num_sentences))

    if num_sentences == 0:
        return features

    #for i, sen in enumerate(sentencesA):
        #print(sen, i)

    ## elicits number of words
    words = []
    num_words = 0
    for sen in sentencesA:
        words.extend(re.split('\s+', sen))

    # trims each word and removes non-words and non-alphanumerics
    wordsA = []
    for word in words:
        word = word.strip()
        if re.search('\w+', word):
            wordsA.append(re.sub(r'\W+', '', word))
    words = wordsA
    num_words = len(words)
    #print('Words:', num_words)
    features.append(('words', num_words))

    # elicits number of syllables
    num_syllables = 0
    for word in words:
        num_syllables += syllables(word)
    #print('Syllables:', num_syllables)
    features.append(('syllables', num_syllables))

    # elicits number of letters
    num_letters = 0
    for word in words:
        num_letters += len(word)
    #print('Letters:', num_letters)
    features.append(('letters', num_letters))

    # elicits number of unique words
    words_upper = [x.upper() for x in words]
    words_set = set(words_upper)
    num_unique_words = len(words_set)
    #print('Unique Words:', num_unique_words)
    features.append(('unique', num_unique_words))

    # calculates type-token ratio
    ttr = num_unique_words / num_words
    #print('Type-Token Ratio:', ttr)
    features.append(('ttr', ttr))

    # calculates flesch reading ease index
    # FH -> 206.84 - (0.6 * P) - (102 * F)
    f_huerta = 206.84 - (60) * (num_syllables/num_words) - (1.02) * (num_sentences/num_words)
    flesch = 206.835 - (84.6) * (num_syllables/num_words) - (1.015) * (num_words/num_sentences)
    #print('Flesch: ', flesch)
    #print('Fernandez-Huerta: ', f_huerta)
    features.append(('flesh-adap', flesch))
    features.append(('fern-huerta', f_huerta))

    # TODO - Make sure you use FH score in algorithm

    # calculates Coleman Liau (adjusted)
    coleman_liau = 5.730 * num_letters / num_words - 171.365 * num_sentences / num_words - 6.662
    #coleman_liau = 5.88 * num_letters / num_words - 29.6 * num_sentences / num_words - 15.8
    #print('Coleman Liau: ', coleman_liau)
    features.append(('coleman', coleman_liau))

    # calculates Flesch Kincaid (adjusted)
    flesch_kincaid = 0.883 * num_words / num_sentences + 17.347 * num_syllables / num_words - 41.239
    #flesch_kincaid = 0.39 * num_words / num_sentences + 11.8 * num_syllables / num_words - 15.59
    #print('Flesch Kincaid: ', flesch_kincaid)
    features.append(('flesch-grade', flesch_kincaid))

    # calculates Automated Readability Index (adjusted)
    #ari = 6.286 * num_letters / num_words + 0.927 * num_words / num_sentences - 36.551
    ari = 4.71 * num_letters / num_words + 0.5 * num_words / num_sentences - 21.43
    #print('ARI: ', ari)
    features.append(('ari', ari))

    # TODO - Find way to calculate complex words to calculate SMOG and ARI

    # calculates average number of letters per word
    avg_letters_per_word = num_letters / num_words
    #print('Average # letters per word: ', avg_letters_per_word)
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
    #print('SD # letters per word: ', sd_letters_per_word)
    features.append(('awlstd', sd_letters_per_word))

    # TODO - Try and use PALAVRAS parser to add other features

    # returns dummy dictionary
    return features


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
