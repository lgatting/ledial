import codecs
import thesis_helper
import json
from deepmoji.create_vocab import VocabBuilder
from deepmoji.word_generator import TweetWordGenerator, FasttextWordGenerator

with codecs.open('../../fasttext/thesis/datasets/english-user-tweets.dataset', 'rU', 'utf-8') as stream:
    wg = FasttextWordGenerator(stream, use_stemmer=False)
    vb = VocabBuilder(wg)
    vb.count_all_words()
    vb.save_vocab()
