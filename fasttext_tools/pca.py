import codecs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-model", help=".vec model file location")
args = parser.parse_args()

with codecs.open(args.model, 'rU', 'utf-8') as stream:
    vecs = []
    i = 0
    for line in stream:
        i += 1

        if i == 1:
            continue
        
        if i % 10000 == 0:
            print i

        vec = map(float, line.split(" ")[1:-1])
        vecs.append(vec)

    pca = PCA(n_components=2)
    vecs_2d = pca.fit_transform(vecs)
    vecs_2d_x = []
    vecs_2d_y = []

    for el in vecs_2d:
        vecs_2d_x.append(el[0])
        vecs_2d_y.append(el[1])
    
    plt.plot(vecs_2d_x, vecs_2d_y, "bo")
    plt.show()
