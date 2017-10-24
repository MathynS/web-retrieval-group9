#!/usr/bin/python3.5

import scholarly
import sys
import csv

sys.path.insert(0, '../')
from models import Authors, connect_to_db

# Connect to the database
connect_to_db('../nips-papers.db')
LIMIT = 10000

def ratings_to_csv(ratings):
    with open('author_rating.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, lineterminator= '\n')
        wr.writerows(ratings)


def get_data(author_name):
    try:
        author_data = next(scholarly.search_author(author_name)).fill()
        h_index = author_data.hindex
        h_index5y = author_data.hindex5y
        i10_index = author_data.i10index
        i10_index5y = author_data.i10index5y
        lst = [h_index, h_index5y, i10_index, i10_index5y]
        print (lst)
        return lst
    except:
        lst = [0, 0, 0, 0]
        print(lst)
        return lst


def main():
    authors = Authors.select().limit(LIMIT)
    rating_list = []
    for a in authors:
        print(a.name)
        rating_list.append(get_data(a.name))
    ratings_to_csv(rating_list)

if __name__ == '__main__':
    main()