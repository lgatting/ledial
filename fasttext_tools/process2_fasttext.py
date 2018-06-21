""" Takes a fastText-ready dataset, removes stopwords, stems the words and saves the output in a given file
"""

import argparse
import codecs
from nltk.stem import SnowballStemmer, PorterStemmer, LancasterStemmer
from nltk.corpus import stopwords

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
args = parser.parse_args()

stemmer = SnowballStemmer("english")

new_dataset = []

with codecs.open(args.src, "rU", "utf-8") as stream:
    i = 0
    for line in stream:
        i += 1

        if i % 1000 == 0:
            print i

        text = line[11:].strip()
        words = text.split(" ")

        stemmed_text = " ".join([stemmer.stem(w) for w in words if not w in stopwords.words("english")])

        new_line = line[:11] + stemmed_text

        new_dataset.append(new_line)


with codecs.open(args.dst, "wU", "utf-8") as file:
    for line in new_dataset:
        file.write(line + "\n")
