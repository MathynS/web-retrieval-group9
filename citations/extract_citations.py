#!/usr/bin/python3.5

import sys
import time
import re

sys.path.insert(0, '../')
from models import Papers, connect_to_db


connect_to_db('nips-papers.db')


def main():
    for paper in Papers.select().limit(10): 
        citations = re.split('[Rr][Ee][Ff][Ee][Rr][Ee][Nn][Cc][Ee]([Ss])?',
                paper.paper_text)[-1]
        print(citations.split('\n'))

if __name__ == '__main__':
    main()
