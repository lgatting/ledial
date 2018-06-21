import codecs
import random
import thesis_helper as th

n_to_select = 9000 # Number of tweets to select for each region

state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()
label_replacements = [0, 1, 2, 0]

c1 = 0
c2 = 0
r1 = []
r2 = []

with codecs.open('../../preprocessing/rawtweets.tsv', 'rU', 'utf-8') as stream:
    for line in stream:
        label, location = th.get_label(line, state_codes, regions, region_labels)
        label = label_replacements[label]
        
        if label == 1:
            if c1 == n_to_select:
                continue
            c1 += 1
            r1.append(line)
        else:
            if c2 == n_to_select:
                continue
            c2 += 1
            r2.append(line)
        
        if c1 == n_to_select and c2 == n_to_select:
            break

smallest_len = min(len(r1), len(r2))

r = r1[:smallest_len] + r2[:smallest_len]

random.shuffle(r)

with codecs.open("../../preprocessing/rawtweets2.tsv", "wU", "utf-8") as file:
    for line in r:
        file.write(line)