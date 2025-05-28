import asyncio

from celery import Task

from .worker import celery_app
from config.logger import logger
from utils.crawler import crawl_urls_task_async


class BaseTask(Task):
    autoretry_for = (Exception,)  # Retry for all unhandled exceptions
    retry_kwargs = {"max_retries": 3, "countdown": 10}
    retry_backoff = True  # Exponential backoff
    retry_jitter = True  # Add random jitter to avoid thundering herd
    default_retry_delay = 10  # seconds

    def on_success(self, retval, task_id, args, kwargs) -> None:
        logger.info(f"[{task_id}] ✅ Task completed successfully.")
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo) -> None:
        logger.error(f"[{task_id}] ❌ Task failed with error: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo) -> None:
        logger.warning(f"[{task_id}] 🔁 Task is being retried due to: {exc}")
        super().on_retry(exc, task_id, args, kwargs, einfo)


@celery_app.task(bind=True, base=BaseTask, name="tasks.crawl_urls_task")
def crawl_urls_task(self, collection_name: str, urls: list[str]) -> None:
    _ = asyncio.run(crawl_urls_task_async(urls))  # 👈 wrap async logic


@celery_app.task(bind=True, base=BaseTask, name="tasks.upload_file_task")
def upload_file_task(self, collection_name: str, file_path: str) -> None:
    pass
