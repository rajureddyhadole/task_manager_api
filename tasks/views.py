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

    return tasks

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def list(self, request):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many = True)

    return Response({
      'message': "Tasks fetched successfully",
      'data': serializer.data
    })



class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user, is_deleted=False)
  
  lookup_url_kwarg = "task_id"

  def perform_destroy(self, instance):
    instance.is_deleted = True
    instance.save()