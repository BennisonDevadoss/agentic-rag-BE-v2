import shutil
from typing import List, Any
from tempfile import NamedTemporaryFile

from fastapi import UploadFile
from celery.result import AsyncResult

from queues.tasks import crawl_urls_task, upload_file_task
from queues.worker import celery_app
from config.vector_db import vector_db


# FIXME: this is the temp function (document ingestion process should be executed inside celery tasks.)
def upload_file(
    _: str, file: UploadFile
) -> str:  # collection_name is passed like _ (underscore)
    with NamedTemporaryFile(delete=True, suffix=f"_{file.filename}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name

        documents = vector_db.load_and_split(file_path)
        vector_db.ingest_documents(documents)

    return "File is been ingested to Vector DB successfully!!!"


def start_crawl_task(collection_name: str, urls: List[str]) -> Any:
    task = crawl_urls_task.delay(collection_name=collection_name, urls=urls)
    return task


def start_file_upload_task(collection_name: str, file: UploadFile) -> Any:
    with NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name

    task = upload_file_task.delay(collection_name, file_path)
    return task


def get_task_status(task_id: str) -> dict[str, Any]:
    task_result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": str(task_result.result) if task_result.result else None,
    }
    return response
