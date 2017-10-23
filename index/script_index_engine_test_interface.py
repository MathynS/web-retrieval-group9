#!/usr/bin/env python

import json
import subprocess
import sys
from subprocess import PIPE

query_content_cmd = 'QUERY_CONTENT'
query_title_cmd = 'QUERY_TITLE'
create_index_cmd = 'CREATE_INDEX'
apply_stemming = False

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--query", dest="query", help="Enter the search query", default=None)
parser.add_option("-c", "--command", dest="command", help="Enter the search query")
parser.add_option("-a", "--amount-document", dest="amount", help="Enter the document comma separated", default=None)
(options, args) = parser.parse_args()


def create_index():
    # print("Executing: java -jar java-code/executable/indexengine.jar {0}".format(create_index_cmd))
    #subprocess.call(['java', '-jar', '/home/mathyn/Documents/web-retrieval-group9/index/java-code/executable/indexengine.jar', create_index_cmd])
    subprocess.call(['java', '-jar', '/home/jorge/Documents/courses/third-quartile/information-retrieval/project/web-retrieval-group9/index/java-code/executable/indexengine.jar', create_index_cmd])
    
# TODO Add stemming for query & stopword removal
def stemming(data):
    return data

def search_per_content(command, data, amount):
    # print("Executing: java -jar java-code/executable/indexengine.jar {0} {1} {2}".format(query_cmd, data, number_of_docs))
    if apply_stemming:
        data = stemming(data)
    #search = subprocess.Popen(['java', '-jar', '/home',
                               #command, data, amount],
                              #stdout=subprocess.PIPE)
    search = subprocess.Popen(['java', '-jar', '/home/jorge/Documents/courses/third-quartile/information-retrieval/project/web-retrieval-group9/index/java-code/executable/indexengine.jar', command, data, amount], stdout=subprocess.PIPE)
    output = search.communicate()
    print(output[0])
    return str(output[0], "utf-8").strip().split()

def search_per_title(command, data, amount):
    #search = subprocess.Popen(['java', '-jar', '/home/mathyn/Documents/web-retrieval-group9/index/java-code/executable/indexengine.jar',
                               #command, query, amount],
                              #stdout=subprocess.PIPE)
    search = subprocess.Popen(['java', '-jar', '/home/jorge/Documents/courses/third-quartile/information-retrieval/project/web-retrieval-group9/index/java-code/executable/indexengine.jar', command, data, amount], stdout=subprocess.PIPE)
    output = search.communicate()
    print(output[0])
    return output[0]
if __name__ == '__main__':
    usage = """Usage
* To create the index run: python3 CREATE_INDEX
* To search documents in the index run: python3 QUERY [QUERY_DATA] [NUMBER_OF_DOCUMENTS]
""" 
    if len(sys.argv) >= 2:
        if options.command == create_index_cmd:
            create_index()
        elif options.command == query_content_cmd and options.query is not None and options.amount is not None:
            search_per_content(options.command, options.query, options.amount)
        elif options.command == query_title_cmd and options.query is not None and options.amount is not None:
            search_per_title(options.command, options.query, options.amount)
        else:
            print(usage)
    else:
       print(usage)
