from rest_framework import serializers, status
from rest_framework.response import Response

from logs.models import Log, Task
import json


class LogsSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance
