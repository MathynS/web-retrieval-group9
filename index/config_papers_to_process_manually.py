#!/usr/bin/env python

"""
This file contains the configuration variables needed to run 
the script script_retrieve_papers_to_process_manually.py

* ids_reference_not_separated contains the ids of the papers that have content and reference mixed
* ids_poorly_defined_reference contains the ids of the papers that have content and reference separated but it is not worth doing automatic separation of content for those papers
"""
ids_reference_not_separated = [76, 170, 219, 361, 760, 1501,
                               1617, 4172, 2410]
ids_poorly_defined_reference = [591, 795, 2040, 2047, 2283, 2329,
                                2946, 3443, 3547, 3651, 3727, 3858,
                                3979, 3989, 4016, 4694, 5948, 68]

IRREGULAR_PAPERS_DIRECTORY = "data/irregular-papers"
DATABASE_FILENAME = "data/database.sqlite"
