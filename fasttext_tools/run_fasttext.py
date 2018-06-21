import subprocess
import os.path
import codecs
import argparse
from time import gmtime, strftime

parser = argparse.ArgumentParser()
parser.add_argument("-folder", help="Folder where train and test files are located and where results will be saved", default="./")
parser.add_argument("-epoch", help="Number of iterations/epochs", default="10")
parser.add_argument("-wordNgrams", help="N for n-grams", default="1")
parser.add_argument("-lr", help="Learning rate", default="0.125")
parser.add_argument("-dim", help="Dimension of vector", default="100")
parser.add_argument("-ws", help="Size of the window", default="5")
parser.add_argument("-minn", help="Min length of character n-gram", default="0")
parser.add_argument("-maxn", help="Max length of character n-gram", default="0")
parser.add_argument("-minCount", help="Minimal number of word occurences", default="1")
args = parser.parse_args()
folder = (args.folder + "/") if args.folder else "./"

command = "../fastText-0.1.0/fasttext"

k_dataset_prefix = folder + "fasttext"
model_location = folder + "dialect_model"
epoch = args.epoch
wordNgrams = args.wordNgrams
lr = args.lr
dim = args.dim
ws = args.ws
minn = args.minn
maxn = args.maxn
minCount = args.minCount

train_cmd_generator = lambda train_file: [command, "supervised", "-input", train_file, "-output", model_location, "-epoch", str(epoch), "-wordNgrams", str(wordNgrams), "-lr", str(lr), "-dim", str(dim), "-ws", str(ws), "-minn", str(minn), "-maxn", str(maxn), "-minCount", str(minCount)]

precisions = []

i = 0
while True:
    i += 1

    test_file = k_dataset_prefix + "." + str(i) + ".test"
    train_file = k_dataset_prefix + "." + str(i) + ".train"

    if os.path.isfile(test_file) and os.path.isfile(train_file):
        print "Shuffling training set"
        subprocess.call(["shuf", train_file, "-o", train_file])
        print "Training set", train_file
        subprocess.call(train_cmd_generator(train_file))
        print "Testing set", test_file
        cmd = subprocess.Popen([command, "test", model_location + ".bin", test_file, "1"], stdout=subprocess.PIPE)
        result = cmd.stdout.read()
        precision = result.split("\n")[1].split("\t")[1] # Precision is located at line 1, column 1

        print "\tPrecision:", precision

        precisions.append(float(precision))
    else:
        break

avg_precision = round((sum(precisions)*1.0 / len(precisions)*1.0), 3)

print ""
print "Overall result:", avg_precision

currtime = strftime("%Y-%m-%d_%H%M%S", gmtime())
with codecs.open(folder + "results_" + currtime + ".txt", "wU", "utf-8") as file:
    file.write("Results saved " + currtime + "\n")
    file.write("\n")
    file.write("Folder: " + folder + "\n")
    file.write("k-fold cross validation with k=" + str(i - 1) + "\n")
    file.write("Training command: " + " ".join(train_cmd_generator("<PREFIX " + k_dataset_prefix + ">")) + "\n")
    file.write("Precisions: " + " ".join(map(str, precisions)) + "\n")
    file.write("Overall average precision: " + str(avg_precision) + "\n")