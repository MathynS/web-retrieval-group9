#!/usr/bin/env python

import utils.index_models as models
import config_papers_to_process_manually as conf
import utils.io_utils as io

def create_paper_newname(output_directory, paper_name):
    #print(paper_name)
    #print(paper_name.split(".pdf"))
    #print(str(paper_name.split(".pdf")[0]))
    partial_filename = str(paper_name.split(".pdf")[0]) + ".txt"
    complete_filename = output_directory + "/" + partial_filename
    return complete_filename
    
def retrieve_papers():
    io.create_directory(conf.IRREGULAR_PAPERS_DIRECTORY)
    models.connect_to_db(conf.DATABASE_FILENAME)

    # retrieve papers with reference not separated
    query = models.Papers.select().where(models.Papers.id.in_(conf.ids_reference_not_separated))
    for paper in query:
        filename = create_paper_newname(conf.IRREGULAR_PAPERS_DIRECTORY, paper.pdf_name)
        content = paper.paper_text
        io.save_file(content, filename)
        
    # retrieve papers with poorly defined reference section
    query = models.Papers.select().where(models.Papers.id.in_(conf.ids_poorly_defined_reference))
    for paper in query:
        filename = create_paper_newname(conf.IRREGULAR_PAPERS_DIRECTORY, paper.pdf_name)
        content = paper.paper_text
        io.save_file(content, filename)

    models.close_connection()
        
if __name__ == '__main__':
    retrieve_papers()
