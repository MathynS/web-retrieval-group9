#!/usr/bin/env python
import utils.index_models as models
import sys
import time


ids_reference_not_separated = [76, 170, 219, 361, 760, 1501, 1617, 4172, 2410]
ids_poorly_defined_reference = [591, 795, 2040, 2047, 2283, 2329,
                                2946, 3443, 3547, 3651, 3727, 3858,
                                3979, 3989, 4016, 4694, 5948, 68]
ids_encoding_issues = [558, 644, 873, 905, 940, 1085, 1090, 1148, 
                       1174, 1616, 1866, 5820]
ids_short_paper = [167, 6178, 6260, 797, 799, 807, 870, 984, 992,
                   2703, 173, 198, 405, 1150, 1294, 1533, 1774,
                   1842, 6113, 6114]
ids_no_reference = [218, 62, 709, 734, 1142, 1289, 1612, 1669,
                    1778, 1874, 1912, 1937, 3407, 5823, 6524, 6597]

## Function that creates a list of valid ids used to query the DB
def create_list_of_ids(first_id, n, max_id):
    ids = []
    last_id = first_id + n
    if first_id + n > max_id:
        last_id = max_id + 1
        
    for current_id in range(first_id, last_id):
        invalid_id = False
        if current_id in ids_reference_not_separated:
            invalid_id = True
        elif current_id in ids_poorly_defined_reference:
            invalid_id = True
        elif current_id in ids_encoding_issues:
            invalid_id = True

        if not invalid_id:
            ids.append(current_id)
    return ids


# Function that removes the references from the pdf content
def remove_reference_section(pdf_content):
    rows = pdf_content.split("\n")
    new_pdf_content = ""
    reference_found = False
    references_words = ["references", "bibliography", "referenees", "rererences", "reference8", "references.", "refereneea", "reference", "refereaces", "reference:", "referencess"]
    unwanted_end_symbols = [".", ",", ":", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    
    for row in rows:
        if reference_found:
            break
        
        tokens = row.split()
        new_row = []
        for token in tokens:
            ltoken = token.strip().lower()
            if ltoken[-1] in unwanted_end_symbols:
                ltoken = ltoken[:-1]
            if ltoken in references_words:
                reference_found = True
                break
            new_row.append(token)
            
        new_pdf_content += " ".join(new_row) + "\n"

    return new_pdf_content


DATABASE_FILENAME = "data/database.sqlite"

def clean_papers_from_db():
    models.connect_to_db(DATABASE_FILENAME)
    last_id_query = models.Papers.select().order_by(models.Papers.id.desc()).limit(1)
    first_id = 1
    #last_id = 8
    last_id = last_id_query[0].id
    increments = 10

    for i in range(first_id, last_id + 1, increments):
        papers_to_process = create_list_of_ids(i, increments, last_id)
        for paper_id in papers_to_process:
            paper_query = models.Papers.select().where(models.Papers.id == paper_id)
            print(paper_query)
            print(len(paper_query))
            if (len(paper_query) > 0):
                paper_content = paper_query[0].paper_text
                paper_pdf_name = paper_query[0].pdf_name
                print("Removing reference section from paper id: {0}".format(paper_id))
                new_content = remove_reference_section(paper_content)
                print("Saving new paper_text into papers_for_index")
                new_entry = models.Papers_NR.create(id=paper_id,
                                                       pdf_name=paper_pdf_name,
                                                       paper_text=new_content)
                print("Number of rows modified: {0}".format(new_entry.save()))

        print("Sleeping for one second ...")
        time.sleep(1)

    models.close_connection()

    
def drop_papers_nr_table():
    models.connect_to_db(DATABASE_FILENAME)
    models.Papers_NR.drop_table()
    models.close_connection()
    
        
if __name__ == '__main__':
    drop_papers_nr_table()
    clean_papers_from_db()

