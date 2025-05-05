from celery import Celery

from config.settings import SETTINGS

celery = Celery(
    "worker",
    broker=SETTINGS.REDIS_BASE_URL,
    backend=SETTINGS.REDIS_BASE_URL,
)

# If you need to set any other Celery options
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
    task_routes={
        "tasks.add_numbers": {"queue": "priority_high"},
        "tasks.send_email": {"queue": "emails"},
    },
)

# celery -A app.core.celery_app.celery_app worker --loglevel=info -Q emails,priority_high,default

# # Worker only for emails
# celery -A worker.worker.celery_app worker --loglevel=info -Q emails

# # Worker for priority tasks
# celery -A worker.worker.celery_app worker --loglevel=info -Q priority_high

# # Worker for default
# celery -A worker.worker.celery_app worker --loglevel=info -Q default
