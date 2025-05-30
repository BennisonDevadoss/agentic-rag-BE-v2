from typing import Any

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain.tools.retriever import create_retriever_tool

from vector_db.milvus_db import MilvusService


# from langchain_core.tools.simple import Tool
# def get_all_retriver_tools(collection_name: str) -> list | list[Tool]:
#     # So for here we have only one retriver tool, if there are multiple retriver - need to handle those things.
#     if collection_name:
#         milvus_service = MilvusService(collection_name)
#         retriever_tool = create_retriever_tool(
#             milvus_service.vector_store.as_retriever(),
#             "retriver_tool",
#             "Search and return information about user query.",
#         )
#         return [retriever_tool]
#     return []


@tool()
def retriever_tool(query: str, config: RunnableConfig) -> Any:
    """Search and return information about user query"""

    collection_name = config["configurable"]["collection_name"]
    milvus_service = MilvusService(collection_name)
    retriever_tool = create_retriever_tool(
        milvus_service.vector_store.as_retriever(),
        "retriver_tool",
        "Search and return information about Lilian Weng blog posts.",
    )
    return retriever_tool.invoke(input=query)
