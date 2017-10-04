#!/usr/bin/python3.5
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--query", dest="query", help="Enter the search query")
parser.add_option("-d", "--documents", dest="documents", help="Enter the document comma separated")
parser.add_option("-m", '--max-words', dest="max_words", help="Maximal length of the snippet in words", default=30)
(options, args) = parser.parse_args()

sys.path.insert(0, '../')
from models import Papers, connect_to_db


def get_documents() -> list:
    """
    Given the documents in the option parser return the body of these documents
    Returns: list of corpus of bodies

    """
    document_ids = [d.strip() for d in options.documents.split(',')]
    papers = Papers.select().where(Papers.id << document_ids)
    return [p.paper_text for p in papers]


def get_query_words_positions(documents_words: list) -> list:
    """
    Searches the index of the query words in the given documents
    Args:
        documents_words: list of documents in which must be searched

    Returns: list of indices of query words per document

    """
    result = []
    query_words = options.query.split(" ")
    for document_words in documents_words:
        indices = [i for i, q in enumerate(document_words) if q in query_words]
        result.append(indices)
    return result


def create_snippets(documents_words: list, query_words_positions: list) -> list:
    """
    Extract a snippet given a document corpus and an index list of query words
    Args:
        documents_words: list of corpus of the documents
        query_words_positions: list of indices of query words per document corpus

    Returns: list of snippets

    """
    results = []
    for document_words, positions in zip(documents_words, query_words_positions):
        best_score = 0
        tmp_snip = []
        for position in positions:
            part = range(position, position + options.max_words)
            snip_positions = [p for p in positions if p in part]
            # Prefer text elements where query words are sequential
            subseq_words = [s for s in snip_positions if s + 1 in snip_positions]
            score = len(snip_positions) + 2 * len(subseq_words)
            if score > best_score:
                best_score = score
                tmp_snip = document_words[position: position + options.max_words]
        results.append(" ".join(tmp_snip))
    return results


def main():
    connect_to_db('../nips-papers.db')
    documents = get_documents()
    documents_words = [d.replace('\n', " ").split(" ") for d in documents]
    query_words_positions = get_query_words_positions(documents_words)
    snippets = create_snippets(documents_words, query_words_positions)
    print(snippets)


if __name__ == '__main__':
    main()
