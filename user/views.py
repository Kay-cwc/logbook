from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.db import transaction

from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from user.serializers import UserSerializer
from user.models import CustomUser, CustomUserManager

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    @action(detail=False, methods=['GET'])
    def all_user(self, request, *args, **kwargs,):
        '''
        add filter param here
        '''
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        data = {
            'data': serializer.data
        }
        print(data)
        return Response(data)

class AuthRegisterView(generics.CreateAPIView):
    permissions_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    @transaction.atomic
    def post(self, request, format=None):
        #serializer = UserSerializer(data=request.data)
        print('==============================')
        param = request.data
        email = param.get('email')
        password = param.get('password')
        print(request.data)
        user = CustomUser(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_admin = False
        user.save()
        print('==============================')

        print(user)
        respones_data = {
            'data': user
        }
        return Response(respones_data, status=status.HTTP_201_CREATED)
