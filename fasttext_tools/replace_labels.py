""" Replaces labels and saves output to output file
"""

import argparse
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="Source file")
parser.add_argument("-dst", help="Destination file")
args = parser.parse_args()

org_labels = ["2", "4", "5", "7"]
new_label = "1"

new_file = []

with codecs.open(args.src, "rU", "utf-8") as stream:
    i = 0
    for line in stream:
        i += 1

        if i == 1:
            continue

        if i % 100000 == 0:
            print i

        if line[9] in org_labels:
            line = line[:9] + new_label + line[10:]

        new_file.append(line)

header = "Dataset created by replacing labels from " + args.src
        
with codecs.open(args.dst, "wU", "utf-8") as file:
    file.write(header + "\n")
    for line in new_file:
        file.write(line)