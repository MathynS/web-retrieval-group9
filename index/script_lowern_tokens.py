#!/usr/bin/env python
from utils.text_cleaner import Cleaner
from utils.printer import Printer
import utils.index_models as models
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

def compute_lower_n_tokens_per_doc(lower_n, first_id, last_id):

    models.connect_to_db(conf.DATABASE_FILENAME)
    cleaner = Cleaner()
    lower_n_tokens_per_paper = {}

    for i in range(first_id, last_id + 1, increments):
        papers_to_process = ids_to_query(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers_NR.select().where(models.Papers.id == paper_id)
            if DEBUG:
                print(paper_query)
                print(len(paper_query))

            if len(paper_query) > 0:
                paper_content = paper_query[0].paper_text
                pdf_name = paper_query[0].paper_name
                tokens = cleaner.tokenize(paper_content)
                token_frequencies = {}
                for token in tokens:
                    if token not in token_frequencies:
                        token_frequencies[token] = 1
                    else:
                        token_frequencies[token] = token_frequencies[token] + 1

                sorted_tokens = [(k, token_frequencies[k]) for k in sorted(token_frequencies, key=token_frequencies.get, reverse=True)]
                lower_n_tokens_per_paper[pdf_name] = sorted_tokens[-1*lower_n:]

    models.close_connection()
    printer = Printer()
    printer.print_dict(lower_n_tokens_per_paper)


def compute_lower_n_tokens_for_collection(lower_n):
    
    models.connect_to_db(conf.DATABASE_FILENAME)
    first_id = 1
    last_id_query = models.Papers_NR.select().order_by(models.Papers_NR.id.desc()).limit(1)
    last_id = last_id_query[0].id
    increments = 10
    
    cleaner = Cleaner()
    token_frequencies = {}

    for i in range(first_id, last_id + 1, increments):
        papers_to_process = ids_to_query(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers.select().where(models.Papers.id == paper_id)

            if DEBUG:
                print(paper_query)
                print(len(paper_query))

            if len(paper_query) > 0:
                paper_content = paper_query[0].paper_text
                paper_pdf_name = paper_query[0].pdf_name
                tokens = cleaner.tokenize(paper_content)
    
                for token in tokens:
                    if token not in token_frequencies:
                        token_frequencies[token] = 1
                    else:
                        token_frequencies[token] = token_frequencies[token] + 1

    models.close_connection()
    sorted_tokens = [(k, token_frequencies[k]) for k in sorted(token_frequencies, key=token_frequencies.get, reverse=True)]
    lower_n_tokens = sorted_tokens[-1*lower_n:]
    printer = Printer()
    printer.print_token_frequency(lower_n_tokens)
    

if __name__ == '__main__':

    if conf.LOWERN_OPTION == "all":
        compute_lower_n_tokens_for_collection(conf.LOWERN_NUMBER_OF_TOKENS)
    elif conf.LOWERN_OPTION == "each":
        compute_lower_n_tokens_per_doc(conf.LOWERN_NUMBER_OF_TOKENS,
                                          conf.LOWERN_FIRST_PAPER_ID,
                                          conf.LOWERN_LAST_PAPER_ID)
    else:
        print("Invalid option {0}".format(conf.LOWERN_OPTION))
        exit(1)
