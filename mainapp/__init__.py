from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django import dispatch

from mainapp.tasks import hello_celery


def model_delete_pre(sender, **kwargs):   # sender is mainapp.models.Student (model.Model child class)
                                                 # kwargs: signal:sender(django.db.models.signals.ModelSignal)
                                                 # using: db name (default)  instance:Student object(1)
    from mainapp.models import Student  # avoid cycling reference

    #print(issubclass(sender, Student))  # true
    #print(isinstance(sender, Student))  # false
    #print(sender is Student)  # true
    #print(sender == Student)  # true
    if sender is Student:
        print('pre-delete',sender, kwargs)


pre_delete.connect(model_delete_pre)  # bind signal to function

@receiver(post_delete)
def model_delete_post(sender, **kwargs):
    from mainapp.models import Student
    if sender is Student:
        print('post-delete',sender, kwargs)


codeSignal = dispatch.Signal(providing_args=['path', 'memo'])   # declare keys param list sending inside signal


