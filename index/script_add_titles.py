#!/usr/bin/env python

import utils.index_models as models
import time

DATABASE_FILENAME = "data/database.sqlite"
increments = 50

def create_list_of_ids(first_id, n, max_id):
    ids = []
    last_id = first_id + n
    if first_id + n > max_id:
        last_id = max_id + 1        
    for current_id in range(first_id, last_id):
            ids.append(current_id)
    return ids

def insert_title_column_to_nr_nsw_table():
    models.connect_to_db(DATABASE_FILENAME)
    last_id_query = models.Papers_NR.select().order_by(models.Papers_NR.id.desc()).limit(1)
    first_id = 1
    last_id = last_id_query[0].id
    last_id = 100
    increments = 50

    for i in range(first_id, last_id + 1, increments):
        papers_to_process = create_list_of_ids(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers_NR.select().where(models.Papers_NR.id == paper_id)
            
            if len(paper_query) > 0:
                paper_pdf_name = paper_query[0].pdf_name
                
                title = paper_pdf_name.split(".pdf")[0]
                print("Title before replace: {0}".format(title))
                title = title.replace("-", " ")
                print("Title after replace: {0}".format(title))
                new_entry = models.Papers_NR_NSW.create(id=paper_id,
                                                        pdf_name=paper_pdf_name,
                                                        paper_text=cleaned_content)
                new_entry.save()                
                

        counter += increments
        print("Number of documents cleaned: {0}".format(counter))
        print("Sleeping for one second ...")
        time.sleep(1)

    models.close_connection()
    

if __name__ == '__main__':
    insert_title_column_to_nr_nsw_table()
