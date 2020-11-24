from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import json

from user.models import CustomUser
from .models import Task

c = APIClient()

def registration(email, password):
    url = '/api/user/auth/registration'
    data = {
      'email': email,
      'password1': password,
      'password2': password,
    }
    response = c.post(url, data)
    content = json.loads(response.content).get('key')
    return content

class TaskTestCase(TestCase):

  def setUp(self):
    Group.objects.create(
      name='editor'
    )
    Group.objects.create(
      name='manager'
    )

  def test_create_task_authorised(self):
    registration('user02@local.host', 'workw37techture')
    key = registration('user01@local.host', 'workw37techture')
    user = CustomUser.objects.filter(email='user01@local.host')[0]
    group_manager = Group.objects.filter(name='manager')[0]
    user.group = group_manager
    user.save()

    url = '/api/logs/tasks/'
    # logged in and role == manager
    c.login(email="user01@local.host", password="workw37techture")
    data = {
      'subject': 'subject01',
      'description': 'description01',
      'status': 'OP',
      'task_members': '3,4',
    }
    response = c.post(url, data)
    c.logout()
    self.assertEqual(response.status_code, 201)

    # logged in and role != manager
    c.login(email="user02@local.host", password="workw37techture")
    data = {
      'subject': 'subject02',
      'description': 'description01',
      'status': 'OP',
      'task_members': '3,4',
    }
    response = c.post(url, data)
    c.logout()
    self.assertEqual(response.status_code, 401)

    # annoymous user
    data = {
      'subject': 'subject03',
      'description': 'description01',
      'status': 'OP',
      'task_members': '3,4',
    }
    response = c.post(url, data)
    c.logout()
    self.assertEqual(response.status_code, 401)

  def test_update_task_authorised(self):
    registration('user02@local.host', 'workw37techture')
    key = registration('user01@local.host', 'workw37techture')
    user = CustomUser.objects.filter(email='user01@local.host')[0]
    group_manager = Group.objects.filter(name='manager')[0]
    user.group = group_manager
    user.save()

    Task.objects.create(
      subject='subject01',
      description='description01',
      status='OP',
      task_members='3,4',
      created_by=user
    )
    
    task = Task.objects.filter(subject='subject01')[0]
    taskId = task.id
    url = '/api/logs/tasks/' + str(taskId) + '/'
    c.login(email="user01@local.host", password="workw37techture")
    data = {
      'description': 'description02',
      'status': 'FU',
      'task_members': '3,4,5',
    }
    response = c.put(url, data)
    c.logout()
    self.assertEqual(response.status_code, 201)

    c.login(email="user02@local.host", password="workw37techture")
    data = {
      'description': 'description03',
      'task_members': '3',
    }
    response = c.put(url, data)
    c.logout()
    self.assertEqual(response.status_code, 401)

  


    

