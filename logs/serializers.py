from rest_framework import serializers, status
from rest_framework.response import Response

from logs.models import Log, Task
from user.models import CustomUser
import json


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('password', )

class LogsSerializer(serializers.ModelSerializer):

    created_by = UserSerializer()

    class Meta:
        model = Log
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return Log.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance


class TasksSerializer(serializers.ModelSerializer):

    created_by = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance
