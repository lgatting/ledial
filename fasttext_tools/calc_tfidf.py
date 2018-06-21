import operator
import codecs
import numpy as np
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Dataset file")
parser.add_argument("-topn", help="How many of the most indicative words should be displayed", default="10")
args = parser.parse_args()

ngram_low = 1
ngram_high = 1
analyzer = "word" # Word or char
top_n = int(args.topn)

filename = args.file

class_sets = [[], []]

idfs = []

with codecs.open(filename, 'rU', 'utf-8') as stream:
    i = 0
    for line in stream:
        i += 1
        if i == 1:
            continue
        label = line[9]
        tweetdoc = line[11:]
        label = 1 if label == "6" else 0

        class_sets[label].append(tweetdoc)

for i, class_set in enumerate(class_sets):
    class_sets[i] = " ".join(class_set)

tv = TfidfVectorizer(analyzer=analyzer,
        ngram_range=(ngram_low, ngram_high))
tfidf_matrix = tv.fit_transform(class_sets)
feature_names = tv.get_feature_names()

tfidfs_for_classes = []

for i, class_set in enumerate(class_sets):
    print "TFIDF scores for document", str(i)

    doc = i
    feature_index = tfidf_matrix[doc,:].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])

    tfidf_word_scores = [(feature_names[i], s) for (i, s) in tfidf_scores]

    tfidfs_for_classes.append(dict(tfidf_word_scores))

    #print "; ".join([e[0] + ": " + str(e[1]) for e in tfidf_word_scores[:top_n]])

magnitudes = {}

for tfidfs_for_class in tfidfs_for_classes:
    for key in tfidfs_for_class:
        if not key in magnitudes:
            try:
                v1 = tfidfs_for_classes[0][key]
                v2 = tfidfs_for_classes[1][key]
            except KeyError:
                continue

            if v1 > v2:
                magnitude = v1 / v2
            else:
                magnitude = - (v2 / v1)
            magnitudes[key] = magnitude

sorted_magnitudes = sorted(magnitudes.items(), key=lambda x: x[1])

print "First class"
print [e[0] for e in sorted_magnitudes[:top_n]]
print "Second class"
print [e[0] for e in sorted_magnitudes[-top_n:][::-1]]

# print "Sorted magnitudes class 1"
# print "; ".join([e[0] + ": " + str(round(e[1], 2)) for e in sorted_magnitudes[:top_n]])
# print "Sorted magnitudes class 2"
# print "; ".join([e[0] + ": " + str(round(e[1], 2)) for e in sorted_magnitudes[-top_n:][::-1]])