""" Merges user tweets and creates a fast text dataset
"""
import argparse
import codecs
from time import gmtime, strftime

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
parser.add_argument("-min", help="Minimum number of tweets per user", default="10")
parser.add_argument("-max", help="Maximum number of tweets per user", default="500")
args = parser.parse_args()

dataset = []

with codecs.open(args.src, "rU", "utf-8") as stream:

    current_user_tweets = None
    current_label = ""

    i = 0
    for line in stream:
        i += 1

        if i == 1:
            continue

        if i % 100000 == 0:
            print i

        line = line.strip()

        if line == "__ENDOFUSER__":
            l = len(current_user_tweets)
            if l >= int(args.min) and l <= int(args.max):
                dataset.append("__label__" + current_label + " " + " ".join(current_user_tweets))
            current_user_tweets = None
        elif current_user_tweets == None:
            current_label = line.split("\t")[1]
            current_user_tweets = []
        else:
            current_user_tweets.append(line)

header = "Dataset created on " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ""

with codecs.open(args.dst, "wU", "utf-8") as file:
    file.write(header + "\n")
    for line in dataset:
        file.write(line + "\n")
