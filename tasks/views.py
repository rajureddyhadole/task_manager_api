from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import  TaskSerializer
from .pagination import TaskPagination
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]
  pagination_class = TaskPagination

  def perform_create(self, serializer):
    return serializer.save(user=self.request.user)
