from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from logs import views

router = DefaultRouter()
router.register('logs', views.LogsViewSet)
router.register('tasks', views.TasksViewSet)
router.include_format_suffixes = False

# user auth endpoint

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns = format_suffix_patterns(urlpatterns)
