import codecs
import operator
import thesis_helper as th
import nltk
import random
from deepmoji.word_generator import TweetWordGenerator
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from time import gmtime, strftime

num_of_dialect_regions = 2 # 7 # How many dialect regions are there present
n_to_select = 250000 # Number of users to select (i.e. number of tweetdocs)
ignore_tweet_if_custom_more_than = 3 # Default value has been 3
label_replacements = [0, 1, 2, 0] #, 4, 5, 6, 7] # Replaces label with new label located at given index
min_tweettext_length = 15 # Min length of a tweetdoc in chars

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
                
                valid, text, emojis = wg.data_preprocess_filtering(line, None)
                if valid:
                    clean_text = th.remove_newlines((" ".join(map(stemming_fn, [w for w in wg.get_words(text) if not w in stopwords_list])))).strip()  # th.clean_text(text)
                    valid = valid and th.count_custom_occurrence(clean_text) < ignore_tweet_if_custom_more_than and len(clean_text) >= min_tweettext_length
                    if valid:
                        label, location = th.get_label(line, state_codes, regions, region_labels)
                        label = label_replacements[label]
                        if label == 0 or n_users_satisfied_per_region[label] == n_to_select:
                            continue
                        tweetdocs.append(line)
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

    except Exception, e:
        print str(e)
        
print "Writing the set ..."
with codecs.open("../../preprocessing/rawtweets.tsv", "wU", "utf-8") as file:
    for line in tweetdocs:
        file.write(line)
