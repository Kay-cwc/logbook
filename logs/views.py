from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from logs.models import Log, Task
from logs.serializers import LogsSerializer, TasksSerializer
from logs.permissions import IsOwnerOrReadOnly

@method_decorator(csrf_exempt, name='dispatch')
class LogsViewSet(viewsets.ModelViewSet):

    queryset = Log.objects.all()
    serializer_class = LogsSerializer

@method_decorator(csrf_exempt, name='dispatch')
class TasksViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
