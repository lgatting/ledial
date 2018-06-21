""" Replaces words that are not location indicative
"""

import argparse
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
parser.add_argument("-salientwords", help="File containing the salient words")
args = parser.parse_args()

new_dataset = []

salient_words = []

with codecs.open(args.salientwords, "rU", "utf-8") as stream:
    for line in stream:
        word = line.strip()
        salient_words.append(word)

salient_words = set(salient_words)

with codecs.open(args.src, "rU", "utf-8") as stream:
    i = 0
    for line in stream:
        i += 1

        if i == 1:
            continue

        if i % 1000 == 0:
            print i

        label_text = line[:11]
        text = line[11:]

        words = text.split(" ")
        new_words = []
        
        for word in words:
            word = word.strip()

            if len(word) < 1:
                continue
            
            if not word in salient_words:
                continue
            
            new_words.append(word)

        new_text = " ".join(new_words)

        if len(new_text) < 1:
            continue
        
        new_dataset.append(label_text + new_text)

header = "Dataset created from " + args.src
        
with codecs.open(args.dst, "wU", "utf-8") as file:
    file.write(header + "\n")
    for line in new_dataset:
        file.write(line + "\n")