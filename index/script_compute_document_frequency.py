#!/usr/bin/env python
from utils.text_cleaner import Cleaner
from utils.printer import Printer
import utils.index_models as models
from utils.index_models import Papers_NR_NSW as papers
import config_ntokens as conf

DEBUG = False

def ids_to_query(first_id, n, max_id):
    ids = []
    last_id = first_id + n
    if first_id + n > max_id:
        last_id = max_id + 1
        
    for current_id in range(first_id, last_id):
        ids.append(current_id)

    return ids


def compute_document_frequencies():

    models.connect_to_db(conf.DATABASE_FILENAME)
    first_id = 1
    last_id_query = papers.select().order_by(papers.id.desc()).limit(1)
    last_id = last_id_query[0].id
    increments = 10

    token_frequencies = {}

    for i in range(first_id, last_id + 1, increments):
        papers_to_process = ids_to_query(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = papers.select().where(papers.id == paper_id)

            unique_tokens = set()
            
            if DEBUG:
                print(paper_query)
                print(len(paper_query))

            if len(paper_query) > 0:
                paper_content = paper_query[0].paper_text
                paper_pdf_name = paper_query[0].pdf_name
                tokens = paper_content.strip().split()
                for token in tokens:
                    #print(token)
                    unique_tokens.add(token.lower())

                for i, token in enumerate(unique_tokens):
                    #print(token)
                    if token not in token_frequencies:
                        token_frequencies[token] = 1
                    else:
                        token_frequencies[token] = token_frequencies[token] + 1
                
    models.close_connection()
    sorted_tokens = [(k, token_frequencies[k]) for k in sorted(token_frequencies, key=token_frequencies.get)]
    printer = Printer()
    printer.print_token_frequency(sorted_tokens)
    

if __name__ == '__main__':
    compute_document_frequencies()                

    
