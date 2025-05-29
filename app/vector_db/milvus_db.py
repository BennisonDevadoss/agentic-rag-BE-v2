import os
from uuid import uuid4

from pymilvus import connections, db, utility, Collection, MilvusException
from langchain_milvus import Milvus
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
from config.settings import SETTINGS
from config.embedding import embeddings


class MilvusService:
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name
        self.vector_store = self.get_vector_store()

    @classmethod
    def create_and_reset_db(cls) -> None:
        logger.info("Connecting to Milvus...")
        connections.connect(host=SETTINGS.MILVUS_HOST, port=SETTINGS.MILVUS_PORT)

        try:
            existing_dbs = db.list_database()
            if SETTINGS.MILVUS_DB in existing_dbs:
                db.using_database(SETTINGS.MILVUS_DB)
                for collection_name in utility.list_collections():
                    Collection(name=collection_name).drop()
                    logger.info(f"Dropped collection '{collection_name}'")
                db.drop_database(SETTINGS.MILVUS_DB)
                logger.info(f"Deleted database '{SETTINGS.MILVUS_DB}'")

            db.create_database(SETTINGS.MILVUS_DB)
            logger.info(f"Created database '{SETTINGS.MILVUS_DB}'")
        except MilvusException as e:
            logger.error(f"Milvus error: {e}")
            raise

    def get_vector_store(self) -> Milvus:
        return Milvus(
            drop_old=False,
            index_params={"index_type": "FLAT", "metric_type": "L2"},
            connection_args={
                "uri": f"http://{SETTINGS.MILVUS_HOST}:{SETTINGS.MILVUS_PORT}",
                "db_name": SETTINGS.MILVUS_DB,
            },
            collection_name=self.collection_name,
            embedding_function=embeddings,
        )

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
            return JSONLoader(file_path)
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
