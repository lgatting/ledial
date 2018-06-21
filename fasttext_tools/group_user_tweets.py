""" Merges all tweets for all users. The output, however, is still raw and not fastText ready
"""

import argparse
import codecs
from time import gmtime, strftime

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
args = parser.parse_args()

usertweets = {}

with codecs.open(args.src, "rU", "utf-8") as stream:
    i = 0
    for line in stream:
        i += 1

        if i == 1:
            continue

        if i % 100000 == 0:
            print i
        
        split_line = line.strip().split("\t")

        label = split_line[0]
        userid = split_line[1]
        text = split_line[2]

        if not userid in usertweets:
            usertweets[userid] = {"labels": [], "tweets": []}
        
        usertweets[userid]["labels"].append(label)
        usertweets[userid]["tweets"].append(text)

header = "Dataset created on " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ""

counts = {}

with codecs.open(args.dst, "wU", "utf-8") as file:
    file.write(header + "\n")
    for userid in usertweets:
        most_popular_label = max(set(usertweets[userid]["labels"]), key=usertweets[userid]["labels"].count)
        tweet_count = str(len(usertweets[userid]["tweets"]))
        if not tweet_count in counts:
            counts[tweet_count] = 0

        counts[tweet_count] += 1

        file.write(userid + "\t" + most_popular_label + "\n")
        for text in usertweets[userid]["tweets"]:
            file.write(text + "\n")
        file.write("__ENDOFUSER__\n")

print "Tweet counts:"

keylist = map(int, counts.keys())
keylist.sort()

for count in keylist:
    print count, ": ", counts[str(count)]