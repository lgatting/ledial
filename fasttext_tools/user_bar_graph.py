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
args = parser.parse_args()

r = []
with codecs.open("datasets/tweet-counts-per-user.txt", 'rU', 'utf-8') as stream:
    for line in stream:
        s = line.strip().split(" :  ")
        nr = [int(s[0])] * int(s[1])
        r += nr

plt.hist(r,6519)
plt.show()