from django.conf import settings
from rest_framework import serializers

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'id',
            'is_active',
            'is_admin',
            'last_login',
        ]
