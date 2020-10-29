from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.db import transaction

from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from user.serializers import UserSerializer
from user.models import CustomUser, CustomUserManager

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
