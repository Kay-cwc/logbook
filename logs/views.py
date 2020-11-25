from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
        queryset = Log.objects.all()
        if taskid != None:
            queryset = queryset.filter(project=taskid)
        serializers = LogsSerializer(queryset, many=True)
        data = {
            'data': serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

class TasksViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.group == None:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif user.group.name == 'manager':
            param = request.data
            team_member_list = param['task_members'].strip()
            if len(team_member_list) == 0:
                team_member_list = [user.id]
            else:
                team_member_list = team_member_list.split(',')
            if not user.id in team_member_list:
                team_member_list.append(user.id)
            team_member_list = ",".join(map(str,team_member_list))
            task = Task(
                created_by=user,
                subject=param['subject'],
                description=param['description'],
                task_members=team_member_list
            )
            serializers = TasksSerializer(task)
            task.save()
            data = {
                'data': serializers.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        user = request.user
        param = request.data 
        task = Task.objects.filter(pk=pk)[0]
        
        if task.created_by == user:

            for key, value in param.items():
                setattr(task, key, value)
            task.save()
            
            serializers = TasksSerializer(task)
            data = {
                'data': serializers.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        user = request.user
        if user == None:
            data = {
                'data': 'please login first ',
                'accessRight': 'ANONYMOUS',
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if user.group == None: 
            data = {
                'data': 'You must be a manager or an editor to view tasks. Please contact your administrator.',
                'accessRight': 'REGISTERED'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif user.group.name == 'manager':
            queryset = Task.objects.all()
            serializers = TasksSerializer(queryset, many=True)
            data = {
                'data': serializers.data,
                'accessRight': 'MANAGER',
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            userId = user.id
            queryset = Task.objects.filter(task_members__icontains=userId)
            serializers = TasksSerializer(queryset, many=True)
            data = {
                'data': serializers.data,
                'accessRight': 'EDITOR',
            }
            return Response(data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        current_user = request.user
        if current_user == None:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Task.objects.get(pk=pk)
        serializers = TasksSerializer(queryset, many=False)

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
        



