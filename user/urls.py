from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

'''
router = DefaultRouter()
router.register('list', views.UserViewSet)
router.include_format_suffixes = False
'''

# user auth endpoint

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/registration', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
