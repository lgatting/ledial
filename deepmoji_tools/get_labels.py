import codecs
import thesis_helper as th

state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()
label_replacements = [0, 1, 2, 0]

labels = []

with codecs.open('../../preprocessing/rawtweets2.tsv', 'rU', 'utf-8') as stream:
    for line in stream:
        label, location = th.get_label(line, state_codes, regions, region_labels)
        label = label_replacements[label]
        labels.append(label)


with codecs.open("../../preprocessing/rawtweets.labels", "wU", "utf-8") as file:
    for line in labels:
        file.write(str(line) + "\n")
