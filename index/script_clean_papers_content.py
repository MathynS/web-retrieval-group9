#!/usr/bin/env python

import utils.index_models as models
import time
import config_text_cleaner as conf
import utils.text_cleaner as text_cleaner


def create_list_of_ids(first_id, n, max_id):
    ids = []
    last_id = first_id + n
    if first_id + n > max_id:
        last_id = max_id + 1        
    for current_id in range(first_id, last_id):
            ids.append(current_id)
    return ids

def clean_papers():
    models.connect_to_db(conf.DATABASE_FILENAME)

    last_id_query = models.Papers_NR.select().order_by(models.Papers_NR.id.desc()).limit(1)
    first_id = 1
    last_id = last_id_query[0].id
    increments = 10
    paper_cleaner = text_cleaner.Cleaner()
    
    for i in range(first_id, last_id + 1, increments):
        papers_to_process = create_list_of_ids(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers_NR.select().where(models.Papers_NR.id == paper_id)
            
            if len(paper_query) > 0:
                paper_content = paper_query[0].paper_text
                paper_pdf_name = paper_query[0].pdf_name
                print("Cleaning content for paper id: {0}".format(paper_id))
                
                rows_to_clean = paper_content.split("\n")
                cleaned_content = ""
                cleaner = text_cleaner.Cleaner()
                for row in rows_to_clean:
                    cleaned_row = cleaner.clean_text(row)
                    if len(cleaned_row) > 0:
                        cleaned_content += cleaned_row + "\n"
                
                print("Saving new paper_text into papers_NR_NSW")
                new_entry = models.Papers_NR_NSW.create(id=paper_id,
                                                        pdf_name=paper_pdf_name,
                                                        paper_text=cleaned_content)
                print("Number of rows modified: {0}".format(new_entry.save()))

        print("Sleeping for one second ...")
        time.sleep(1)

    models.close_connection()
        

def drop_papers_nr_nsw_table():
    models.connect_to_db(conf.DATABASE_FILENAME)
    models.Papers_NR_NSW.drop_table()
    models.close_connection()
        
if __name__ == '__main__':
    drop_papers_nr_nsw_table()
    clean_papers()

    
