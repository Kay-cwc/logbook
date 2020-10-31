from django.db import models
from django.conf import settings
from datetime import datetime

from django.contrib.postgres.fields import ArrayField


class Log(models.Model):

    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    detail = models.TextField()
    project = models.ForeignKey('Task', on_delete=models.CASCADE)
    created_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

class Task(models.Model):

    STATUS_CHOICES = [
        ('OP', 'ON PROGRESS'),
        ('RE', 'REVIEWING'),
        ('FU', 'FOLLOW UP'),
        ('CP', 'COMPLETED')
    ]

    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='OP')

    #task_members = ArrayField(models.IntegerField(blank=True), default=list)
    task_members= models.CharField(max_length=999, blank=True)
    created_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

