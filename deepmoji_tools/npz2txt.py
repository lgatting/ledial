""" Converts data from npz file into a text file.
    Next script to for use with this output: preprocess_tweets_for_fasttext.py
"""

import numpy as np
import random

def fasttextset_to_txt():
    """ Saves fastText set from preprocessed data as a two text files - training and validation file.
    """

    def write_set_to_file(filename, data):
        with open(filename, "w") as f:
            for line in data:
                f.write(line)
                f.write("\n")

    d = np.load("preprocessed_data.npz")
    fasttext_set = d["fasttext_set"]

    random.shuffle(fasttext_set)

    # Percentage on which to split the dataset
    train_test_split = 0.9
    breakpoint = int(len(fasttext_set) * train_test_split)

    train_set = fasttext_set[:breakpoint]
    validation_set = fasttext_set[breakpoint:]

    write_set_to_file("fasttext.train", train_set)
    write_set_to_file("fasttext.validation", validation_set)

if __name__ == "__main__":
    fasttextset_to_txt()