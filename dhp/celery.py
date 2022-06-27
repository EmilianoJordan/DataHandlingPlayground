from celery import Celery

from dhp._env_setup import CELERY_BACKEND, CELERY_BROKER

celery_app = Celery("tasks", backend=CELERY_BACKEND, broker=CELERY_BROKER)
