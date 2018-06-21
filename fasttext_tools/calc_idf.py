import operator
import codecs
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Dataset file")
parser.add_argument("-topn", help="How many of the most indicative words should be displayed", default="10")
args = parser.parse_args()

ngram_low = 1
ngram_high = 1
analyzer = "word" # word or char
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

for class_set in class_sets:
    print "TFIDFing class set"
    tv = TfidfVectorizer(analyzer=analyzer,
            ngram_range=(ngram_low, ngram_high),
            binary=False)
    x = tv.fit_transform(class_set)
    idf = tv.idf_
    as_dict = dict(zip(tv.get_feature_names(), idf))
    #ordered = sorted(as_dict.items(), key=operator.itemgetter(1))

    idfs.append(as_dict)

print "Calculating difference"
diff = {}
for key in idfs[0]:
    if key in idfs[1]:
        diff[key] = idfs[1][key] - idfs[0][key]

ordered = sorted(diff.items(), key=operator.itemgetter(1))

print "First class"
print [e[0] for e in ordered[:top_n]]
print "Second class"
print [e[0] for e in ordered[-top_n:][::-1]]

# print "Resultset 1:"
# print "; ".join([e[0] + ": " + str(round(e[1], 2)) for e in ordered[:top_n]])
# print "Resultset 2:"
# print "; ".join([e[0] + ": " + str(round(e[1], 2)) for e in ordered[-top_n:][::-1]])