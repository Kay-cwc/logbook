from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from user.models import CustomUser
from user.serializers import UserSerializer
from logs.models import Log, Task
from logs.serializers import LogsSerializer, TasksSerializer
from logs.permissions import IsOwnerOrReadOnly

class LogsViewSet(viewsets.ModelViewSet):

    queryset = Log.objects.all()
    serializer_class = LogsSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        data = {
            'data': 'data'
        }
        return Response(data, status=status.HTTP_200_OK)

class TasksViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TasksSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        param = request.data
        task = Task(
            created_by=user,
            subject=param['subject'],
            description=param['description']
        )
        task.save()
        data = {
            'data': 'task created'
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request):
        current_user = request.user
        if current_user == None:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Task.objects.all()
        serializers = TasksSerializer(queryset, many=True)
        for item in serializers.data:
            print(type(item))
            user_id = item['created_by']
            creater_obj = CustomUser.objects.get(id=user_id)
            creater = UserSerializer(creater_obj).data
            print(type(creater))
            item.update({'created_by_alias': creater['alias']})
        print(serializers.data)    
        data = {
            'data': serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)
        



