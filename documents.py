import abc
import dataclasses
from abc import ABC
from typing import List, Iterable, Iterator, Dict


@dataclasses.dataclass
class InputDocument:
    """
    Common raw document representation as produced by Text Aquisition stage.

    This representation is stored in the DocumentCollection.
    """
    doc_id: str
    text: str
    title: str


@dataclasses.dataclass
class TransformedDocument:
    """
    Document representation after the Text Transformation stage.

    This representation is the input to the Indexing stage.
    """
    doc_id: str
    tokens: List[str]


class DocumentCollection(ABC):
    """
    Collection of InputDocuments.

    Abstracts Document Data Store.
    Produced and updated by the indexing process.
    Used by Query Process for User Interactions.
    """
    @abc.abstractmethod
    def get_doc(self, doc_id: str) -> InputDocument:
        """
        Get a document by document id
        :param doc_id: Id of the document to return
        :return: InputDocument with the given doc_id
        """
        pass

    @abc.abstractmethod
    def get_docs(self, doc_ids: Iterable[str]) -> 'DocumentCollection':
        """
        Batch get.
        :param doc_ids: Ids of the documents to retrieve
        :return: A collection of documents with the given ids.
        """
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[InputDocument]:
        """
        :return: Iterator over all documents in the collection.
        """
        pass

    @abc.abstractmethod
    def insert(self, doc: InputDocument) -> None:
        """
        Insert another document into this collection.
        :param doc: an InputDocument to insert
        :return: None
        """
        pass


class DictDocumentCollection(DocumentCollection):
    """
    In memory DocumentCollection that uses a dict of doc_ids and corresponding InputDocuments.
    Implemented as part of HW2 exercise 1.
    """
    def __init__(self, id_to_doc_dict: Dict[str, InputDocument]):
        self.id_to_doc_dict = id_to_doc_dict

    @staticmethod
    def create_empty() -> 'DictDocumentCollection':
        return DictDocumentCollection(dict())

    def get_doc(self, doc_id: str) -> InputDocument:
        return self.id_to_doc_dict[doc_id]

    def get_docs(self, doc_ids: Iterable[str]) -> 'DocumentCollection':
        return DictDocumentCollection({doc_id: self.id_to_doc_dict[doc_id] for doc_id in doc_ids})

    def __iter__(self):
        return self.id_to_doc_dict.values().__iter__()

    def insert(self, doc: InputDocument) -> None:
        self.id_to_doc_dict[doc.doc_id] = doc
