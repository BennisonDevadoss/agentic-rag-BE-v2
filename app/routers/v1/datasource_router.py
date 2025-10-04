from typing import Annotated, Any

from fastapi import APIRouter, status, UploadFile, File, Form

from services import datasource_service
from config.logger import logger
from schemas.datasource_schema import (
    CrawlParams,
    CrawlResponse,
    FileUploadResponse,
    TaskStatusResponse,
    TempFileUploadResponse,
)

datasource_router = APIRouter(prefix="/datasource", tags=["datasource"])


@datasource_router.post(
    "/upload/temp",
    response_model=TempFileUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_file(
    collection_name: Annotated[str, Form(...)], file: UploadFile = File(...)
) -> FileUploadResponse:
    try:
        return TempFileUploadResponse(
            message=datasource_service.upload_file(collection_name, file)
        )
    except Exception as e:
        logger.exception(e)
        raise e


@datasource_router.post(
    "/crawl", response_model=CrawlResponse, status_code=status.HTTP_202_ACCEPTED
)
async def start_crawling(params: CrawlParams) -> CrawlResponse:
    try:
        task = datasource_service.start_crawl_task(
            collection_name=params.collection_name, urls=params.model_dump()["urls"]
        )
        return CrawlResponse(message="Crawling started", task_id=task.id)
    except Exception as e:
        logger.exception(e)
        raise e


@datasource_router.post(
    "/upload", response_model=FileUploadResponse, status_code=status.HTTP_202_ACCEPTED
)
async def upload_file(
    collection_name: Annotated[str, Form(...)], file: UploadFile = File(...)
) -> FileUploadResponse:
    try:
        task = datasource_service.start_file_upload_task(collection_name, file)
        return FileUploadResponse(message="File processing started", task_id=task.id)
    except Exception as e:
        logger.exception(e)
        raise e


@datasource_router.get(
    "/task/{task_id}", response_model=TaskStatusResponse, status_code=status.HTTP_200_OK
)
async def check_task_status(task_id: str) -> dict[str, Any]:
    try:
        return datasource_service.get_task_status(task_id)
    except Exception as e:
        logger.exception(e)
        raise e
