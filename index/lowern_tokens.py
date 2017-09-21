#!/usr/bin/env python
import sqlite3
import sys
from utils.text_cleaner import Cleaner
from utils.printer import Printer

DEBUG = False

def compute_lower_n_tokens_per_doc(lower_n, for_all, first_id, last_id):

    database_file = '../data/database.sqlite'
    db_connection = sqlite3.connect(database_file)
    cursor = db_connection.cursor()

    select_cmd = ''
    if for_all:
        select_cmd = 'SELECT pdf_name, paper_text from papers;'
    else:    
        select_cmd = 'SELECT pdf_name, paper_text from papers WHERE id >= ' + str(first_id)  + ' AND id <= ' + str(last_id) + ';'

    cleaner = Cleaner()
    lower_n_tokens_per_paper = {}
    
    for counter, row in enumerate(cursor.execute(select_cmd)):
        if DEBUG and counter % 100 == 0:
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
        lower_n_tokens_per_paper[pdf_name] = sorted_tokens[-1*lower_n:]

    db_connection.close()
    printer = Printer()
    printer.print_dict(lower_n_tokens_per_paper)


def compute_lower_n_tokens_for_collection(lower_n):
    
    database_file = '../data/database.sqlite'
    db_connection = sqlite3.connect(database_file)
    cursor = db_connection.cursor()

    select_cmd = 'SELECT pdf_name, paper_text from papers;'
    cleaner = Cleaner()
    token_frequencies = {}
    
    for counter, row in enumerate(cursor.execute(select_cmd)):
        if DEBUG and counter % 100 == 0:
            print("Processing pdf text number: {0}".format(counter))
            
        pdf_name = row[0]
        tokens = cleaner.tokenize(row[1])
        for token in tokens:
            if token not in token_frequencies:
                token_frequencies[token] = 1
            else:
                token_frequencies[token] = token_frequencies[token] + 1

    db_connection.close()
    sorted_tokens = [(k, token_frequencies[k]) for k in sorted(token_frequencies, key=token_frequencies.get, reverse=True)]
    lower_n_tokens = sorted_tokens[-1*lower_n:]
    print(lower_n_tokens)
    

if __name__ == '__main__':

    instructions = "\nThere are three ways to use this script to compute the lower n tokens that appear in the pdfs' text contained in the database\n"
    instructions += "1) To compute the lower n tokens for a range of pdfs run the following command:\n"
    instructions += "\tpython3 lowern_tokens n [lower_n] [first_paper_id] [last_paper_id]\n"
    instructions += "2) To compute the lower n tokens for each of the pdfs run the following command:\n"
    instructions += "\tpython3 lowern_tokens each [lower_n]\n"
    instructions += "3) To compute the lower n tokens for all the pdfs run the following command:\n"
    instructions += "\tpython3 lowern_tokens all [lower_n]\n\n"
    instructions += "Where:\n\t[lower_n] corresponds to the number of the least frequent tokens you want to see,\n"
    instructions += "\t[first_paper_id] corresponds to the first paper that will be queried from the database, and\n"
    instructions += "\t[last_paper_id] corresponds to the last paper that will be queried from the database\n"
    
    if len(sys.argv) >= 3:
        option = sys.argv[1].strip()
        lower_n = int(sys.argv[2].strip())
        if option == 'n' and len(sys.argv) == 5:
            first_paper_id = int(sys.argv[3].strip())
            last_paper_id = int(sys.argv[4].strip())
            compute_lower_n_tokens_per_doc(lower_n, False, first_paper_id, last_paper_id)
        elif option == 'each':
            compute_lower_n_tokens_per_doc(lower_n, True, None, None)
        elif option == 'all':
            compute_lower_n_tokens_for_collection(lower_n)
        else:
            print(instructions)
            exit(1)
    else:
        print(instructions)
        exit(1)

    