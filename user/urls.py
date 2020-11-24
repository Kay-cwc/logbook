from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import SearchUserViewSet, UserGroupViewSet

router = DefaultRouter()
router.register('group', UserGroupViewSet)
router.include_format_suffixes = False

# user auth endpoint

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('search/', SearchUserViewSet.as_view({'get': 'search'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
