from __future__ import unicode_literals

from django.db import models
from .signals import notify
# Create your models here.


def new_notification(sender,recipient,action,*args,**kwargs):
    print(recipient)
    print action
    print sender
    print args
    print kwargs

notify.connect(new_notification)
