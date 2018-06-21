import codecs
import argparse


default_file = "exp1/fasttext.meansampled.dataset"
counts = {}
total = 0

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="File with fastText set")
args = parser.parse_args()

filename = args.file if not args.file is None else default_file

with codecs.open(filename, 'rU', 'utf-8') as stream:
    for line in stream:
        l = line[9]

        if l in counts:
            counts[l] += 1
        else:
            counts[l] = 1
        
        total += 1

for key in counts:
    print key + ": " + str(1.0*counts[key]/total*100) + "% (" + str(counts[key]) +")"