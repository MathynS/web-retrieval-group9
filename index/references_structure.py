#!/usr/bin/env python
import sqlite3
import sys

DEBUG = True
def count_explicit_references():
    database_file = '../data/database.sqlite'
    db_connection = sqlite3.connect(database_file)
    cursor = db_connection.cursor()
    references_words = ["references", "bibliography", "referenees", "rererences", "reference8", "references.", "refereneea", "reference", "refereaces", "reference:", "referencess"]
    unwanted_end_symbols = [".", ",", ":", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    select_cmd = 'SELECT pdf_name, paper_text from papers;'
    if DEBUG:
        select_cmd = 'SELECT pdf_name, paper_text from papers where id = 167;'

    explicit_references = []
    implicit_references = []
    for element in cursor.execute(select_cmd):
        pdf_name = element[0]
        text = element[1]
        rows = text.split("\n")
        contains_reference = False
        for row in rows:
            if DEBUG:
                print(">>")
                print(row)
            tokens = row.split()
            for token in tokens:
                #if DEBUG:
                    #print(token)
                ltoken = token.strip().lower()
                if ltoken[-1] in unwanted_end_symbols:
                    ltoken = ltoken[:-1]
                if ltoken in references_words:
                    contains_reference = True
                    break
            if contains_reference:
                break

        if contains_reference:
            explicit_references.append(pdf_name)
        else:
            implicit_references.append(pdf_name)

    db_connection.close()

    for pdf_name in implicit_references:
        print(pdf_name)

    print("Reference text appears {0} times".format(len(explicit_references)))
    print("Reference text does not appear {0} times".format(len(implicit_references)))

        
if __name__ == '__main__':
    count_explicit_references()
