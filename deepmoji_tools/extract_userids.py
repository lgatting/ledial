import codecs
import operator
import thesis_helper as th
import nltk
import random
import bisect
from deepmoji.word_generator import TweetWordGenerator
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords, words
from time import gmtime, strftime

num_of_dialect_regions = 7 # How many dialect regions are there present (not counting "unknown")
n_to_select = 99999999 # Number of users to select (i.e. number of tweetdocs)
ignore_tweet_if_custom_more_than = 99 # Default value has been 3
label_replacements = [0, 1, 2, 3, 4, 5, 6, 7] # Replaces label with new label located at given index
min_tweettext_length = 5 # Min length of a tweetdoc in chars

promising_userids = []
tweetdocs = []

state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()

n_users_satisfied = 0

region_sets = [[] for i in range(0, num_of_dialect_regions + 1)] # + 1 for the "unknown region
n_users_satisfied_per_region = [0] * (num_of_dialect_regions + 1)
n_regions_satisfied = 0

stemming_fn = lambda x: x #SnowballStemmer("english").stem # lambda x: x
stopwords_list = [] # stopwords.words("english") #

print "Region labels used:"
print region_labels

englines = []
with codecs.open('/home/lvmsu/School/fasttext/thesis/exp2/fasttext.dataset', 'rU', 'utf-8') as stream:
    for line in stream:
        englines.append(line[11:].strip())

print "Loaded English lines"
englines.sort()
print "Sorted englines"

userids = []

print len(englines)

with codecs.open('/home/lvmsu/School/preprocessing/english_preprocessed_malformed.dataset', 'rU', 'utf-8') as stream:
    i = 0
    try:
        for line in stream:
            i += 1
            clean_line = line.strip()
            if not "\t" in clean_line:
                continue

            if i % 10000 == 0:
                print i

            text = clean_line.split("\t")[2]

            b_i = bisect.bisect_left(englines, text)
            if b_i != len(englines) and englines[b_i] == text:
                del englines[b_i]
                userids.append(clean_line)
    except Exception:
        print "An exception occurred while processing malformed data"

print "malformed data processed"
print len(englines)

with codecs.open('/media/sf_Shared_Folder/regionstuff.tsv', 'rU', 'utf-8') as stream:
    wg = TweetWordGenerator(stream)

    try:
        i = 0
        for line in stream:
            try:
                i += 1

                split_line = line.split("\t")
                userid = split_line[1]
                text = split_line[9]
                
                valid, words, info = wg.extract_valid_sentence_words(line)
                text = " ".join(words)
                if valid:
                    clean_text = text # th.remove_newlines((" ".join(map(stemming_fn, [w for w in wg.get_words(text) if not w in stopwords_list])))).strip()  # th.clean_text(text)
                    valid = valid and th.count_custom_occurrence(clean_text) <= ignore_tweet_if_custom_more_than and len(clean_text) >= min_tweettext_length
                    if valid:
                        label, location = th.get_label(line, state_codes, regions, region_labels)
                        label = label_replacements[label]
                        if label == 0 or n_users_satisfied_per_region[label] == n_to_select:
                            continue
                        b_i = bisect.bisect_left(englines, clean_text)
                        if b_i != len(englines) and englines[b_i] == clean_text:
                            del englines[b_i]
                            userids.append(str(label) + "\t" + userid + "\t" + clean_text)
                        tweetdocs.append(str(label) + "\t" + clean_text)
                        n_users_satisfied_per_region[label] += 1
                        if n_users_satisfied_per_region[label] == n_to_select:
                            n_regions_satisfied += 1

                if i % 100000 == 0:
                    print i, n_regions_satisfied, n_users_satisfied_per_region, len(englines)

                #if n_users_satisfied >= n_to_select:
                if n_regions_satisfied >= num_of_dialect_regions:
                    print "Finished acquiring tweets for users"
                    break
            except Exception, e:
                print str(e)

    except Exception, e:
        print str(e)
        

file_header = "Dataset created on " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " with count_alltweets.py with params n_to_select=" + str(n_to_select) + ", min_tweettext_length=" + str(min_tweettext_length) + ", ignore_tweet_if_custom_more_than=" + str(ignore_tweet_if_custom_more_than) + "\n"

with codecs.open("../../preprocessing/english_preprocessed.dataset", "wU", "utf-8") as file:
    file.write(file_header)
    for line in userids:
        if not line == None:
            file.write(line + "\n")
        else:
            file.write("\n")