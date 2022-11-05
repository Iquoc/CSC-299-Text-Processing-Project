import document_source
from document_source import DocumentSource, WikiJsonDocumentSource
from document_transformer import DocumentTransformer, NaiveSearchDocumentTransformer
from index import Index, Indexer, NaiveIndexer, SingleIndexIndexer, ListBasedInvertedIndexWithFrequencies
from tokenizer import NaiveTokenizer


class DefaultIndexingProcess:
    """
    Simple implementation of the indexing prorocess.

    This class runs components of the indexing process supplied to it either in the constructor
    or in the arguments to the |run| function below.
    """
    def __init__(self, document_transformer: DocumentTransformer, indexer: Indexer):
        self.document_transformer = document_transformer
        self.indexer = indexer

    def run(self, source: DocumentSource) -> Index:
        """
        Runs the Indexing Process using the supplied components.
        :param source: Source of documents to index.
        :return: An index used to search documents from the given source.
        """
        # Run the aquisition stage, or just load the results of that stage. Enable iteration over
        # all documents from the given source.
        document_collection = source.read()
        # Create an empty index. Documents will be added one at a time.
        index = self.indexer.create_index()
        for doc in document_collection:
            # Transform and index the document.
            transformed_doc = self.document_transformer.transform_document(doc)
            index.add_document(transformed_doc)
        return index


def create_naive_indexing_process(index_filename: str) -> DefaultIndexingProcess:
    return DefaultIndexingProcess(
        document_transformer=NaiveSearchDocumentTransformer(tokenizer=NaiveTokenizer()),
        indexer=NaiveIndexer(index_filename))


def run_naive_indexing_process(input_filename: str, output_filename: str):
    ip = create_naive_indexing_process(output_filename)
    index = ip.run(WikiJsonDocumentSource(input_filename))
    index.write()


def create_tf_idf_indexing_process(index_filename: str) -> DefaultIndexingProcess:
    return DefaultIndexingProcess(
        document_transformer=NaiveSearchDocumentTransformer(tokenizer=NaiveTokenizer()),
        indexer=SingleIndexIndexer(ListBasedInvertedIndexWithFrequencies(index_filename)))


def run_covid_trec_indexing_process(input_filename: str, output_filename: str):
    ip = create_tf_idf_indexing_process(output_filename)
    index = ip.run(source=document_source.TrecCovidJsonlSource(input_filename))
    index.write()
