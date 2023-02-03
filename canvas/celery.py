import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "canvas.settings")


app = Celery("canvas")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.update(
    BROKER_URL=os.environ["REDIS_URL"], CELERY_RESULT_BACKEND=os.environ["REDIS_URL"]
)

app.conf.update(
    result_expires=3600,
)
