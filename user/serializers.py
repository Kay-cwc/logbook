from django.conf import settings
from rest_framework import serializers

from user.models import CustomUser
from rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'alias',
            'group',
        ]
        depth = 1

class CustomRegisterSerializer(RegisterSerializer):
    alias = serializers.CharField(
        required=False,
        max_length=50
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['alias'] = self.validated_data.get('alias', '')
        return data_dict

