""" (to_json_vocab.py) -> logreg_learner2.py
"""

import json
import codecs
import random
import heapq
import thesis_helper as th
from sklearn import linear_model
from deepmoji.word_generator import TweetWordGenerator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Dataset file")
args = parser.parse_args()

# Settings
vocab_file = "vocab.json"
use_randomlogreg = True
test_size = 0.1
# EO Settings

with open(vocab_file, "r") as f:
    vocabulary = json.load(f)

vocab_len = len(vocabulary)

samples = []
labels = []

with codecs.open(args.file, 'rU', 'utf-8') as stream:
    wg = TweetWordGenerator(stream)
    i = 0
    for line in stream:
        try:
            i += 1

            if i % 10000 == 0:
                print i

            label = int(line[9])
            text = line[11:]
            tokens = [0] * vocab_len

            for w in wg.get_words(text):
                try:
                    tokens[vocabulary[w]] += 1
                except KeyError:
                    pass
            samples.append(tokens)
            labels.append(label)
        except ValueError:
            pass
        
print "Finished loading samples"

l1 = int(len(samples) * test_size)

# train_samples = samples[:l1]
# train_labels = labels[:l1]
# test_samples = samples[-l1:]
# test_labels = labels[-l1:]

print len(labels), len(samples), len(samples[0])

if use_randomlogreg:
    print "Running ranlogreg"
    logreg = linear_model.RandomizedLogisticRegression(n_resampling=200, selection_threshold=0.25)
    print "Fitting"
    logreg.fit(samples, labels)

    samples = None
    labels = None

    print "Swapping vocab"
    indices = logreg.get_support(indices=True)
    swapped_vocab = dict((v, k) for k, v in vocabulary.iteritems())

    print ", ".join([swapped_vocab[i] for i in indices])
    exit()
else:
    logreg = linear_model.LogisticRegression()
    logreg.fit(train_samples, train_labels)

print "Done"

predictions = logreg.predict(test_samples)

print heapq.nlargest(3, enumerate(logreg.coef_[0]), key=lambda x: x[1])

success = 0.0
total = 0.0
random_predictions = 0.0
for i, prediction in enumerate(predictions):
    random_predictions += prediction == random.randint(1, 2)
    success += prediction == test_labels[i]
    total += 1

print success/total, random_predictions/total