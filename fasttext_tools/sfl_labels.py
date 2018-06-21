import codecs
from random import randint

counts = {}
total = 0

def sfl_file(filename):
    with codecs.open(filename, 'rU', 'utf-8') as stream:
        lines = []

        for line in stream:
            l = line[:9] + str(randint(0, 1)) + line[10:]
            lines.append("".join(l))

        with codecs.open(filename, "wU", "utf-8") as file:
            for line in lines:
                file.write(line)

sfl_file("fasttext.train")
sfl_file("fasttext.validation")