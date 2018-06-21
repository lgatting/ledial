import operator
import codecs
import numpy as np
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Dataset file")
parser.add_argument("-label", help="For which label do we want to see the most indicative words", default="1")
parser.add_argument("-topn", help="How many of the most indicative words should be displayed", default="10")
args = parser.parse_args()

ngram_low = 1
ngram_high = 1
analyzer = "word" # Word or char
top_n = int(args.topn)

filename = args.file

class_sets = {}

idfs = []

with codecs.open(filename, 'rU', 'utf-8') as stream:
    i = 0
    for line in stream:
        i += 1
        if i == 1:
            continue
        label = line[9]
        tweetdoc = line[11:]

        if not label in class_sets:
            class_sets[label] = []

        class_sets[label].append(tweetdoc)

for label in class_sets:
    class_sets[label] = " ".join(class_sets[label])

labels = []
sets = []
for label in class_sets:
    sets.append(class_sets[label])
    labels.append(label)

tv = TfidfVectorizer(analyzer=analyzer,
        ngram_range=(ngram_low, ngram_high))
tfidf_matrix = tv.fit_transform(sets)
feature_names = tv.get_feature_names()

tfidfs_for_classes = []

for i, _ in enumerate(sets):
    print "TFIDF scores for document", str(i)

    doc = i
    feature_index = tfidf_matrix[doc,:].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])

    tfidf_word_scores = [(feature_names[i], s) for (i, s) in tfidf_scores]

    tfidfs_for_classes.append(dict(tfidf_word_scores))

ordered = sorted(tfidfs_for_classes[labels.index(args.label)].items(), key=lambda x: x[1])

print "For label:", args.label
print [x[0] for x in ordered[:top_n]]