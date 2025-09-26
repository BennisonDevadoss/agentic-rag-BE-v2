from langchain_postgres import PGVector

from config.settings import SETTINGS

# from .base_vector_db import BaseVectorService
from .base_vector_db import BaseVectorService


class PGVectorService(BaseVectorService):
    def get_vector_store(self) -> PGVector:
        return PGVector(
            embeddings=self.embedding_model,
            collection_name=self.collection_name,
            connection=str(
                SETTINGS.PG_VECTOR_DB_URL
            ),  # e.g. "postgresql+psycopg://user:pass@host:port/db"
            use_jsonb=True,
        )
