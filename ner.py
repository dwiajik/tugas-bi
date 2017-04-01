from os import listdir
from os.path import isfile, join
import operator
import re

import nltk
from nltk.corpus import stopwords
#from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

english_stopwords = set(stopwords.words('english'))
#stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

pos_path = 'Movie Reviews Data Set/review_polarity/txt_sentoken/pos'
neg_path = 'Movie Reviews Data Set/review_polarity/txt_sentoken/neg'

pos_files = [join(pos_path, f) for f in listdir(pos_path) if isfile(join(pos_path, f))]
neg_files = [join(neg_path, f) for f in listdir(neg_path) if isfile(join(neg_path, f))]

pos_words = {}
neg_words = {}

for file_path in pos_files:
    with open(file_path) as f:
        for line in f:
            line = re.sub(r'\s[^a-zA-Z0-9]',' ', line) 
            tokens = line.split()
            tokens = [lemmatizer.lemmatize(token).encode("ascii") \
                for token in tokens \
                if '\'s' not in token \
                and '\'t' not in token]
            tokens = nltk.pos_tag(tokens)
            for token in tokens:
                #token = stemmer.stem(token)
                #token = lemmatizer.lemmatize(token).encode("ascii")
                if 'NN' in token[1] and token[0] not in english_stopwords:
                    try:
                        pos_words[token] += 1
                    except:
                        pos_words[token] = 1

for file_path in neg_files:
    with open(file_path) as f:
        for line in f:
            line = re.sub(r'\s[^a-zA-Z0-9]',' ', line) 
            tokens = line.split()
            tokens = [lemmatizer.lemmatize(token).encode("ascii") \
                for token in tokens \
                if '\'s' not in token \
                and '\'t' not in token]
            tokens = nltk.pos_tag(tokens)
            for token in tokens:
                #token = stemmer.stem(token)
                #token = lemmatizer.lemmatize(token).encode("ascii")
                if 'NN' in token[1] and token[0] not in english_stopwords:
                    try:
                        neg_words[token] += 1
                    except:
                        neg_words[token] = 1

pos_words = sorted(pos_words.items(), key=operator.itemgetter(1), reverse=True)
neg_words = sorted(neg_words.items(), key=operator.itemgetter(1), reverse=True)

with open('pos.csv', 'a') as f:
    for item in pos_words:
        f.write('{0},{1},{2}\n'.format(item[0][0], item[0][1], item[1]))

with open('neg.csv', 'a') as f:
    for item in neg_words:
        f.write('{0},{1},{2}\n'.format(item[0][0], item[0][1], item[1]))

print 'Total pos words:', len(pos_words)
for word in pos_words[:40]:
    print word

print 'Total neg words:', len(neg_words)
for word in neg_words[:40]:
    print word
#print pos_words[:30]


#print(pos_files)
