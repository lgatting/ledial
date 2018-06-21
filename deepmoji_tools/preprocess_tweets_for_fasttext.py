""" Preprocessing script specifically tailored for use with fasttext.
    Next script to use after this is npz2txt.py or npz2usrtxt.py
"""

import codecs
import thesis_helper
import json
import numpy as np
import thesis_helper as th
from deepmoji.word_generator import TweetWordGenerator
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

tweets_file = "../../preprocessing/tweets.2017.2m.NvsS.tsv" #tweets.2017.3mil.tsv #regional-tweets.2016-01-01.tsv
vocab_file = "vocab.2017.top5000k.3mil.json"

stemming_fn = SnowballStemmer("english").stem # lambda x: x
stopwords_list = stopwords.words("english")
max_for_region = [0,160000,0,0,4000,36000,200000,0]
label_replacements = [0, 1, 2, 3, 1, 1, 6, 7] # Replaces label with new label located at given index
num_relevant_regions = 4
min_tweet_length = 5
region_counts = {}
labels_achieved = []

with open(vocab_file, 'r') as f:
    vocabulary = json.load(f)
state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()
sentences = []
user_sentences = {}
normalized_sentences = []
locations = []
labels = []

for k, v in region_labels.iteritems():
    region_counts[v] = 0

with codecs.open(tweets_file, 'rU', 'utf-8') as stream:
    wg = TweetWordGenerator(stream)

    i = 0

    # Load up tweet texts into sentences list
    for line in stream:
        i += 1
        if (i % 10000 == 0):
            print "Processing line number " + str(i)
            print region_counts

        valid, text, emojis = wg.data_preprocess_filtering(line, None)

        if not valid:
            text = unicode(text, "utf-8")

        # Allow only unicode-encoded sentences because that's what deepmoji code expects
        if isinstance(text, unicode):
            # Result of get_words function is an array of "clean" words and joining them by space converts them back to clean tweets
            normalized_tweet_text = (" ".join(map(stemming_fn, [w for w in wg.get_words(text) if not w in stopwords_list]))).strip()
            
            # If the normalized tweet is too short, we skip it
            if len(normalized_tweet_text) < min_tweet_length:
                continue

            label, location = th.get_label(line, state_codes, regions, region_labels)

            if label == region_labels["unknown"]:
                continue
        
            if len(labels_achieved) == num_relevant_regions:
                print "Breaking at", i
                break

            if label in labels_achieved:
                continue

            if region_counts[label] >= max_for_region[label]:
                labels_achieved.append(label)
                continue

            region_counts[label] += 1

            normalized_sentences.append(normalized_tweet_text)
            sentences.append(text)

            locations.append(location)

            labels.append(label_replacements[label])
            
            userid = line.split("\t")[1]
            if not userid in user_sentences:
                user_sentences[userid] = {"labels": [], "sentences": []}
            user_sentences[userid]["labels"].append(label)
            user_sentences[userid]["sentences"].append(normalized_tweet_text)

    print "Zipping sentences and labels for fastText ..."
    fasttext_set = th.fasttext_zip(normalized_sentences, labels)
    
    print "Saving data ..."
    np.savez_compressed("preprocessed_data.npz", sentences=sentences, normalized_sentences=normalized_sentences, locations=locations, labels=labels, region_labels=region_labels, fasttext_set=fasttext_set, user_sentences=user_sentences)

    print "Counts for regions:"
    print region_counts