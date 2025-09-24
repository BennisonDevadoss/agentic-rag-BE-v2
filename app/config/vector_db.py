from config.constants import VECTOR_DB_PROVIDERS
from config.settings import SETTINGS

from vector_db.milvus_db import MilvusService
from vector_db.pg_vector_db import PGVectorService
from .embedding import embedding


vector_db = None
# def load_vector_db(
#     provider: str,
#     collection_name: str,
#     embedding_model: Any,
#     top_k: int = 4,
#     chunk_size: int = 1000,
#     chunk_overlap: int = 200,
# ) -> MilvusService | PGVectorService:
#     provider = provider.lower()


match SETTINGS.VECTOR_DB_PROVIDER.lower():
    case VECTOR_DB_PROVIDERS.MILVUS:
        print('LOADING MILVUS DB ##########')
        vector_db = MilvusService(
            collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME,
            embedding_model=embedding,
        )
    case VECTOR_DB_PROVIDERS.PG_VECTOR:
        print('LOADING PG_VECTOR DB ##########')
        vector_db = PGVectorService(
            collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME,
            embedding_model=embedding,
        )
    case _:
        raise Exception("Unable to load any vector DB")
