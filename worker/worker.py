import os
from celery import Celery
import time
broker_url = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery_app = Celery(name='worker', broker=broker_url, result_backend=res_backend)
@celery_app.task
def get_count(text):
    try:
        wrd_count = len(text.split())
        time.sleep(wrd_count)
        return wrd_count
    except Exception as e:
        print(e)
        return str(e)