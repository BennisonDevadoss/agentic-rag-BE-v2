from pymilvus import connections, db, utility, Collection, MilvusException
from langchain_milvus import Milvus

from config.logger import logger
from config.settings import SETTINGS
from config.embedding import embeddings


class MilvusService:
    _vector_store: Milvus | None = None

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

    @classmethod
    def init_vector_store(cls) -> None:
        if cls._vector_store is None:
            cls._vector_store = Milvus(
                drop_old=False,
                index_params={"index_type": "FLAT", "metric_type": "L2"},
                connection_args={
                    "uri": f"http://{SETTINGS.MILVUS_HOST}:{SETTINGS.MILVUS_PORT}",
                    "db_name": SETTINGS.MILVUS_DB,
                },
                embedding_function=embeddings,
            )
            logger.info("Milvus vector store initialized.")

    @classmethod
    def get_vector_store(cls) -> Milvus:
        if cls._vector_store is None:
            raise RuntimeError(
                "Milvus vector store not initialized. Call init_vector_store() first."
            )
        return cls._vector_store
