""" Takes all tweets and converts them to feature vectors based on the vocabulary.
"""

import codecs
import thesis_helper
import json
import numpy as np
import argparse
from nltk.corpus import stopwords
from deepmoji.create_vocab import VocabBuilder
from deepmoji.word_generator import TweetWordGenerator
from deepmoji.sentence_tokenizer import SentenceTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("-rmsw", action="store_true", help="Remove stopwords from sentences")
parser.add_argument("-rpd", action="store_true", help="Store raw preprocessing output data in a file")
parser.add_argument("-urpd", action="store_true", help="Use raw preprocessing output data from default file")
args = parser.parse_args()

raw_preprocessing_data_filename = "raw_preprocessed_data.npz"

def remove_stopwords_from_tokens(vocabulary, tokens):
    """ Takes vocabulary and list of int-token sentences and removes all stopwords.

        Params:
            vocabulary - Object of <str: int> pairs.
            tokens - Numpy array of int-lists.
    """
    stopword_indices = [vocabulary[word] for word in stopwords.words("english") if word in vocabulary]

    for i, sentence in enumerate(tokens):
        for j, token in enumerate(sentence):
            if token in stopword_indices:
                sentence = np.delete(sentence, j)
                sentence = np.append(sentence, 0)
        tokens[i] = sentence

    return tokens

def normalize_sententes(st, sentences_tokens):
    """ Takes list of sentences represented as list of ints that match current vocabulary
        and converts them back to actual strings.

        Params:
            st - Sentence tokenizer.
            sentences_tokens - list of sentence tokens where a token is an in refering to an
                actual word in vocabulary.
    """
    r = []

    for sentence_tokens in sentences_tokens:
        r.append(st.to_sentence(sentence_tokens))

    return r

def fasttext_zip(sentences, labels):
    """ Merges sentences and labels so that the output can be used by fastText. Both parameters
        must be lists and must have same length.

        Params:
            sentences - List of strings, i.e. sentences
            labels - List of labels.
    """
    tuples = zip(sentences, labels)

    r = []
    for sentence, label in tuples:
        line = "__label__" + str(label) + " " + (sentence if isinstance(sentence, unicode) else str(" ".join(map(str, sentence))))
        r.append(line)
    return r

def load_state_codes():
    """ Loads state names, codes and FIPS into a variable and returns it. Rturns a list of list
        with three items in format of [<STATE FULL NAME>, <2-LETTER ABBREVIATION>, <FIPS CODE>].
    """

    state_codes = []

    with codecs.open('cont-states.tsv', 'rU', 'utf-8') as stream:
        iterstream = iter(stream)

        # Skip first line which is just a header
        next(iterstream)
        for line in iterstream:
            state_codes.append(line.split("\t"))
    
    return state_codes

def load_regions_and_region_labels():
    """ Loads regions and a map of <REGION NAME>: <UNIQUE_INT> where unique int is and integer that gets incremented each time.
    """
    with open('../../county2region/output_t0.95.json', 'r') as f:
        regions = json.load(f)

    region_labels = {"unknown": 0}
    c = 1
    for region in regions:
        region_labels[region] = c
        c += 1
    
    return regions, region_labels
    

state_codes = load_state_codes()
regions, region_labels = load_regions_and_region_labels()

with open('vocab.2017.3mil.json', 'r') as f:
    vocabulary = json.load(f)

sentences = []
locations = []
labels = []

st = SentenceTokenizer(vocabulary, 30)

if not args.urpd:
    print "Generating raw preprocessed data."

    with codecs.open('../../preprocessing/tweets.2017.3mil.tsv', 'rU', 'utf-8') as stream:
        wg = TweetWordGenerator(stream)

        i = 0

        # Load up tweet texts into sentences list
        for line in stream:
            i += 1
            if (i % 100000 == 0):
                print "Processing line number " + str(i)
                
            valid, text, emojis = wg.data_preprocess_filtering(line, None)

            # Allow only unicode-encoded sentences because that's what deepmoji code expects
            if (isinstance(text, unicode)):
                sentences.append(text)

                location = thesis_helper.normalize_location_str(line, state_codes)
                locations.append(location)
                
                region_found = False
                for region in regions:
                    if location in regions[region]:
                        region_found = True
                        labels.append(region_labels[region])
                        break
                
                if not region_found:
                    labels.append(region_labels["unknown"])

        tokens, infos, stats = st.tokenize_sentences(sentences)

        print(stats)

        # Remove stopwords
        if args.rmsw:
            print "Removing stopwords."
            remove_stopwords_from_tokens(vocabulary, tokens)

        raw_sentences = sentences

        # Store tokens, locations and labels in a raw preprocessing file
        if args.rpd:
            np.savez_compressed(raw_preprocessing_data_filename, raw_sentences=raw_sentences, tokens=tokens, locations=locations, labels=labels, region_labels=region_labels, args=args)
else:
    print "Using stored raw preprocessed data."

    data = np.load(raw_preprocessing_data_filename)

    raw_sentences = data["raw_sentences"]
    tokens = data["tokens"]
    locations = data["locations"]
    labels = data["labels"]
    region_labels = data["region_labels"]
    org_args = data["args"]

    # if args.rmsw != org_args.rmsw:
    #     print "Remove stopwords argument was/wasn't passed in the original raw data preprocessing process, but isn't/is present in this script execution."
    #     print "Exiting"
    #     exit()

print "Normalizing sentences."
normalized_sentences = normalize_sententes(st, tokens)
print "Zipping sentences and labels for fastText."
fasttext_set = fasttext_zip(normalized_sentences, labels)

np.savez_compressed("preprocessed_data.npz", sentences=sentences, tokens=tokens, locations=locations, labels=labels, region_labels=region_labels, args=args, fasttext_set=fasttext_set)