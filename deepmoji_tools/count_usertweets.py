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
n_to_select = 10000 # Number of users to select (i.e. number of tweetdocs)
n_tweets_min = 3 # How many tweets each user should have assigned
n_tweets_max = 20
ignore_tweet_if_custom_more_than = 3 # Default value has been 3
label_replacements = [0, 1, 2, 0] #, 4, 5, 6, 7] # Replaces label with new label located at given index
min_tweettext_length = 1 # Min length of a tweetdoc in chars

promising_userids = []
user_tweets = {}
usertweets = {}

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
        selected_users = False
        i = 0
        for line in stream:
            try:
                i += 1

                split_line = line.split("\t")
                userid = split_line[1]
                text = split_line[9]

                if i < 1000000:
                    label, location = th.get_label(line, state_codes, regions, region_labels)
                    label = label_replacements[label]

                    if label == 0:
                        continue

                    if not userid in usertweets:
                        usertweets[userid] = 0
                    
                    usertweets[userid] += 1

                    if i % 100000 == 0:
                        print i, len([u for u in usertweets if usertweets[u] > n_tweets_min]), len(usertweets)
                else:
                    if not selected_users:
                        print "Finished selecting promising users ..."
                        selected_users = True
                        promising_userids = dict(sorted(usertweets.iteritems(), key=operator.itemgetter(1), reverse=True)[:n_to_select*10000]) # [:(n_to_select*2)]
                        for promising_userid in promising_userids:
                            user_tweets[promising_userid] = []
                    
                    if userid in user_tweets:
                        curr_len = len(user_tweets[userid])
                        if curr_len < n_tweets_max:
                            valid, text, emojis = wg.data_preprocess_filtering(line, None)
                            if valid:
                                clean_text = th.remove_newlines((" ".join(map(stemming_fn, [w for w in wg.get_words(text) if not w in stopwords_list])))).strip()  # th.clean_text(text)
                                valid = valid and th.count_custom_occurrence(clean_text) < ignore_tweet_if_custom_more_than and len(clean_text) >= min_tweettext_length
                                if valid:
                                    label, location = th.get_label(line, state_codes, regions, region_labels)
                                    label = label_replacements[label]
                                    if label == 0 or n_users_satisfied_per_region[label] == n_to_select:
                                        continue
                                    user_tweets[userid].append(str(label) + "\t" + clean_text)
                                    if curr_len + 1 == n_tweets_min:
                                        n_users_satisfied += 1
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
        for user in user_tweets:
            if len(user_tweets[user]) >= n_tweets_min:
                labels = []
                tweet_doc = "" # All user's tweets merged into one "document"
                for tweet in user_tweets[user]:
                    split_tweet = tweet.split("\t")
                    label = int(split_tweet[0])
                    clean_text = split_tweet[1]

                    labels.append(label)
                    tweet_doc += " " + clean_text#" ".join(map(stemming_fn, ntlk.word_tokenize(clean_text)))
                majority_label = max(set(labels), key=labels.count)
                final_label = label_replacements[majority_label]

                region_sets[final_label].append("__label__" + str(final_label) + " " + tweet_doc)

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
    fasttext_set += region_set[:min_len]

random.shuffle(fasttext_set)

l = len(fasttext_set)
limit = int(l*.9)
train = fasttext_set[:limit]
validation = fasttext_set[limit:]

file_header = "Dataset created on " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " with params n_to_select=" + str(n_to_select) + ", n_tweets_min=" + str(n_tweets_min) + ", n_tweets_max=" + str(n_tweets_max) + ", min_tweettext_length=" + str(min_tweettext_length) + ", ignore_tweet_if_custom_more_than=" + str(ignore_tweet_if_custom_more_than) + ", label_replacements=" + str(label_replacements) + ", region_labels=" + str(region_labels) + "\n"

print "Writing training set ..."
with codecs.open("../../preprocessing/fasttext.train", "wU", "utf-8") as file:
    file.write(file_header)
    for line in train:
        file.write(line + "\n")

print "Writing validation set ..."
with codecs.open("../../preprocessing/fasttext.validation", "wU", "utf-8") as file:
    file.write(file_header)
    for line in validation:
        file.write(line + "\n")
