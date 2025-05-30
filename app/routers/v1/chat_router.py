from fastapi import APIRouter, HTTPException

from services import chat_service
from config.logger import logger
from schemas.chat_schema import ChatRequestParams, ChatResponse

chat_router = APIRouter(prefix="/chat", tags=["Chat"])


@chat_router.post("/web", response_model=ChatResponse)
async def chat_completion(request: ChatRequestParams) -> ChatResponse:
    """
    Endpoint to generate chat completions from the LLM based on user input messages.
    """
    try:
        completion = await chat_service.generate_chat_completion(
            request.messages, request.collection_name, request.thread_id
        )
        return ChatResponse(message=completion)
    except HTTPException as e:
        logger.exception(e)
        raise e
