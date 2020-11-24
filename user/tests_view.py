from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import json

from .models import CustomUser

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

class UserViewTestCase(TestCase):

  def setUp(self):
    Group.objects.create(
      name='editor'
    )
    Group.objects.create(
      name='manager'
    )

  def test_create_user(self):
    url = '/api/user/auth/registration'
    data = {
      'email': 'user02@local.host',
      'password1': 'workw37techture',
      'password2': 'workw37techture'
    }
    response = c.post(url, data)
    self.assertEqual(response.status_code, 201)

  def test_get_user_profile(self):

    key = registration('user01@local.host', 'workw37techture')
    url = '/api/user/auth/user/'
    c.login(email="user01@local.host", password="workw37techture")
    response = c.get(url)
    self.assertEqual(response.status_code, 200)

  def test_assign_user_group_authorized(self):
    # only admin can create 
    registration('user02@local.host', 'workw37techture')
    key = registration('user01@local.host', 'workw37techture')
    user = CustomUser.objects.filter(email='user01@local.host')[0]
    group_manager = Group.objects.filter(name='manager')[0]
    user.group = group_manager
    user.save()

    url = '/api/user/group/assign/'
    c.login(email="user01@local.host", password="workw37techture")
    data = {
      'email': 'user02@local.host',
      'groupId': 2
    }
    response = c.post(url, data)
    self.assertEqual(
      response.data.get('data').get('group').get('name'),
      'editor'
    )

  def test_assign_user_group_unauthorized(self):
    # if not admin, return 401
    registration('user02@local.host', 'workw37techture')

    url = '/api/user/group/assign/'
    c.login(email="user02@local.host", password="workw37techture")
    data = {
      'email': 'user02@local.host',
      'groupId': 2
    }
    response = c.post(url, data)
    self.assertEqual(response.status_code, 401)


  def test_get_user_list_anonymous(self):
    url = '/api/user/group/'
    response = c.get(url)
    self.assertEqual(response.status_code, 403)
    

  def test_get_user_list_authenticated(self):
    registration('user02@local.host', 'workw37techture')
    registration('user03@local.host', 'workw37techture')
    registration('user04@local.host', 'workw37techture')
    registration('user01@local.host', 'workw37techture')
    user = CustomUser.objects.filter(email='user01@local.host')[0]
    group_manager = Group.objects.filter(name='manager')[0]
    user.group = group_manager
    user.save()

    url = '/api/user/group/'

    c.login(email="user01@local.host", password="workw37techture")
    response = c.get(url)
    c.logout()
    self.assertEqual(response.status_code, 200)

    c.login(email="user02@local.host", password="workw37techture")
    response = c.get(url)
    self.assertEqual(response.status_code, 401)

