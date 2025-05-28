from pydantic import BaseModel, HttpUrl


class CrawlParams(BaseModel):
    collection_name: str
    urls: list[HttpUrl]


class CrawlResponse(BaseModel):
    message: str
    task_id: str


class FileUploadResponse(BaseModel):
    message: str
    task_id: str


class TaskStatusResponse(BaseModel):
    status: str
    task_id: str
    result: str | None = None
