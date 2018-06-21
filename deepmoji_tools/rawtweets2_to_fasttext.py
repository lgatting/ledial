import codecs
import thesis_helper as th
from deepmoji.word_generator import TweetWordGenerator

state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()

stopwords_list = []
stemming_fn = lambda x: x

result = []

with codecs.open('../../preprocessing/rawtweets2.tsv', 'rU', 'utf-8') as stream:
    wg = TweetWordGenerator(stream)
    for line in stream:
        split_line = line.split("\t")
        text = split_line[9]

        clean_text = th.remove_newlines((" ".join(map(stemming_fn, [w for w in wg.get_words(text) if not w in stopwords_list])))).strip()
        label, location = th.get_label(line, state_codes, regions, region_labels)

        result.append("__label__" + str(label) + " " + clean_text)

with codecs.open("../../preprocessing/rawtweets2.dataset", "wU", "utf-8") as file:
    for line in result:
        file.write(line + "\n")