from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langchain_core.runnables.graph import MermaidDrawMethod

from .state import State
from config.logger import logger
from ..common.checkpointer import checkpointer
from .nodes import (
    retriever_tool_node,
    generate_query_or_respond_node,
    rewrite_question_assistant_node,
    document_greading_assistant_node,
    generate_answer_assistant_node,
)

####################################
# DEFINE GRAPH
####################################

builder = StateGraph(State)

# Define the nodes we will cycle between
builder.add_node("generate_query_or_respond", generate_query_or_respond_node)
builder.add_node("retrieve", retriever_tool_node)
builder.add_node("rewrite_question_assistant", rewrite_question_assistant_node)
builder.add_node("generate_answer_assistant", generate_answer_assistant_node)
builder.add_node("document_grading_assistant", document_greading_assistant_node)

builder.add_edge(START, "generate_query_or_respond")

# Decide whether to retrieve
builder.add_conditional_edges(
    "generate_query_or_respond",
    # Assess LLM decision (call `retriever_tool` tool or respond to the user)
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

# Edges taken after the `action` node is called.
builder.add_conditional_edges(
    "retrieve",
    # Assess agent decision
    "document_grading_assistant",
)
builder.add_edge("generate_answer_assistant", END)
builder.add_edge("rewrite_question_assistant", "generate_query_or_respond")

###################################
# COMPILE GRAPH
###################################

graph = builder.compile(checkpointer=checkpointer)

try:
    png_data = graph.get_graph(xray=True).draw_mermaid_png(
        draw_method=MermaidDrawMethod.API
    )
    with open("./assets/multimodel-rag-graph.png", "wb") as f:
        f.write(png_data)
except Exception as e:
    logger.error(e)
    pass
