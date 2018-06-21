""" Dynamically creates k-fold datasets on-the-go and provides them via iterator
"""

import codecs
import random
import resample

class DatasetGenerator():
    def __init__(self, dataset_path, dest_folder, kfolds=10):
        """ dataset_path - path to the dataset file
            dest_folder - path to the folder where the k-fold files will be saved
            kfolds - number of folds for cross-validation
        """

        self.dataset_path = dataset_path
        self.dest_folder = dest_folder if dest_folder.endswith("/") else (dest_folder + "/")
        self.kfolds = kfolds

        self.lines = []

        with codecs.open(self.dataset_path, "rU", "utf-8") as stream:
            for line in stream:
                self.lines.append(line)
    
    def __iter__(self):
        l = len(self.lines)
        k_fold_size = l / self.kfolds

        for i in range(self.kfolds):
            start = i * int(k_fold_size)
            end = (i + 1) * int(k_fold_size)

            train_set = self.lines[:start] + self.lines[end:]
            test_set = self.lines[start:end]

            train_fname = self.dest_folder + "fasttext.dynkfold.train"
            test_fname = self.dest_folder + "fasttext.dynkfold.test"

            with codecs.open(train_fname, "wU", "utf-8") as file:
                for line in train_set:
                    file.write(line)

            with codecs.open(test_fname, "wU", "utf-8") as file:
                for line in test_set:
                    file.write(line)

            #resample.resample(train_fname, train_fname)
            
            yield train_fname, test_fname