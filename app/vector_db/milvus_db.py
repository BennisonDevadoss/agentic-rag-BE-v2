# https://python.langchain.com/docs/integrations/vectorstores/milvus/

from pymilvus import Collection, MilvusException, connections, db, utility
from langchain_milvus import Milvus

from config.logger import logger
from config.settings import SETTINGS
from config.embedding import embeddings


def create_milvus_database() -> None:
    connections.connect(host=SETTINGS.MILVUS_HOST, port=SETTINGS.MILVUS_PORT)

    # Check if the database exists
    try:
        existing_databases = db.list_database()
        if SETTINGS.MILVUS_DB in existing_databases:
            logger.info(f"Database '{SETTINGS.MILVUS_DB}' already exists.")

            # Use the database context
            db.using_database(SETTINGS.MILVUS_DB)

            # Drop all collections in the database
            collections = utility.list_collections()
            for collection_name in collections:
                collection = Collection(name=collection_name)
                collection.drop()
                logger.info(f"Collection '{collection_name}' has been dropped.")

            db.drop_database(SETTINGS.MILVUS_DB)
            logger.info(f"Database '{SETTINGS.MILVUS_DB}' has been deleted.")
        else:
            logger.info(f"Database '{SETTINGS.MILVUS_DB}' does not exist.")
            db.create_database(SETTINGS.MILVUS_DB)
            logger.info(f"Database '{SETTINGS.MILVUS_DB}' created successfully.")
    except MilvusException as e:
        logger.error(f"An error occurred: {e}")


vector_store = Milvus(
    drop_old=False,
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    connection_args={
        "uri": f"http://{SETTINGS.MILVUS_HOST}:{SETTINGS.MILVUS_PORT}",
        "db_name": SETTINGS.MILVUS_DB,
    },
    embedding_function=embeddings,
)
