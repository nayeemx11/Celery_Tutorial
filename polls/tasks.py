# tasks.py
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def every_10_s():
    return 10



# celery -A celery_tutorial beat -l info
# celery -A celery_tutorial worker --pool=solo -l info