from django.db import models
from django.conf import settings
from datetime import datetime


class Log(models.Model):

    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    detail = models.TextField()
    project = models.ForeignKey('Task', on_delete=models.CASCADE)
    created_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)


class Task(models.Model):

    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
