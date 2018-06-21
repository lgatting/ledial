""" Converts data from npz file into a text file suitable for fasttext where each
    line is a set of all tweets found for any given user
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

    print "Opening .npz file ..."
    d = np.load("preprocessed_data.npz")
    user_sentences = d["user_sentences"].item() # .item() because of how numpy saves dict in its npz file

    sentences = []

    print "Preparing sentences ..."
    for k in user_sentences:
        label = max(set(user_sentences[k]["labels"]), key=user_sentences[k]["labels"].count)
        if label != 0:
            sentences.append("__label__" + str(label) + " " + ". ".join(user_sentences[k]["sentences"]))

    print "Slicing and saving ..."
    # Percentage on which to split the dataset
    train_test_split = 0.9
    breakpoint = int(len(sentences) * train_test_split)

    train_set = sentences[:breakpoint]
    validation_set = sentences[breakpoint:]

    write_set_to_file("fasttext.train", train_set)
    write_set_to_file("fasttext.validation", validation_set)

if __name__ == "__main__":
    fasttextset_to_txt()