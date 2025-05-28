from celery import Celery

from config.settings import SETTINGS

celery_app = Celery(
    "worker",
    broker=SETTINGS.REDIS_BASE_URL,
    backend=f"db+{SETTINGS.DATABASE_URL}",
    # backend=SETTINGS.REDIS_BASE_URL,
)

celery_app.autodiscover_tasks(["queues"])

# If you need to set any other Celery options
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
    task_routes={
        "tasks.crawl_urls_task": {"queue": "crawler"},
        "tasks.upload_file_task": {"queue": "document"},
    },
)

# PYTHONPATH=. celery -A queues.worker worker --loglevel=info -Q emails,priority_high,default

# # Worker only for emails
# PYTHONPATH=. celery -A worker.worker.celery_app worker --loglevel=info -Q emails

# # Worker for priority tasks
# PYTHONPATH=. celery -A worker.worker.celery_app worker --loglevel=info -Q priority_high

# # Worker for default
# PYTHONPATH=. celery -A worker.worker.celery_app worker --loglevel=info -Q default
