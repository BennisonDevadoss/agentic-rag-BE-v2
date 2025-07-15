from typing import Any

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from ..common.callbacks import get_all_callbacks
from langgraph.graph.message import Messages
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
# UTILITIES
####################################


def _print_event(event: dict, _printed: set, max_length: int = 1500) -> str:
    current_state = event.get("dialog_state")
    if current_state:
        logger.info(f"Currently in: {current_state[-1]}")
    message: Messages = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            logger.info(msg_repr)
            _printed.add(message.id)
            logger.info(message)
            return message.content
        return ""
    return ""


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


_printed: Any = set()


async def stream_graph_updates(
    user_input: str, collection_name: str, thread_id: str
) -> str:
    config = {
        "configurable": {
            "thread_id": thread_id,
            "collection_name": collection_name,
        },
        "callbacks": get_all_callbacks(thread_id),
    }

    # response = graph.invoke({"messages": ("user", user_input)}, config=config)
    # return response["messages"][-1].content

    final_output = ""
    events = graph.stream(
        {"messages": ("user", user_input)}, config=config, stream_mode="values"
    )
    for event in events:
        final_output = _print_event(event, _printed)
    return final_output
