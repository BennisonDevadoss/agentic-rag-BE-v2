from fastapi import APIRouter, HTTPException, Request, Depends

from services import chat_service
from config.logger import logger
from schemas.chat_schema import ChatRequestParams, ChatResponse
from dependencies.captcha import verify_captcha
from dependencies.fingerprint import verify_session_fingerprint

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


@chat_router.post(
    "/porfolio/web",
    dependencies=[Depends(verify_captcha), Depends(verify_session_fingerprint)],
    response_model=ChatResponse,
)
async def chat_completion_web(
    request: Request,  # Request parameter need to be present, if using `slowapi` plugin
    params: ChatRequestParams,
) -> ChatResponse:
    try:
        completion = await chat_service.generate_chat_completion(
            params.messages, params.collection_name, params.thread_id
        )
        return ChatResponse(message=completion)
    except HTTPException as e:
        logger.exception(e)
        raise e
