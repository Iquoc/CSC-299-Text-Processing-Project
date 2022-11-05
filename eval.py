# Functions for evaluating search results
import dataclasses
import json
from typing import Dict, List

import query_process
from search_api import Query, SearchResults


@dataclasses.dataclass
class EvalEntry:
    query_id: int  # Query id from queries.jsonl file
    result_doc_id: str  # doc_id associated with the result for the query
    eval_value: int  # Manual relevance annotation from tests.tsv


def read_queries(queries_filename: str):
    query_id_to_query = dict()  # A dictionary with query ids as keys and query texts as values.
    with open(queries_filename) as fp:
        for line in fp:
            record = json.loads(line)
            query_id = int(record["_id"])
            query_text = record["metadata"]["query"]
            query_id_to_query[query_id] = query_text
    return query_id_to_query


def run_queries(
        queries_filename: str, query_process: query_process.QueryProcess, num_results: int = 10
) -> Dict[int, List[str]]:
    """
    Runs queries from queries_filename through the search defined by query_process.
    :param queries_filename: jsonl file with queries.
    :param query_process: QueryProcess used to run search.
    :param num_results: Number of results to request for each query.
    :return: Dict that maps query ids to result_doc_id lists.
    """

    query_id_to_query = read_queries(queries_filename)
    query_id_to_result_doc_ids = dict()  # The dict to be returned.
    for query_id, query_string in query_id_to_query.items():
        query: Query = query_process.query_parser.parse_query(query_string, num_results)
        results: SearchResults = query_process.index.search(query)
        query_id_to_result_doc_ids[query_id] = results.result_doc_ids
    return query_id_to_result_doc_ids


def read_tests(tests_filename) -> List[EvalEntry]:
    """
    Reads the relevance ratings into a list of EvalEntries.
    :param tests_filename: Path to the file containing the ratings in tsv format.
    :return: List of EvalEntries.
    """
    out = list()
    with open(tests_filename) as fp:
        head_line = fp.readline()
        for line in fp:
            fields = line.split()
            out.append(
                EvalEntry(
                    query_id=int(fields[0]), result_doc_id=fields[1], eval_value=int(fields[2])))
    return out


def annotate_single_result(
        query_id: int, doc_id: str, reference_values: List[EvalEntry]
) -> EvalEntry:
    for entry in reference_values:
        if entry.query_id == query_id and entry.result_doc_id == doc_id:
            return entry
    return EvalEntry(query_id=query_id, result_doc_id=doc_id, eval_value=0)  # Not relevant.


def annotate_results(query_id_to_result_doc_ids: Dict[int, List[str]],
                     reference_values: List[EvalEntry]) -> List[EvalEntry]:
    """
    Annotate actual results with ratings from human evaluations.
    :param query_id_to_result_doc_ids: The output of run_queries()
    :param reference_values: The output of read_tests().
    :return: List of EvalEntries corresponding to actual results from out search engine.
    """
    out = list()
    for query_id, result_doc_ids in query_id_to_result_doc_ids.items():
        for doc_id in result_doc_ids:
            out.append(annotate_single_result(
                query_id=query_id, doc_id=doc_id, reference_values=reference_values))
    return out


def score_by_sum_of_eval_values(annotated_results: List[EvalEntry]) -> int:
    return sum([e.eval_value for e in annotated_results])

