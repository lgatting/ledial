import operator
import codecs
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Dataset file")
parser.add_argument("-label", help="For which label do we want to see the most indicative words", default="1")
parser.add_argument("-topn", help="How many of the most indicative words should be displayed", default="10")
args = parser.parse_args()

ngram_low = 1
ngram_high = 1
analyzer = "word" # word or char

filename = args.file

class_sets = {}

idfs = {}

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
    print "TFIDFing class set"

    class_set = class_sets[label]

    tv = TfidfVectorizer(analyzer=analyzer,
            ngram_range=(ngram_low, ngram_high),
            binary=False)
    x = tv.fit_transform(class_set)
    idf = tv.idf_
    as_dict = dict(zip(tv.get_feature_names(), idf))
    #ordered = sorted(as_dict.items(), key=operator.itemgetter(1))

    idfs[label] = as_dict

ordered = sorted(idfs[args.label].items(), key=operator.itemgetter(1))

print "For label:", args.label
print [x[0] for x in ordered[-int(args.topn):]]