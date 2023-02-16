from celery import shared_task
import time


@shared_task
def hello():
    time.sleep(1)
    print("Hello, world!")


@shared_task
def weekly_notifications():

    pass
