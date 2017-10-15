# Overview

This document contains information that describe the following operations.
* Create the database that is going to be used during the creation of the index.
* Creation of the index.
* Searching for documents in the index.

## Prepare the index database
The operations required to create the index database are detailed below.
1. Place the file `database.sqlite` in the `index/data/` directory. This file contains a sqlite database with the papers that are going to be indexed.
2. Run the python script `script_extract_content_from_papers.py`. This script removes the reference section for most of the entries in the database. After the script finishes the table `Papers_NR` will be populated with the resulting papers after removing references.
3. Run the python script `script_load_irregular_papers.py`. This script loads several papers that were processed manually to remove their reference section. The papers content will be also inserted into the table `Papers_NR`
4. Run the python script `script_clean_papers_content.py`. This script removes noise characters and words from the content of the papers in the `Papers_NR` table. The cleaned content for each paper is inserted into the table `Papers_NR_NSW`

At this point the `Papers_NR_NSW` is ready to be used to create the index.

## Create the index
To create the index run the following command in a command line.<br/>
`python3 script_index_engine_controller.py CREATE_INDEX`


## Search documents in the index
To search documents in the index run the following command in a command line. <br/> `python3 script_index_engine_controller.py QUERY [words] [number of docs]` <br/> Where `[words]` is a sequence of words like "neural networks", "optimization process", or "information retrieval with genetic algorithms", and `[number of docs]` is the maximum number of document ids you want to retrieve from the index.