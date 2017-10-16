#!/usr/bin/python3.5
import sys
import scholar
import csv
import time

sys.path.insert(0, '../')
from models import Papers, connect_to_db

# Connect to the database
connect_to_db('../nips-papers.db')

BEGIN = 6284
LIMIT = 6603
COOKIE = "cookies.txt"

def citations_to_csv(n_citations):
    with open('citations.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
        wr.writerow(n_citations)

def scrape_citation_count(p):
    scholar.ScholarConf.COOKIE_JAR_FILE = COOKIE
    query = scholar.SearchScholarQuery()
    #query.set_author(p.author)
    query.set_words(p.title)
    querier = scholar.ScholarQuerier()
    querier.send_query(query)
    #print(querier.articles[0].as_txt())
    try:
        print(querier.articles[0].attrs['num_citations'][0])
        return querier.articles[0].attrs['num_citations'][0]
    except:
        print("Google Scholar captcha :(")
        return -1

def main():
    papers = Papers.select().limit(LIMIT)
    n_citations = []
    for index, p in enumerate(papers[BEGIN:]):
        print(p.id-1)

        n_citations.append(scrape_citation_count(p))
        if n_citations[index] == -1:
            print("Finished after {} iterations".format(index))
            break
        time.sleep(2)
    citations_to_csv(n_citations)
    print(n_citations)

if __name__ == '__main__':
    main()
