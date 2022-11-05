import abc
import json
from abc import ABC

from documents import DocumentCollection, DictDocumentCollection, InputDocument


class DocumentSource(ABC):
    """
    Text Acquisition component of the Indexing Process.

    This can be a feed or a crawled source, though the current interface reads all documents
    at the same time.
    """
    @abc.abstractmethod
    def read(self) -> DocumentCollection:
        """
        Get documents from this source.
        :return: The DocumentCollection of all documents from this source.
        """
        pass


class WikiJsonDocumentSource(DocumentSource):
    """
    DocumentSource that reads documents from wiki_small.json or another file with the same format.

    Implemented as a part of HW2 exercise 2.
    """
    def __init__(self, filename: str):
        """
        Constructor
        :param filename: Full path to the data location.
        """
        self.filename = filename

    def read(self) -> DocumentCollection:
        with open(self.filename) as fp:
            data = json.load(fp)
        docs = DictDocumentCollection.create_empty()
        for record in data:
            docs.insert(InputDocument(doc_id=record['id'], text=record['init_text'], title=record['title']))
        return docs


class TrecCovidJsonlSource(DocumentSource):
    def __init__(self, filename: str):
        self.filename = filename

    def read(self) -> DocumentCollection:
        doc_collection = DictDocumentCollection.create_empty()
        with open(self.filename) as f:
            for line in f:
                record = json.loads(line)
                doc_collection.insert(InputDocument(record['_id'], record['text'], record['title']))
        return doc_collection
