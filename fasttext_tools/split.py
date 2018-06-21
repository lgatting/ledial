""" Splits the dataset into training and testing files
"""

import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("-src", help="File to split")
parser.add_argument("-dst", help="Name of the output file without .train/.test extension", default="")
parser.add_argument("-ts", help="Test size/size of the test partition as a fraction of the whole file ", default="0.1")
args = parser.parse_args()

if args.dst == "":
    print "No output specified, exiting"
    exit()

cmd = subprocess.Popen(["wc", args.src], stdout=subprocess.PIPE)
result = cmd.stdout.read()
line_count = int(result.strip().split(" ")[0])

test_size = int(line_count * float(args.ts))
train_size = line_count - test_size

os.system("tail -n " + str(test_size) + " \"" + args.src + "\" > \"" + args.dst + ".test\"")
os.system("head -n " + str(train_size) + " \"" + args.src + "\" > \"" + args.dst + ".train\"")
