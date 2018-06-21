""" Module import helper.
Modifies PATH in order to allow us to import the deepmoji directory.
"""
import sys
import re
import codecs
import json
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

def normalize_location_str(rawline, state_codes):
    '''Normalizes location strings. Little Bjarke wrote this.
    
    '''

    # remove unicode
    if isinstance(rawline, str):
        line = rawline.decode('utf-8')
    elif isinstance(rawline, unicode):
        line = rawline
    else:
        raise TypeError("Line neither string nor unicode")
    entries = line.split("\t")
    if len(entries) != 12:
        return None
    
    loc = entries[8]
    loc = loc.encode('unicode-escape')
    loc = loc.decode('unicode_escape').encode('ascii','ignore')    

    # remove non-alphanumeric
    loc = loc.lower()
    loc = re.sub('[^0-9a-zA-Z]+', ' ', loc)

    # remove US from right side
    loc = ' '.join(loc.split())
    us_names = [' us', ' usa', ' united states', ' united states of america']
    for pattern in us_names:
        loc = re.sub('%s$' % pattern, '', loc)

    # abbreviate state names
    for s in state_codes:
        loc = loc.replace(s[0].lower(), ' '+s[1])

    # cleaning whitespace uses
    loc = ' '.join(loc.split())
    loc = loc.strip()
    loc = loc.lower()

    if loc == '':
        return None
    return loc

def fasttext_zip(sentences, labels):
    """ Merges sentences and labels so that the output can be used by fastText. Both parameters
        must be lists and must have same length.

        Params:
            sentences - List of strings, i.e. sentences
            labels - List of labels.
    """
    tuples = zip(sentences, labels)

    r = []
    for sentence, label in tuples:
        line = "__label__" + str(label) + " " + (sentence if isinstance(sentence, unicode) else str(" ".join(map(str, sentence))))
        r.append(line)
    return r

def load_state_codes():
    """ Loads state names, codes and FIPS into a variable and returns it. Rturns a list of list
        with three items in format of [<STATE FULL NAME>, <2-LETTER ABBREVIATION>, <FIPS CODE>].
    """

    state_codes = []

    with codecs.open('cont-states.tsv', 'rU', 'utf-8') as stream:
        iterstream = iter(stream)

        # Skip first line which is just a header
        next(iterstream)
        for line in iterstream:
            state_codes.append(line.split("\t"))
    
    return state_codes

def load_regions_and_region_labels():
    """ Loads regions and a map of <REGION NAME>: <UNIQUE_INT> where unique int is and integer that gets incremented each time.
    """

    county_mapping_file = "../../county2region/county2region_t0.95.json" # "../../county2region/county2region_t0.95.json"

    with open(county_mapping_file, 'r') as f:
        regions = json.load(f)

    region_labels = {"unknown": 0}
    c = 1
    for region in regions:
        region_labels[region] = c
        c += 1
    
    return regions, region_labels

def get_label(line, state_codes, regions, region_labels):
    """ Takes a line from the tweet file and returns a region label for it.

        Params:
            line - A line from twitter dateset.
            state_codes - Result of load_state_codes function.
            regions - first item returned from load_regions_and_region_labels function,
            region_labels - second item returned from load_regions_and_region_labels function,
    """
    location = normalize_location_str(line, state_codes)
    
    label = None

    region_found = False
    for region in regions:
        if location in regions[region]:
            region_found = True
            label = region_labels[region]
            break
    
    if not region_found:
        label = region_labels["unknown"]

    return label, location

def clean_text(text):
    """ Custom preprocessing function for the tweet text
    """

    retweet_re = re.compile(r"^[rR][tT]")
    gtlt_re = re.compile(r"&[gl]t;")
    
    text = text.lower()
    text = re.sub(r"https?\S+", "", text) # Remove URLS
    # text = re.sub(r"\s+", " ", text) # Replace multiple spaces with a single space - acc went slightly down' so not really helping
    text = "".join([c for c in text if ord(c) < 128])
    
    if retweet_re.search(text) or gtlt_re.search(text): # Remove retweets and the strange &gt; &lt; HTML entities
        return ""

    return text

def remove_newlines(s):
    """ Removes new lines from the string.
    """

    s = s.replace("\r\n", " ")
    s = s.replace("\n", " ")

    return s

def count_custom_occurrence(s):
    """ Counts number of occurrences of "custom_"-like strings in given string.
    """

    m = re.finditer(r"custom_\S+", s)
    m = tuple(m)

    return len(m)