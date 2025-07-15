# https://langchain-ai.github.io/langgraph/how-tos/persistence/#use-in-production

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from config.settings import SETTINGS

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

pool = ConnectionPool(
    kwargs=connection_kwargs,
    max_size=20,
    conninfo=str(SETTINGS.DATABASE_URL),
)
checkpointer = PostgresSaver(pool)

# checkpointer = PostgresSaver.from_conn_string(str(SETTINGS.DATABASE_URL))
# checkpointer.setup()

# with PostgresSaver.from_conn_string(str(SETTINGS.DATABASE_URL)) as checkpointer:
#     checkpointer.setup()
