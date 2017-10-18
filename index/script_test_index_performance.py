#!/usr/bin/env python

import script_index_engine_controller as engine_controller
import utils.index_models as models
import utils.io_utils as io


test_dir = "data/test"
DATABASE_FILENAME = "data/database.sqlite"

def retrieve_documents_from_index(query_sentence, output_filename):
    documents = engine_controller.search_documents(query_sentence,
                                                    number_of_docs)
    print(documents)
    models.connect_to_db(DATABASE_FILENAME)

    test_result = "query sentence: " + query_sentence
    test_result += "\n---------------------------------------------------------------------\n"
    for doc_id in documents:
        paper_query = models.Papers_NR_NSW.select().where(models.Papers_NR_NSW.id == doc_id)
        if len(paper_query) > 0:
            test_result += "title: " + paper_query[0].pdf_name + "\n\n"
            test_result += paper_query[0].paper_text
            test_result += "\n----------------------------------------------------------------\n\n"
    full_path_output_filename = test_dir + "/" + output_filename
    io.save_file(test_result, full_path_output_filename)
            

if __name__ == '__main__':
    number_of_docs = '10'
    query_sentences = [
        "bullet size in millimeters from lowresolution picture",
        "search only non-malicious real-world web-pages",
        "where to buy power-efficient batteries for mini reactor",
        "tokenization of artificially-generated natural-language",
        "2dimensional non-randomized column-vector",
        "digital-to-analog microelectronic converters used in automobiles",
        "documentation of contaminants in agricultural activities",
        "over-simplified ethics of webspam",
        "usage of telescope during weekends with daylight",
        "TODO: write last query"
    ]

    for i, query_sentence in enumerate(query_sentences):
        output_filename = "index_test_" + str(i) + ".txt"
        print("query: {0}".format(query_sentence))
        retrieve_documents_from_index(query_sentence, output_filename)
