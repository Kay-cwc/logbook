from django.test import TestCase
from django.contrib.auth.models import Group

from .models import CustomUser
# Create your tests here.

class UserTestCase(TestCase):
  
  def setUp(self):
    CustomUser.objects.create(
      email="user01@local.host",
      password="qwerty1234",
      is_active=True,
      is_admin=True,
      alias='user01',
    )

    # create group object
    Group.objects.create(
      name='editor'
    )
    Group.objects.create(
      name='manager'
    )

    