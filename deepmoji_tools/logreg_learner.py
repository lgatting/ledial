""" (to_json_vocab.py) -> select_balanced_rawtweets.py -> get_labels.py -> logreg_learner.py
"""

import json
import codecs
import random
import heapq
import thesis_helper as th
from sklearn import linear_model
from deepmoji.word_generator import TweetWordGenerator

# Settings
vocab_file = "vocab.json"
use_randomlogreg = True
# EO Settings

with open(vocab_file, "r") as f:
    vocabulary = json.load(f)

vocab_len = len(vocabulary)

samples = []
labels = []

with codecs.open('../../preprocessing/rawtweets.labels', 'rU', 'utf-8') as stream:
    for line in stream:
        if len(line) >= 1:
            labels.append(int(line.strip()))

with codecs.open('../../preprocessing/rawtweets2.tsv', 'rU', 'utf-8') as stream:
    wg = TweetWordGenerator(stream)
    for s_words, s_info in wg:
        tokens = [0] * vocab_len

        for w in s_words:
            try:
                tokens[vocabulary[w]] += 1
            except KeyError:
                pass
        
        samples.append(tokens)

train_samples = samples[:len(samples) - 1000]
train_labels = labels[:len(labels) - 1000]
test_samples = samples[-1000:]
test_labels = labels[-1000:]

print len(labels), len(samples), len(samples[0])

if use_randomlogreg:
    logreg = linear_model.RandomizedLogisticRegression(n_resampling=150)
    logreg.fit(train_samples, train_labels)

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