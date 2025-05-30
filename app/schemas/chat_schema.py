from pydantic import BaseModel


# Pydantic model for the request
class ChatRequestParams(BaseModel):
    messages: list[dict]  # Example: [{"role": "user", "content": "Hello"}]
    thread_id: str
    collection_name: str


# Pydantic model for the response
class ChatResponse(BaseModel):
    message: str
