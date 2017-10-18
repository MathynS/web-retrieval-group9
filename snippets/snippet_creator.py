#!/usr/bin/python3.5
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--query", dest="query", help="Enter the search query")
parser.add_option("-d", "--document", dest="document", help="Enter the document comma separated")
parser.add_option("-m", '--max-words', dest="max_words", help="Maximal length of the snippet in words", default=30)
(options, args) = parser.parse_args()

sys.path.insert(0, '/home/mathyn/Documents/web-retrieval-group9')
from models import Papers, connect_to_db


def get_documents() -> list:
    """
    Given the documents in the option parser return the body of these documents
    Returns: list of corpus of bodies

    """
    paper = Papers.select().where(Papers.id == options.document).get()
    return paper.paper_text 


def get_query_words_positions(document_words: list) -> list:
    """
    Searches the index of the query words in the given documents
    Args:
        documents_words: list of documents in which must be searched

    Returns: list of indices of query words per document

    """
    query_words = options.query.split(" ")
    indices = [i for i, q in enumerate(document_words) if q in query_words]
    return indices


def create_snippets(document_words: list, query_words_positions: list) -> list:
    """
    Extract a snippet given a document corpus and an index list of query words
    Args:
        documents_words: list of corpus of the documents
        query_words_positions: list of indices of query words per document corpus

    Returns: list of snippets

    """
    best_score = 0
    tmp_snip = []
    for position in query_words_positions:
        part = range(position, position + int(options.max_words))
        snip_positions = [p for p in query_words_positions if p in part]
        # Prefer text elements where query words are sequential
        subseq_words = [s for s in snip_positions if s + 1 in snip_positions]
        score = len(snip_positions) + 2 * len(subseq_words)
        if score > best_score:
            best_score = score
            tmp_snip = document_words[position: position + int(options.max_words)]
    return " ".join(tmp_snip)


def main():
    connect_to_db('/home/mathyn/Documents/web-retrieval-group9/nips-papers.db')
    document = get_documents()
    document_words = document.replace('\n', " ").split(" ")
    query_words_positions = get_query_words_positions(document_words)
    snippets = create_snippets(document_words, query_words_positions)
    print(snippets)


if __name__ == '__main__':
    main()
