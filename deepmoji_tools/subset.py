""" Creates subset of the main set such that each region is represented equally and each region
    has the specified number of tweets assigned
"""

import codecs
import thesis_helper as th
import numpy as np

state_codes = th.load_state_codes()
regions, region_labels = th.load_regions_and_region_labels()

max_for_region = [0,800000,0,0,20000,180000,1000000,0]
region_counts = {}
labels_achieved = []
num_relevant_regions = 4 # Relevant: 1,4,5,6
irelevan_regions = [0,2,3,7] # [0, 7, 5, 1, 4, 2]

new_dataset = []

print region_labels


for k, v in region_labels.iteritems():
    region_counts[v] = 0

with codecs.open('/media/sf_Shared_Folder/regionstuff.tsv', 'rU', 'utf-8') as stream:
    i = 0
    for line in stream:
        try:
            i += 1

            if i % 100 == 0:
                print "Line", i, "out of approximatelly 30 mil          \r",


            if i % 100000 == 0:
                print ""
                print region_counts

            label, location = th.get_label(line, state_codes, regions, region_labels)

            if label in irelevan_regions:
                continue
            
            if len(labels_achieved) == num_relevant_regions:
                break

            if label in labels_achieved:
                continue

            if region_counts[label] >= max_for_region[label]:
                labels_achieved.append(label)
                continue

            region_counts[label] += 1

            new_dataset.append(line)
        except:
            print "Error occurred; continuing ..."

print ""
print "Writing to npz ..."

try:
    np.savez_compressed("../../preprocessing/newdataset.npz", new_dataset=new_dataset)
except:
    print "Failed writing npz"

print "Writing to file ..."

try:
    with codecs.open("../../preprocessing/newdataset.tsv", "wU", "utf-8") as file:
        for line in new_dataset:
            file.write(line)
except:
    print "Failed writing to file"
