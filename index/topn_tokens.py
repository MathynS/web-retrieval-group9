#!/usr/bin/env python
import sqlite3
import sys
from utils.text_cleaner import Cleaner
from utils.printer import Printer

def compute_top_n_tokens(top_n, for_all, first_id, last_id):

    database_file = '../data/database.sqlite'
    db_connection = sqlite3.connect(database_file)
    cursor = db_connection.cursor()

    select_cmd = ''
    if for_all:
        select_cmd = 'SELECT pdf_name, paper_text from papers;'
    else:    
        select_cmd = 'SELECT pdf_name, paper_text from papers WHERE id >= ' + str(first_id)  + ' AND id <= ' + str(last_id) + ';'

    cleaner = Cleaner()
    top_n_tokens_per_paper = {}
    
    for counter, row in enumerate(cursor.execute(select_cmd)):
        if counter % 100 == 0:
            print("Processing pdf text number: {0}".format(counter))
            
        pdf_name = row[0]
        tokens = cleaner.tokenize(row[1])
        token_frequencies = {}
        for token in tokens:
            if token not in token_frequencies:
                token_frequencies[token] = 1
            else:
                token_frequencies[token] = token_frequencies[token] + 1

        sorted_tokens = [(k, token_frequencies[k]) for k in sorted(token_frequencies, key=token_frequencies.get, reverse=True)]
        top_n_tokens_per_paper[pdf_name] = sorted_tokens[:top_n]

    db_connection.close()
    printer = Printer()
    printer.print_dict(top_n_tokens_per_paper)
    

if __name__ == '__main__':

    # default values for computing the top n tokens in pdf text content
    top_n = 20
    first_paper_id = 1
    last_paper_id = 10
    for_all = False
    
    if len(sys.argv) >= 3:
        option = sys.argv[1].strip()
        top_n = int(sys.argv[2].strip())
        if option == 'n' and len(sys.argv) == 5:
            first_paper_id = int(sys.argv[3].strip())
            last_paper_id = int(sys.argv[4].strip())
        elif option == 'all':
            for_all = True
        else:
            print("Wrong parameters!")
            exit(1)
            
    compute_top_n_tokens(top_n, for_all, first_paper_id, last_paper_id)
    
