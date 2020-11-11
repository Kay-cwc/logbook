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
        user = request.user
        param = request.data
        project_instance = Task.objects.get(pk=int(param['project']))
        log = Log(
            created_by=user,
            subject=param['subject'],
            detail=param['detail'],
            project=project_instance
        )
        serializers = LogsSerializer(log)
        log.save()
        data = {
            'data': serializers.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        param = request.data 

        log = Log.objects.get(pk=pk)
        log.subject = param['subject'] if param['subject'] is not None else log.subject
        log.detail = param['detail'] if param['detail'] is not None else log.description

        log.save()

        serializers = LogsSerializer(log)
        data = {
            'data': serializers.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request):
        current_user = request.user
        if current_user == None:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        param = request.query_params
        taskid = param.get('taskid') if param.get('taskid') is not None else None
        print(param.get('taskid'))
        queryset = Log.objects.all()
        if taskid != None:
            queryset = queryset.filter(project=taskid)
        serializers = LogsSerializer(queryset, many=True)
        for item in serializers.data:
            print(type(item))
            user_id = item['created_by']
            creater_obj = CustomUser.objects.get(id=user_id)
            creater = UserSerializer(creater_obj).data
            print(type(creater))
            item.update({'created_by_alias': creater['alias']})
        data = {
            'data': serializers.data
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
            description=param['description'],
            task_members=param['task_members']
        )
        serializers = TasksSerializer(task)
        task.save()
        data = {
            'data': serializers.data
        }
        print(serializers.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        param = request.data 
        print(param)

        task = Task.objects.get(pk=pk)
        task.created_by = user
        task.subject = param['subject'] if param['subject'] is not None else task.subject
        task.description = param['description'] if param['description'] is not None else task.description
        task.task_members = param['task_members'] if param['task_members'] is not None else task.task_members
        task.status = param['status'] if param['status'] is not None else task.status

        task.save()

        serializers = TasksSerializer(task)
        data = {
            'data': serializers.data
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
        data = {
            'data': serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        current_user = request.user
        if current_user == None:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Task.objects.get(pk=pk)
        serializers = TasksSerializer(queryset, many=False)
        # user_id = serializers.data['created_by']
        # creater_obj = CustomUser.objects.get(id=user_id)
        # creater = UserSerializer(creater_obj).data

        task_members_obj = []

        for member_id in serializers.data['task_members'].split(','):
            member_obj = CustomUser.objects.get(id=member_id)
            member_obj = UserSerializer(member_obj).data
            task_members_obj.append(member_obj)

        newData = {
            'task_members_obj': task_members_obj
        }
        newData.update(serializers.data)

        return Response(newData, status=status.HTTP_200_OK)
        



