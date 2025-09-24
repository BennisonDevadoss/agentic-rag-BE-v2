from pymilvus import connections, db, MilvusException
from langchain_milvus import Milvus

from config.logger import logger
from config.settings import SETTINGS
from .base_vector_db import BaseVectorService


class MilvusService(BaseVectorService):
    def get_vector_store(self) -> Milvus:
        return Milvus(
            drop_old=False,
            index_params={"index_type": "FLAT", "metric_type": "L2"},
            connection_args={
                "uri": f"http://{SETTINGS.MILVUS_HOST}:{SETTINGS.MILVUS_PORT}",
                "db_name": SETTINGS.MILVUS_DB,
            },
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
        )

    @classmethod
    def create_and_reset_db(cls) -> None:
        logger.info("Connecting to Milvus...")
        connections.connect(host=SETTINGS.MILVUS_HOST, port=SETTINGS.MILVUS_PORT)
        try:
            existing_dbs = db.list_database()
            if SETTINGS.MILVUS_DB not in existing_dbs:
                db.create_database(SETTINGS.MILVUS_DB)
                logger.info(f"Created database '{SETTINGS.MILVUS_DB}'")
            else:
                logger.info(f"Database '{SETTINGS.MILVUS_DB}' already exists.")
        except MilvusException as e:
            logger.error(f"Milvus error: {e}")
            raise
