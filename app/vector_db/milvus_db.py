from pymilvus import connections, db, utility, Collection, MilvusException
from langchain_milvus import Milvus

from config.logger import logger
from config.settings import SETTINGS
from config.embedding import embeddings


class MilvusService:
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

    @staticmethod
    def get_vector_store(collection_name) -> None:
        return Milvus(
            drop_old=False,
            index_params={"index_type": "FLAT", "metric_type": "L2"},
            connection_args={
                "uri": f"http://{SETTINGS.MILVUS_HOST}:{SETTINGS.MILVUS_PORT}",
                "db_name": SETTINGS.MILVUS_DB,
            },
            collection_name=collection_name,
            embedding_function=embeddings,
        )
