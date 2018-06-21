""" From given dataset creates n new datasets for cross validation
"""

import codecs
import subprocess
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("-folder", help="Folder where train and test files are located and where results will be saved")
args = parser.parse_args()
folder = (args.folder + "/") if args.folder else "./"

k_fold = 7 # k in the k-fold cross validation
filenames = map(lambda x: folder + x, ["fasttext.train", "fasttext.validation"])
new_filename_prefix = folder + "fasttext" # Name of new file without a suffix (i.e. without e.g. .txt)

lines = []
datasets = []

for filename in filenames:
    with codecs.open(filename, 'rU', 'utf-8') as stream:
        for line in stream:
            if line.startswith("Dataset created on"): # Skip the header in the file, if present
                continue

            lines.append(line)

random.shuffle(lines)
    
l = len(lines)
k_fold_size = l / k_fold

for i in range(k_fold):
    start = i * int(k_fold_size)
    end = (i + 1) * int(k_fold_size)

    train_set = lines[:start] + lines[end:]
    test_set = lines[start:end]

    datasets.append(
        [
            test_set,
            train_set
        ]
    )

for i, dataset in enumerate(datasets):
    current_new_filename_root = new_filename_prefix + "." + str(i + 1)
    extensions = ["test", "train"]

    for j, data in enumerate(dataset):
        with codecs.open(current_new_filename_root + "." + extensions[j], "wU", "utf-8") as file:
            for line in data:
                file.write(line)