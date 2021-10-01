from __future__ import absolute_import


from django import dispatch
from mainapp import codeSignal, hello_celery

from .celery import app as celery_app

@dispatch.receiver(codeSignal)
def receive_signal(sender, **kwargs):
    print('message from other team', sender, kwargs)   # sender: api  kwargs: path='/xxx', name='xxx'

__all__ = ('celery_app',)   # add celery_app object inside project

