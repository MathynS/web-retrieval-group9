#!/usr/bin/env python

import subprocess
import sys
from subprocess import PIPE

query_content_cmd = 'QUERY_CONTENT'
query_title_cmd = 'QUERY_TITLE'
create_index_cmd = 'CREATE_INDEX'

def create_index():
    print("Executing: java -jar java-code/executable/indexengine.jar {0}".format(create_index_cmd))
    subprocess.call(['java', '-jar', 'java-code/executable/indexengine.jar', create_index_cmd])
    

def search_documents_by_content(data, number_of_docs):
    print("Executing: java -jar java-code/executable/indexengine.jar {0} {1} {2}".format(query_content_cmd, data, number_of_docs))
    search = subprocess.Popen(['java', '-jar', 'java-code/executable/indexengine.jar',
                               query_content_cmd, data, number_of_docs],
                              stdout=subprocess.PIPE)
    output = search.communicate()
    ids = str(output[0], 'utf-8').strip().split()
    print(ids)
    return ids

def search_documents_by_title(data, number_of_docs):
    print("Executing: java -jar java-code/executable/indexengine.jar {0} {1} {2}".format(query_title_cmd, data, number_of_docs))
    search = subprocess.Popen(['java', '-jar', 'java-code/executable/indexengine.jar',
                               query_title_cmd, data, number_of_docs],
                              stdout=subprocess.PIPE)
    output = search.communicate()
    ids = str(output[0], 'utf-8').strip().split()
    print(ids)
    return ids

          
if __name__ == '__main__':
    usage = """Usage
* To create the index run: python3 CREATE_INDEX
* To search documents in the index run: python3 [QUERY_CONTENT|QUERY_TITLE] [QUERY_DATA] [NUMBER_OF_DOCUMENTS]
""" 
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if command == create_index_cmd:
            create_index()
        elif command == query_content_cmd and len(sys.argv) == 4:
            data = sys.argv[2]
            number_of_docs = sys.argv[3]
            if not number_of_docs.isdigit():
                number_of_docs = '10'
            search_documents(data, number_of_docs)
        elif command == query_title_cmd and len(sys.argv) == 4:
            data = sys.argv[2]
            number_of_docs = sys.argv[3]
            if not number_of_docs.isdigit():
                number_of_docs = '10'
            search_documents(data, number_of_docs)            
        else:
            print(usage)
    else:
       print(usage)
