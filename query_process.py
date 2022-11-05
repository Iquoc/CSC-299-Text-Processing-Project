import abc
import sys
from abc import ABC

import document_source
import documents
from index import Index, NaiveIndex, ListBasedInvertedIndexWithFrequencies
from search_api import Query, SearchResults

from tokenizer import NaiveTokenizer, Tokenizer


class QueryParser(ABC):
    """
    Responsible for converting the input query string entered by a user into the structured Query
    representation.
    """
    @abc.abstractmethod
    def parse_query(self, query_str: str, num_results: int) -> Query:
        """
        Runs the QueryParser logic.
        :param query_str: The input query string entered by the user.
        :param num_results: Number of results requested for this search.
        :return: Structured Query representation to be used by search.
        """
        pass


class NaiveQueryParser(QueryParser):
    """
    A QueryParser implementation that runs the supplied tokenizer.
    """
    def __init__(self, tokenizer: Tokenizer):
        """
        :param tokenizer: A tokenizer instance that will be used in parse_query.
        """
        self.tokenizer = tokenizer

    def parse_query(self, query_str: str, num_results: int) -> Query:
        """
        Runs the tokenizer and wraps the output into a Query dataclass.
        :param query_str: The input query string entered by the user.
        :return: Query representation with tokenized query.
        """
        return Query(terms=self.tokenizer.tokenize(query_str), num_results=num_results)


class ResultFormatter(ABC):
    """
    Abstract class responsible for presenting search results to users.
    """
    @abc.abstractmethod
    def format_results_for_display(self, results: SearchResults) -> str:
        """
        Takes SearchResults dataclass and outputs a string to be displayed to users.
        :param results: Structured representation of search results containing the doc_ids.
        :return: A human-readable string containing all search results as they should be displayed
            to users.
        """
        pass


class NaiveResultFormatter(ResultFormatter):
    """
    Fake result formatter that just displays the doc_ids of the results.
    """
    def format_results_for_display(self, results: SearchResults) -> str:
        return repr(results)


class OutputTitlesResultFormatter(ResultFormatter):
    def __init__(self, document_collection: documents.DocumentCollection):
        self.document_collection = document_collection

    def format_results_for_display(self, results: SearchResults) -> str:
        out = ''
        for doc_id in results.result_doc_ids:
            doc = self.document_collection.get_doc(doc_id)
            out += f'({doc_id}) {doc.title}\n'
        return out


class QueryProcess:
    """
    Class responsible for running the whole query process.
    """
    def __init__(
            self, query_parser: QueryParser, index: Index, result_formatter: ResultFormatter):
        """
        Constructor taking all the necessary components.
        :param query_parser: Specific implementation of a QueryParser.
        :param index: Specific implementation of an Index with all the data necessary to run a
            search.
        :param result_formatter: Specific implementation of a ResultFormatter.
        """
        self.query_parser = query_parser
        self.index = index
        self.result_formatter = result_formatter

    def run(self, query_string: str, num_results: int = 10) -> str:
        """
        Runs the query process.
        :param num_results: The maximum number of the top results to return.
        :param query_string: The query string taken from the user.
        :return: A human-readable representation of search results displayed to the user.
        """
        query: Query = self.query_parser.parse_query(query_string, num_results)
        results: SearchResults = self.index.search(query)
        output_str: str = self.result_formatter.format_results_for_display(results)
        return output_str


def create_naive_query_process(index_filename) -> QueryProcess:
    index = ListBasedInvertedIndexWithFrequencies(index_filename)
    index.read()
    process = QueryProcess(
        query_parser=NaiveQueryParser(NaiveTokenizer()),
        index=index,
        result_formatter=NaiveResultFormatter())
    return process


def create_query_process(index_filename, corpus_filename) -> QueryProcess:
    index = ListBasedInvertedIndexWithFrequencies(index_filename)
    index.read()
    source = document_source.TrecCovidJsonlSource(corpus_filename)
    doc_collection = source.read()
    process = QueryProcess(
        query_parser=NaiveQueryParser(NaiveTokenizer()),
        index=index,
        result_formatter=OutputTitlesResultFormatter(doc_collection))
    return process


def main(index_filename: str) -> None:
    """
    Reads the index from the provided file and runs an interactive query search loop.
    :param index_filename: The file to read the index data from.
    """
    qp = create_query_process(index_filename)
    query = input("Please enter a query:")
    while query:
        print(qp.run(query_string=query))
        query = input("Please enter a query:")


if __name__ == "__main__":
    # sys.argv is a list of all the command-line arguments supplied to the script.
    # sys.argv[0] is the name of this script, so actual arguments start from position 1.
    main(index_filename=sys.argv[1])
