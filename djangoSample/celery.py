from __future__ import absolute_import # absolute path import
from celery import Celery
import os

from celery.signals import task_postrun, task_success, after_task_publish

from mainapp import hello_celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoSample.settings")   # use project name
#app = Celery('hogwartsCelery', broker='redis://127.0.0.1:6379/2')
app = Celery('hogwartsCelery')  # add broker in settings
app.config_from_object("django.conf:settings") # specify the settings file name for celery settings.py
# app.conf.timezone = "Asia/Shanghai"
app.autodiscover_tasks()  # auto discover task

@app.task(bind=True)
def debug_task(self):
    print('Request %s' % self.request)

@after_task_publish.connect(sender = 'mainapp.tasks.hello_celery')
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    print(sender)


@task_postrun.connect()
def task_postrun(sender=None,task=None,**kwargs):
    # note that this hook runs even when there has been an exception thrown by the task
    print("post run {0} ".format(task))

@task_success.connect
def task_success_notifier(sender, result, **kwargs):
    print(sender)
    print(result)
    print("From task_success_notifier ==> Task run successfully!")