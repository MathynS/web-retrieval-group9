#!/usr/bin/python3.5

import sys
import numpy as np
import networkx as nx

sys.path.insert(0, '../')
from models import connect_to_db, Paper_authors, Authors

amount_authors = 10000

author_matrix = np.zeros([amount_authors, amount_authors])
paper_index = {}

# Create co-author matrix

connect_to_db('../nips-papers.db')

for entry in Paper_authors.select():
    paper, author = entry.paper_id, entry.author_id
    try:
        author = int(author)
    except ValueError:
        continue
    if paper in paper_index:
        paper_index[paper].append(author)
    else:
        paper_index[paper] = [author]

for paper, authors in paper_index.items():
    for author1 in authors:
        for author2 in authors:
            if author1 != author2:
                author_matrix[author1, author2] += 1

# print(author_matrix, 10)

# Graph analysis
G_mat = author_matrix

# Create a directed graph
G1 = nx.DiGraph(G_mat)

# Write edge list to csv file for further analysis in Gephi or something else
    #nx.write_edgelist(G1,'edges.csv',delimiter=',' ,data=False)

# Calculate PageRank per author with parameter alpha = 0.8
pagerank = nx.pagerank(G1, alpha=0.8)
for author in Authors.select():
    author.pagerank = pagerank[author.id]
    author.save()

