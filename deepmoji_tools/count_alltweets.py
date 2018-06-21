import codecs
import operator
import thesis_helper as th
import nltk
import random
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
        englines.append(line[11:])

print "Loaded English lines"

curengpointer = 0
userids = []

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
                        if clean_text == englines[curengpointer]:
                            userids.append(userid)
                            curengpointer += 1
                        tweetdocs.append(str(label) + "\t" + clean_text)
                        n_users_satisfied_per_region[label] += 1
                        if n_users_satisfied_per_region[label] == n_to_select:
                            n_regions_satisfied += 1

                if i % 100000 == 0:
                    print i, n_regions_satisfied, n_users_satisfied_per_region

                #if n_users_satisfied >= n_to_select:
                if n_regions_satisfied >= num_of_dialect_regions:
                    print "Finished acquiring tweets for users"
                    break
            except Exception, e:
                print str(e)
        
        print "Transforming tweets into fastText dataset"
        for tweetdoc in tweetdocs:
            split_tweet = tweetdoc.split("\t")
            label = int(split_tweet[0])
            clean_text = split_tweet[1]
            final_label = label_replacements[label]

            region_sets[final_label].append("__label__" + str(final_label) + " " + clean_text)

    except Exception, e:
        print str(e)
        
min_lens = []
for region_set in region_sets:
    llen = len(region_set)
    if llen != 0:
        min_lens.append(llen)
min_len = min(min_lens)
print min_len
fasttext_set = []

for region_set in region_sets:
    fasttext_set += region_set # [:min_len] # Uncomment this if you want to downsample

random.shuffle(fasttext_set)

l = len(fasttext_set)
limit = int(l*.9)
train = fasttext_set[:limit]
validation = fasttext_set[limit:]

file_header = "Dataset created on " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " with count_alltweets.py with params n_to_select=" + str(n_to_select) + ", min_tweettext_length=" + str(min_tweettext_length) + ", ignore_tweet_if_custom_more_than=" + str(ignore_tweet_if_custom_more_than) + "\n"


with codecs.open("../../preprocessing/fasttext.dataset", "wU", "utf-8") as file:
    file.write(file_header)
    for line in fasttext_set:
        file.write(line + "\n")

# print "Writing training set ..."
# with codecs.open("../../preprocessing/fasttext.train", "wU", "utf-8") as file:
#     file.write(file_header)
#     for line in train:
#         file.write(line + "\n")

# print "Writing validation set ..."
# with codecs.open("../../preprocessing/fasttext.validation", "wU", "utf-8") as file:
#     file.write(file_header)
#     for line in validation:
#         file.write(line + "\n")
