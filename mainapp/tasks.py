from celery import shared_task
import time
@shared_task
def hello_celery(a, b):
    print("Hello Hogwarts")
    time.sleep(1)
    return a + b