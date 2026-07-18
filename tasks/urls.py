from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = []

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
urlpatterns += router.urls