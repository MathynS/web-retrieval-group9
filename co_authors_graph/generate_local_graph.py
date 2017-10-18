#!/usr/bin/python3.5

import sys
import json
import random
import numpy as np

from typing import Union, Any
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", '--author', dest="author", help="Enter an author id", default=30)
parser.add_option("-m", '--max-depth', dest="max_depth", help="Max distance to the base author", default=2)
(options, args) = parser.parse_args()

sys.path.insert(0, '/home/mathyn/Documents/web-retrieval-group9')
from models import connect_to_db, Authors, Paper_authors


def makelist(items: Any) -> list:
    """
    Make a list from an item or of the input is already a list do nothing
    Args:
        items: a single item of any type or a list of item

    Returns: a list of items

    """
    if type(items) in [list, set]:
        return items
    elif type(items) is not int and (items is None or len(items) == 0):
        return []
    else:
        return [items]


def get_co_authors(author_id: str) -> set:
    """
    Retrieves the co authors of an author by looking which papers a given author has created and retrieve the other
    authors that have worked on these papers
    Args:
        author_id: author for which the co authors must be searched

    Returns: list of authors who have worked on the same papers as the given author

    """
    papers = Paper_authors.select().where(Paper_authors.author_id == author_id)
    papers = [p.paper_id for p in papers]
    co_authors = Paper_authors.select().where(Paper_authors.paper_id << papers)

    return set([a.author_id for a in co_authors if a.author_id != int(author_id)])


def add_authors_to_graph(nodes: list, edges: list, author_ids: Union[list, int], base_author_id: int=None) \
        -> (list, list):
    """
    Add a list of author ids to the graph
    Args:
        edges: current list of edges
        nodes: current list of nodes
        author_ids: a list of authors to add to the list
        base_author_id: the author of which the authors should be connected by edges

    Returns: updates list of nodes and edges

    """
    author_ids = makelist(author_ids)
    for author_id in author_ids:
        author = Authors.select().where(Authors.id == author_id).get()
        new_node = {
            "id": author.id,
            "label": author.name,
            "shape": "dot",
            "value": author.pagerank,
            "font": "14px arial black",
            "color": '#97C2FC' if author.id == int(options.author) else '#FB7E81'
        }
        if new_node not in nodes:
            nodes.append(new_node)
        if base_author_id is not None and int(base_author_id) != author.id:
            new_edge = {
                "from": min(author.id, int(base_author_id)),
                "to": max(author.id, int(base_author_id))
            }
            if new_edge not in edges:
                edges.append(new_edge)
    return nodes, edges


def process_author(author_id: int, nodes: list, edges: list,  depth: int=0) -> (list, list):
    """
    Recursive function that creates the graph from an origin author to a certain depth
    Args:
        author_id: origin author
        edges: list of edges
        nodes: list of nodes
        depth: distance to the original author

    Returns: list of edges and list of nodes in the graph

    """
    # nodes, edges = add_authors_to_graph(nodes, edges, author_id)
    co_authors = get_co_authors(author_id)
    nodes, edges = add_authors_to_graph(nodes, edges, co_authors, author_id)
    for co_author in co_authors:
        if depth < int(options.max_depth) and len(nodes) < 150:
            nodes, edges = process_author(co_author, nodes, edges, depth=depth+1)
    return nodes, edges


def main():
    nodes = []
    edges = []
    nodes, edges = add_authors_to_graph(nodes, edges, options.author)
    nodes, edges = process_author(options.author, nodes, edges)
    print(json.dumps({'nodes': nodes, 'edges': edges}))


if __name__ == '__main__':
    connect_to_db('/home/mathyn/Documents/web-retrieval-group9/nips-papers.db')
    main() 
