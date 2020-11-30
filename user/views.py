from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.db import transaction
from django.contrib.auth.models import Group
from django.core import serializers

from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# activation email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

import json

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.serializers import UserSerializer
from user.models import CustomUser, CustomUserManager

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class SearchUserViewSet(viewsets.ViewSet):
    
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    @swagger_auto_schema(operation_summary='', manual_parameters=[
        openapi.Parameter(name='field', in_=openapi.IN_QUERY,
                          description='field', type=openapi.TYPE_STRING),
    ])
    def search(self, request, *args, **kwargs,):

        param = request.query_params.get('field')
        print(param)
        queryset = CustomUser.objects.all()
        queryset = queryset.filter(email__contains=param) | queryset.filter(alias__contains=param)
        #queryset = queryset.filter(alias__contains=param, email__contains=param)
        print(queryset)
        serializers = UserSerializer(queryset, many=True)
        print(serializers.data)
        
        data = {
            'search_param': param,
            'data': serializers.data
        }
        return Response(data)

class UserGroupViewSet(viewsets.ViewSet):
    
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    @action(detail=False, methods=['POST'])
    def assign(self, request, *args, **kwargs,):

        if request.user.group == None:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.group.name == 'manager':
            param = request.data
            email = param.get('email')
            groupId = param.get('groupId')
            
            queryset = CustomUser.objects.filter(email=email)[0]
            if int(groupId) == 2:
                user_group = Group.objects.get(name='editor')
            queryset.group = user_group
            queryset.save()
            serializers = UserSerializer(queryset)
            data = {
                'data': serializers.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs,):

        if request.user.group == None:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.group.name.upper() == 'MANAGER':
            queryset = CustomUser.objects.all()
            serializers = UserSerializer(queryset, many=True)
            data = {
                'data': serializers.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'data': 'action unauthorized'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['GET'])
    def groupList(self, request, *args, **kwargs):
        
        group = Group.objects.all()
        group = json.loads(serializers.serialize('json', group))
        groupList = list()
        for data in group:
            obj = dict()
            obj['id'] = data.get('pk')
            obj['name'] = data.get('fields').get('name')
            groupList.append(obj)
        data = {
            'data': groupList
        }
        return Response(data, status=status.HTTP_200_OK)



