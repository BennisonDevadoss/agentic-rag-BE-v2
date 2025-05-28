from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langchain_core.runnables.graph import MermaidDrawMethod

from .state import State
from config.logger import logger
from ..common.checkpointer import checkpointer
from .nodes import (
    grade_documents,
    generate_answer,
    rewrite_question,
    retriever_tool_node,
    generate_query_or_respond,
)

####################################
# DEFINE GRAPH
####################################

builder = StateGraph(State)

# Define the nodes we will cycle between
builder.add_node("generate_query_or_respond", generate_query_or_respond)
builder.add_node("retrieve", retriever_tool_node)
builder.add_node("rewrite_question", rewrite_question)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "generate_query_or_respond")

builder.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "retrieve",
        END: END,
    },
)

builder.add_conditional_edges(
    "retrieve",
    grade_documents,
)
builder.add_edge("generate_answer", END)
builder.add_edge("rewrite_question", "generate_query_or_respond")

###################################
# COMPILE GRAPH
###################################

graph = builder.compile(checkpointer=checkpointer)

try:
    png_data = graph.get_graph(xray=True).draw_mermaid_png(
        draw_method=MermaidDrawMethod.API
    )
    with open("./assets/agentic-rag-graph.png", "wb") as f:
        f.write(png_data)
except Exception as e:
    logger.error(e)
