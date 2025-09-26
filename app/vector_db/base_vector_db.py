import os
from abc import ABC, abstractmethod

from langchain_milvus import Milvus
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader,
    JSONLoader,
    PyMuPDFLoader,
    UnstructuredHTMLLoader,
    UnstructuredExcelLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)


from config.logger import logger


class BaseVectorService(ABC):
    def __init__(
        self,
        collection_name: str,
        embedding_model: (
            OpenAIEmbeddings
            | HuggingFaceEmbeddings
            | HuggingFaceEmbeddings
            | GoogleGenerativeAIEmbeddings
        ),
    ) -> None:
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.vector_store = self.get_vector_store()

    @abstractmethod
    def get_vector_store(self) -> Milvus | PGVector | Chroma:
        pass

    def get_loader(
        self,
        file_path: str,
    ) -> (
        CSVLoader
        | TextLoader
        | JSONLoader
        | PyMuPDFLoader
        | UnstructuredHTMLLoader
        | UnstructuredExcelLoader
        | UnstructuredMarkdownLoader
        | UnstructuredPowerPointLoader
        | UnstructuredWordDocumentLoader
    ):
        ext = os.path.splitext(file_path)[-1].lower()

        if ext == ".pdf":
            return PyMuPDFLoader(file_path)
        if ext == ".md":
            return UnstructuredMarkdownLoader(file_path)
        elif ext == ".docx":
            return UnstructuredWordDocumentLoader(file_path)
        elif ext in [".txt"]:
            return TextLoader(file_path)
        elif ext == ".csv":
            return CSVLoader(file_path)
        elif ext == ".json":
            return JSONLoader(file_path)  # type: ignore
        elif ext in [".xls", ".xlsx"]:
            return UnstructuredExcelLoader(file_path)
        elif ext == ".pptx":
            return UnstructuredPowerPointLoader(file_path)
        elif ext in [".html", ".htm"]:
            return UnstructuredHTMLLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def load_and_split(
        self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> list[Document]:
        logger.info(f"Loading and splitting content from file path: {file_path}")
        loader = self.get_loader(file_path)
        raw_docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        split_docs = text_splitter.split_documents(raw_docs)
        logger.info(f"Loaded and split into {len(split_docs)} chunks.")
        return split_docs

    def ingest_documents(self, documents: list[Document]) -> list[str]:
        from uuid import uuid4

        uuids = [str(uuid4()) for _ in documents]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        logger.info(
            f"Ingested {len(documents)} documents into collection '{self.collection_name}'"
        )
        return uuids

    def delete_documents(self, ids: list[str]) -> None:
        self.vector_store.delete(ids=ids)
        logger.info(
            f"Deleted {len(ids)} documents from collection '{self.collection_name}'"
        )

    def append_documents(self, documents: list[Document]) -> list[str]:
        return self.ingest_documents(documents)

    def similarity_search(
        self, query: str, k: int = 5, expr: str | None = None
    ) -> list[Document]:
        results = self.vector_store.similarity_search(query, k=k, expr=expr)
        logger.info(
            f"Similarity search returned {len(results)} results for query: '{query}'"
        )
        return results
