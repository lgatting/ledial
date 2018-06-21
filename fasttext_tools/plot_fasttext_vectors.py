""" Plots fastText sentence vectors for the test data.
"""

import subprocess
import os.path
import codecs
import argparse
import re
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
from sklearn.decomposition import PCA

parser = argparse.ArgumentParser()
parser.add_argument("-dataset", help="Testing file")
parser.add_argument("-model", help=".bin model file location")
args = parser.parse_args()

data = args.dataset
model = args.model

command = "../fastText-0.1.0/fasttext"

x = []
y = []
datapoint_colors = []
colors = {"1": "green", "2": "yellow", "3": "red", "4": "purple", "5": "brown", "6": "blue", "7": "black"}

sents = []
vecs = []

max_sents_per_cmd = 500

with codecs.open(data, 'rU', 'utf-8') as stream:
    print "Collecting sentences"
    for line in stream:
        try:
            label = line[9]
            sent = line[11:]
        
            sents.append(sent)
            datapoint_colors.append(colors[label])
        except Exception, e:
            print e
            pass

    print "Formatting sentences"

    results = []
    for i in range(len(sents) / max_sents_per_cmd + 1):
        input_str = "\""
        for sent in sents[(i * max_sents_per_cmd):min((i+1) * max_sents_per_cmd, len(sents))]:
            input_str += re.escape(sent) + "\n"
        input_str = input_str[:-1] + "\""

        print "Calculating vectors for sentences"

        cmd = "echo {} | {} print-sentence-vectors {}".format(input_str, command, model)
        cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        results = results + cmd.stdout.read().split("\n")[:-1]

    print "Converting string vectors to number vectors"

    for result in results:
        vec = map(float, result.strip().split(" "))
        vecs.append(vec)

    print "Performing PCA"
    
    pca = PCA(n_components=2)
    vecs_2d = pca.fit_transform(vecs)
    for el in vecs_2d:
        x.append(el[0])
        y.append(el[1])

plt.scatter(x, y, color=datapoint_colors)
plt.show()