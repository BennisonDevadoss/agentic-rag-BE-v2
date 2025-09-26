from .embedding import embedding
from config.settings import SETTINGS
from config.constants import VECTOR_DB_PROVIDERS
from vector_db.milvus_db import MilvusService

# from vector_db.pg_vector_db import PGVectorService #TODO: need to setup PG-VECTOR to use postgres as VectorDB.
from vector_db.chroma_vector_db import ChromaVectorService

vector_db = None


match SETTINGS.VECTOR_DB_PROVIDER.lower():
    case VECTOR_DB_PROVIDERS.MILVUS:
        vector_db = MilvusService(
            collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME,
            embedding_model=embedding,
        )
    case VECTOR_DB_PROVIDERS.PG_VECTOR:
        pass
        # vector_db = PGVectorService(
        #     collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME,
        #     embedding_model=embedding,
        # )
    case _:
        vector_db = ChromaVectorService(
            collection_name=SETTINGS.VECTOR_DB_COLLECTION_NAME,
            embedding_model=embedding,
        )
