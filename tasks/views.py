from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import  TaskSerializer
from .pagination import TaskPagination
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework import generics


class TaskListCreateView(generics.ListCreateAPIView):
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]
  pagination_class = TaskPagination

  def get_queryset(self):
    tasks = Task.objects.filter(
      user=self.request.user,
      is_deleted=False
    )

    status_param = self.request.query_params.get('status')
    search_query = self.request.query_params.get('search')
    priority_param = self.request.query_params.get('priority')
    overdue_param = self.request.query_params.get('overdue')

    if status_param:
      tasks = tasks.filter(status=status_param)
    
    if search_query:
      tasks = tasks.filter(title__icontains=search_query)
    
    if priority_param:
      tasks = tasks.filter(priority=priority_param)
    
    if overdue_param == "true":
      tasks = tasks.filter(
        due_date__lt=now().date(),
        status='pending'
      )

    return tasks.order_by('-created_at')

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user, is_deleted=False)
  
  lookup_url_kwarg = "task_id"

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()

    instance.is_deleted = True
    instance.save()

    return Response({
      'message': "Task deleted successfully"
    }, status=status.HTTP_200_OK)