#!/usr/bin/python3.5
import sys
import scholar

sys.path.insert(0, '../')
from models import Papers, connect_to_db

# Connect to the database
connect_to_db('../nips-papers.db')

LIMIT = 10

def scrape_citation_count(p):
    query = scholar.SearchScholarQuery()
    #query.set_author(p.author)
    query.set_words(p.title)
    querier = scholar.ScholarQuerier()
    querier.send_query(query)
    print(querier.articles[0].as_txt())
    print(querier.articles[0].attrs['num_citations'][0])
    return querier.articles[0].attrs['num_citations'][0]

def main():
    papers = Papers.select().limit(LIMIT)
    n_citations = []
    for index, p in enumerate(papers):
        n_citations.append(scrape_citation_count(p))

    print(n_citations)

if __name__ == '__main__':
    main()
