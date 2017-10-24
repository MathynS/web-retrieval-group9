#!/usr/bin/python3.5

import scholarly
import csv


def ratings_to_csv(ratings):
    with open('author_rating.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, lineterminator= '\n')
        wr.writerow(ratings)


def get_data(author_name):
    try:
        author_data = next(scholarly.search_author(author_name)).fill()
        h_index = author_data.hindex
        h_index5y = author_data.hindex5y
        i10_index = author_data.i10index
        i10_index5y = author_data.i10index5y
        lst = [h_index, h_index5y, i10_index, i10_index5y]
        print(lst)
        return lst
    except:
        lst = [0, 0, 0, 0]
        print(lst)
        return lst


def main():
    reader = csv.reader(open('pagerank_top.csv', newline=''), delimiter = ',')
    #rating_list = []
    for r in reader:
        print(r[1])
        rating_list = get_data(r[1])
        rating_list.append(r[2])
        ratings_to_csv(rating_list)

if __name__ == '__main__':
    main()