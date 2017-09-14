#!/usr/bin/python3.5

import sys
import re

sys.path.insert(0, '../')
from models import Papers, Citations, connect_to_db

# Connect to the database
connect_to_db('nips-papers.db')


def extract_citations():
    """
    Extract citations from the papers, based on the title of other papers
    """
    titles = dict((p.title.strip(), p.id) for p in Papers.select(Papers) if len(p.title.strip().split(' ')) > 1 )
    for paper in Papers.select():
        citations = [titles[t] for t in list(titles.keys()) if t in
                paper.paper_text and titles[t] != paper.id]
        for citation in citations:
            create_citation(paper.id, citation)
        print("Paper {paper_id}".format(paper_id=paper.id))
        print(citations)


def create_citation(source_id, cited_id):
    Citations.create(
        source_paper = source_id,
        cited_paper = cited_id
    )


if __name__ == '__main__':
    extract_citations()
