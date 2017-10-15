#!/usr/bin/env python

import subprocess
import sys

def create_index(command):
    print("Executing: java -jar java-code/executable/indexengine.jar {0}".format(command))
    subprocess.call(['java', '-jar', 'java-code/executable/indexengine.jar', command])

def search_documents(command, data, number_of_docs):
    print("Executing: java -jar java-code/executable/indexengine.jar {0} {1} {2}".format(command, data, number_of_docs)) 
    subprocess.call(['java', '-jar', 'java-code/executable/indexengine.jar', command, data, number_of_docs])

          
if __name__ == '__main__':
    usage = """Usage
* To create the index run: python3 CREATE_INDEX
* To search documents in the index run: python3 QUERY [QUERY_DATA] [NUMBER_OF_DOCUMENTS]
""" 
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if command == "CREATE_INDEX":
            create_index(command)
        elif command == "QUERY" and len(sys.argv) == 4:
            data = sys.argv[2]
            number_of_docs = sys.argv[3]
            if not number_of_docs.isdigit():
                number_of_docs = '10'
            search_documents(command, data, number_of_docs)
        else:
            print(usage)
    else:
       print(usage)
