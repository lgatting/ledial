""" Upsamples or downsamples given dataset
"""

import random
import codecs
import numpy as np

def resample(source, destination, resampling_fn=lambda x: int(min(x)), cutoff_less=False):
    """ If cutoff_less is True, then any class that has less than the desired amount of samples will be removed,
        otherwise that class will be upsampled
    """

    dataset = source # "exp1/fasttext.dataset"
    output = destination # "exp1/fasttext.resampled.dataset"
    length_limit_fn = resampling_fn # x is length of each class; use min for downsampling, max for upsampling

    data = {}
    newdata = {}

    # print "Loading data"

    # Load data
    with codecs.open(dataset, "rU", "utf-8") as stream:
        for line in stream:
            label = line[9]

            # Skip header line
            if label == "r":
                continue

            if not label in data:
                data[label] = []
            
            data[label].append(line)

    #print "Determining limit"

    # Find how many items should each class have
    length_limit = length_limit_fn([len(data[item]) for item in data])

    #print "Resampling"

    # Resample each class such that each class has the length_limit number of items
    for item in data:
        #print "Resampling class", item

        if cutoff_less and len(data[item]) < length_limit:
            continue

        random.shuffle(data[item])

        newdata[item] = []
        l = len(data[item])

        if length_limit > l:
            for i in range(length_limit - l):
                newdata[item].append(random.choice(data[item]))
        else:
            data[item] = data[item][:length_limit]

    #print "Merging data"

    # Merge the two lists, one containing original data, other containing the newly sampled data and mix them
    for item in newdata:
        newdata[item] = data[item] + newdata[item]

    #print "Flattening data"

    # Flatten the result
    final_list = [item for k in newdata for item in newdata[k]]

    random.shuffle(final_list)

    #print "Saving to", output

    with codecs.open(output, "wU", "utf-8") as file:
        for line in final_list:
            file.write(line)

