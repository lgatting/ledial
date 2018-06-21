""" Creates vocaulary in JSON format from the raw .npz vocab file that contains list of key-value pairs
    of words and their counts.
"""

from deepmoji.create_vocab import MasterVocab

mv = MasterVocab()
mv.populate_master_vocab("./", 1)
mv.save_vocab("count.txt", "vocab.json", 1000)