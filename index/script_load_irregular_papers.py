#!/usr/bin/env python

import utils.index_models as models
import utils.io_utils as io
import config_papers_to_process_manually as conf

def extract_id_from_filename(filename):
    return filename.split('-')[0]

def create_pdf_filename(filename):
    return filename.split(".txt")[0] + ".pdf" 

def save_cleaned_files(input_directory):
    filenames = io.list_files_in_dir(input_directory)
    models.connect_to_db(conf.DATABASE_FILENAME)
    for filename in filenames:
        print("Saving {} into DB".format(filename))
        paper_id = extract_id_from_filename(filename)
        paper_pdf_name = create_pdf_filename(filename)
        file_path = conf.IRREGULAR_PAPERS_DIRECTORY + "/" + filename
        paper_content = io.load_file_rows(file_path)
        new_entry = models.Papers_NR.create(id=paper_id,
                                            pdf_name=paper_pdf_name,
                                            paper_text=paper_content)
        print("Number of rows modified: {0}".format(new_entry.save()))
        
    models.close_connection()


if __name__ == '__main__':
    save_cleaned_files(conf.IRREGULAR_PAPERS_DIRECTORY)
