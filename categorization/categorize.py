#!/usr/bin/python3.5

import sys
import numpy as np

from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import cosine_distances
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer 
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage

sys.path.insert(0, '../')
from models import Papers, connect_to_db


connect_to_db('nips-papers.db')


def cluster(dm, labels):
    Z = linkage(dm, 'ward')
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    plt.subplots_adjust(bottom=0.4)
    dendrogram(
            Z,
            leaf_rotation=90.,  # rotates the x axis labels
            leaf_font_size=8.,  # font size for the x axis labels
            labels=labels
            )
    plt.show()


def compute_distance(a, b):
    return cosine_distances(a, b)[0][0]


def create_distance_matrix(data):
    n = data.shape[0] 
    distance_array = np.array([compute_distance(data[x], data[y]) if x != y else
        0 for x in
            range(n) for y in range(n)])
    distance_matrix = distance_array.reshape(n, n)
    return squareform(distance_matrix)


def extract_features(data):
    hasher = HashingVectorizer(n_features=1048576,
                               stop_words='english', alternate_sign=False,
                               norm=None, binary=False)
    vectorizer = make_pipeline(hasher, TfidfTransformer())
    return vectorizer.fit_transform(data)
	

def main():
    papers = Papers.select().limit(100)
    labels, data = [p.title for p in papers], [p.paper_text for p in papers]
    data_feat = extract_features(data)
    distance_matrix = create_distance_matrix(data_feat)
    cluster(distance_matrix, labels)

if __name__ == '__main__':
    main()
