# services/chat_service.py
# import openai  # Example using OpenAI API, replace with your LLM if needed
from typing import List

from agents.agentic_rag.graph import stream_graph_updates


async def generate_chat_completion(
    messages: List[dict], collection_name: str, thread_id: str
) -> str:
    """
    Generates a chat completion from the LLM based on the provided messages.
    """
    return await stream_graph_updates(
        messages[-1]["content"], collection_name, thread_id
    )
